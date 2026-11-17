"""Extract the classes, functions and methods of one Sage source file.

Python files are read with `ast`, Cython files with the parser of the Cython compiler. Both give
exact entity boundaries and docstrings.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

from Cython.Compiler import Errors, ExprNodes, Nodes
from Cython.Compiler.Main import CompilationOptions, Context, default_options
from Cython.Compiler.Scanning import FileSourceDescriptor

from sage_inventory.models import Entity, EntityKind

PROMPT = re.compile(r"^\s*sage: ", re.MULTILINE)
ALGORITHM = re.compile(r"^\s*ALGORITHMS?:", re.MULTILINE)
CITATION = re.compile(r"\[([A-Za-z][A-Za-z0-9+-]*\d{2,4}[a-z]?)\]_")
IMPORT = re.compile(
    r"""^\s*(?:from|import|cimport)\s+([A-Za-z_][\w.]*)|lazy_import\(\s*['"]([\w.]+)['"]""",
    re.MULTILINE,
)
FEATURE = re.compile(r"#\s*(?:optional|needs)\s*[-:]?\s*([^#\n]+)")

# Third-party imports that name a computational engine, and the engine's name in the index.
ENGINES = {
    "cypari2": "pari",
    "gmpy2": "gmp",
    "pplpy": "ppl",
    "ppl": "ppl",
    "numpy": "numpy",
    "scipy": "scipy",
    "sympy": "sympy",
    "mpmath": "mpmath",
    "networkx": "networkx",
    "cvxopt": "cvxopt",
    "primecountpy": "primecount",
}


@dataclass(frozen=True)
class Scan:
    title: str
    entities: tuple[Entity, ...]
    doctests: int
    backends: tuple[str, ...]
    features: tuple[str, ...]


def scan_file(module: str, path: Path, include: Path) -> Scan:
    """Scan one source file. `include` is the directory that holds the top-level `sage` package."""
    text = path.read_text()
    if path.suffix == ".pyx":
        title, entities = _cython_entities(module, path, include)
    else:
        title, entities = _python_entities(module, text)
    # A name defined more than once (typing overloads, a property and its setter, a Cython forward
    # declaration) is one entity: the definition that carries the documentation.
    unique: dict[str, Entity] = {}
    for entity in entities:
        kept = unique.get(entity.id)
        if kept is None or entity.doctests > kept.doctests:
            unique[entity.id] = entity
    return Scan(
        title=title,
        entities=tuple(unique.values()),
        doctests=len(PROMPT.findall(text)),
        backends=_backends(text),
        features=_features(text),
    )


def _entity(module: str, qualname: str, kind: EntityKind, line: int, bases: tuple[str, ...], doc: str) -> Entity:
    return Entity(
        id=f"{module}:{qualname}",
        module=module,
        qualname=qualname,
        kind=kind,
        public=not any(part.startswith("_") for part in qualname.split(".")),
        line=line,
        bases=bases,
        doctests=len(PROMPT.findall(doc)),
        algorithm=bool(ALGORITHM.search(doc)),
        references=tuple(sorted(set(CITATION.findall(doc)))),
    )


def _first_line(doc: str) -> str:
    return next((line.strip() for line in doc.splitlines() if line.strip()), "")


def _python_entities(module: str, text: str) -> tuple[str, list[Entity]]:
    tree = ast.parse(text)
    found: list[Entity] = []

    def visit(body: list[ast.stmt], prefix: str) -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                qualname = f"{prefix}{node.name}"
                bases = tuple(ast.unparse(base) for base in node.bases)
                found.append(
                    _entity(module, qualname, EntityKind.CLASS, node.lineno, bases, ast.get_docstring(node) or "")
                )
                visit(node.body, f"{qualname}.")
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                kind = EntityKind.METHOD if prefix else EntityKind.FUNCTION
                found.append(
                    _entity(module, f"{prefix}{node.name}", kind, node.lineno, (), ast.get_docstring(node) or "")
                )

    visit(tree.body, "")
    return _first_line(ast.get_docstring(tree) or ""), found


def _cython_entities(module: str, path: Path, include: Path) -> tuple[str, list[Entity]]:
    """Parse with Cython's own parser (`Cython.Compiler`), stopping before type analysis."""
    Errors.init_thread()
    context = Context.from_options(CompilationOptions(default_options, include_path=[str(include)]))
    source = FileSourceDescriptor(str(path), str(path.relative_to(include)))
    scope = context.find_module(module, pos=(source, 1, 0), need_pxd=False)
    tree = context.parse(source, scope, pxd=False, full_module_name=module)
    found: list[Entity] = []

    def visit(node: Nodes.Node | None, prefix: str) -> None:
        if isinstance(node, Nodes.StatListNode):
            for statement in node.stats:
                visit(statement, prefix)
        elif isinstance(node, Nodes.CClassDefNode | Nodes.PyClassDefNode):
            name = node.class_name if isinstance(node, Nodes.CClassDefNode) else node.name
            bases = tuple(_cython_name(base) for base in node.bases.args) if node.bases else ()
            found.append(_entity(module, f"{prefix}{name}", EntityKind.CLASS, node.pos[1], bases, node.doc or ""))
            visit(node.body, f"{prefix}{name}.")
        elif isinstance(node, Nodes.DefNode) or (isinstance(node, Nodes.CFuncDefNode) and node.overridable):
            # `cdef` functions are invisible from Python; `def` and `cpdef` are the callable surface.
            kind = EntityKind.METHOD if prefix else EntityKind.FUNCTION
            name = node.name if isinstance(node, Nodes.DefNode) else _declared_name(node.declarator)
            found.append(_entity(module, f"{prefix}{name}", kind, node.pos[1], (), node.doc or ""))

    visit(tree.body, "")
    return _first_line(tree.doc or ""), found


def _declared_name(declarator: Nodes.CDeclaratorNode) -> str:
    while not isinstance(declarator, Nodes.CNameDeclaratorNode):
        declarator = declarator.base
    return str(declarator.name)


def _cython_name(node: ExprNodes.ExprNode) -> str:
    if isinstance(node, ExprNodes.AttributeNode):
        return f"{_cython_name(node.obj)}.{node.attribute}"
    return str(getattr(node, "name", type(node).__name__))


def _backends(text: str) -> tuple[str, ...]:
    names: set[str] = set()
    for direct, lazy in IMPORT.findall(text):
        parts = (direct or lazy).split(".")
        if parts[0] == "sage" and len(parts) >= 3 and parts[1] == "libs":
            names.add(parts[2])
        elif parts[0] == "sage" and len(parts) >= 3 and parts[1] == "interfaces":
            names.add(f"interface:{parts[2]}")
        elif parts[0] in ENGINES:
            names.add(ENGINES[parts[0]])
    return tuple(sorted(names))


def _features(text: str) -> tuple[str, ...]:
    tags: set[str] = set()
    for group in FEATURE.findall(text):
        for token in re.split(r"[\s,]+", group.strip()):
            if re.fullmatch(r"[A-Za-z_][\w.]*", token) and token not in {"optional", "needs", "internet"}:
                tags.add(token)
    return tuple(sorted(tags))
