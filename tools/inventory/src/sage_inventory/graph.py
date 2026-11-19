"""Derive the capability dependency graph from the `depends_on` fields of the records.

An edge is a mandatory prerequisite: an input that the record's selected complete computational
route consumes. An algorithm family that needs an extra input does not create an edge; that input
belongs to the family's own specification. The derivation therefore rejects an edge to a capability
that no record states, and it rejects a cycle, because a cycle means the records have not yet
separated a prerequisite from an algorithm alternative.

`levels` is the build order: a capability's level is one more than the largest level among its
prerequisites, so every capability of a level can be built once the earlier levels exist.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from pydantic import validate_call

from sage_inventory.coverage import load_records
from sage_inventory.models import Capability, DependencyGraph, GraphNode


class GraphError(ValueError):
    """The `depends_on` fields do not form an acyclic graph over the stated capabilities."""


@validate_call
def derive(capabilities: tuple[Capability, ...]) -> DependencyGraph:
    """Resolve every edge, reject a wrong or cyclic one, and assign the build levels."""
    records = {capability.id: capability for capability in capabilities}
    repeated = sorted(
        identifier for identifier, count in Counter(c.id for c in capabilities).items() if count > 1
    )
    if repeated:
        raise GraphError(f"capability id stated more than once: {', '.join(repeated)}")

    unknown = sorted(
        {prerequisite for capability in capabilities for prerequisite in capability.depends_on}
        - records.keys()
    )
    if unknown:
        raise GraphError(f"depends_on names no capability record: {', '.join(unknown)}")

    dependents: dict[str, set[str]] = defaultdict(set)
    states: dict[str, int] = {}
    levels: dict[str, int] = {}

    def visit(identifier: str, path: tuple[str, ...]) -> int:
        """Depth-first post-order: a capability's level is fixed after its prerequisites."""
        state = states.get(identifier, 0)
        if state == 2:
            return levels[identifier]
        if state == 1:
            cycle = path[path.index(identifier) :] + (identifier,)
            raise GraphError(f"dependency cycle: {' -> '.join(cycle)}")
        states[identifier] = 1
        prerequisites = records[identifier].depends_on
        level = 0 if not prerequisites else 1 + max(visit(p, path + (identifier,)) for p in prerequisites)
        states[identifier] = 2
        levels[identifier] = level
        for prerequisite in prerequisites:
            dependents[prerequisite].add(identifier)
        return level

    for identifier in sorted(records):
        visit(identifier, ())

    nodes = tuple(
        GraphNode(
            id=identifier,
            level=levels[identifier],
            depends_on=tuple(sorted(records[identifier].depends_on)),
            dependents=tuple(sorted(dependents[identifier])),
            reuse=records[identifier].reuse.status,
            catalogue=records[identifier].catalogue,
            algorithm_families=len(records[identifier].algorithms),
        )
        for identifier in sorted(records)
    )
    return DependencyGraph(
        capabilities=len(nodes),
        edges=sum(len(node.depends_on) for node in nodes),
        roots=tuple(node.id for node in nodes if not node.depends_on),
        levels=tuple(
            tuple(node.id for node in nodes if node.level == level)
            for level in range(max(levels.values(), default=-1) + 1)
        ),
        nodes=nodes,
    )


@validate_call
def build(capabilities: Path) -> DependencyGraph:
    """Read every capability record of a directory and derive its dependency graph."""
    records, _ = load_records(capabilities)
    return derive(tuple(records))
