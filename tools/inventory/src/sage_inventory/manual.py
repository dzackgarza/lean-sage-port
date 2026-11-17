"""Read the Sage reference manual's table of contents: which module is documented where.

The manual is reStructuredText. Its front page groups section directories under thematic headings,
and each section lists modules as toctree entries of the form `sage/rings/integer`. A toctree entry
that is not a module names another document of the section, which is read the same way.
"""

from __future__ import annotations

import re
from pathlib import Path

from sage_inventory.models import ManualPlacement

SECTION_LINK = re.compile(r"^\* :doc:`(.+?) <(\w+)/index>`")
ENTRY_TARGET = re.compile(r"<(.+)>\s*$")
UNDERLINE = re.compile(r"^([=\-~^\"'*+#`.:_])\1{2,}\s*$")


def front_page(manual: Path) -> dict[str, tuple[str, str]]:
    """Map each section directory to (thematic group, section title)."""
    lines = (manual / "index.rst").read_text().splitlines()
    sections: dict[str, tuple[str, str]] = {}
    part, chapter = "", ""
    for number, line in enumerate(lines):
        following = lines[number + 1] if number + 1 < len(lines) else ""
        if line.strip() and following.startswith("==="):
            part, chapter = line.strip(), ""
        elif line.strip() and following.startswith("---"):
            chapter = line.strip()
        elif match := SECTION_LINK.match(line):
            title = match.group(1).replace("\\\\(", "").replace("\\\\)", "").replace("\\\\", "\\")
            sections[match.group(2)] = (f"{part} / {chapter}" if chapter else part, title)
    return sections


def placements(manual: Path) -> dict[str, ManualPlacement]:
    """Map each documented module to its first placement in the manual."""
    found: dict[str, ManualPlacement] = {}
    for section, (group, title) in sorted(front_page(manual).items()):
        _read_document(manual / section, "index", (), group, section, title, found, set())
    return found


def _read_document(
    directory: Path,
    name: str,
    inherited: tuple[str, ...],
    group: str,
    section: str,
    title: str,
    found: dict[str, ManualPlacement],
    seen: set[str],
) -> None:
    path = directory / f"{name}.rst"
    if name in seen or not path.is_file():
        return
    seen.add(name)
    lines = path.read_text().splitlines()
    levels: list[str] = []
    headings: list[str] = []
    in_toctree = False
    for number, line in enumerate(lines):
        following = lines[number + 1] if number + 1 < len(lines) else ""
        underline = UNDERLINE.match(following)
        if line.strip() and not line.startswith(" ") and underline and len(following.strip()) >= len(line.strip()):
            mark = underline.group(1)
            if mark not in levels:
                levels.append(mark)
            headings = [*headings[: levels.index(mark)], line.strip()]
            in_toctree = False
            continue
        if line.startswith(".. toctree::"):
            in_toctree = True
            continue
        if in_toctree and line.strip() and not line.startswith(" "):
            in_toctree = False
        entry = line.strip()
        if not in_toctree or not entry or entry.startswith(":"):
            continue
        target = ENTRY_TARGET.search(entry)
        entry = target.group(1) if target else entry
        # A section's front document is titled with the section title, which the placement already holds.
        context = (*inherited, *(headings[1:] if name == "index" else headings))
        if entry.startswith("sage/"):
            found.setdefault(
                entry.replace("/", "."),
                ManualPlacement(group=group, section=section, section_title=title, headings=context),
            )
        else:
            _read_document(directory, entry, context, group, section, title, found, seen)
