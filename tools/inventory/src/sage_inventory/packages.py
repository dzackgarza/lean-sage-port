"""Read the Sage distribution's package table (`build/pkgs`): versions, licences, upstream sites."""

from __future__ import annotations

import re
from pathlib import Path

from sage_inventory.models import Package

WEBSITE = re.compile(r"https?://[^\s>`)]+")


def read_packages(packages: Path) -> list[Package]:
    return [_read_package(directory) for directory in sorted(packages.iterdir()) if (directory / "type").is_file()]


def _read_package(directory: Path) -> Package:
    description = directory / "SPKG.rst"
    text = description.read_text() if description.is_file() else ""
    version = next(
        (
            (directory / name).read_text().strip()
            for name in ("package-version.txt", "version_requirements.txt")
            if (directory / name).is_file()
        ),
        "",
    )
    website = WEBSITE.search(text)
    return Package(
        name=directory.name,
        type=(directory / "type").read_text().strip(),
        version=version,
        license=_section(text, "License"),
        website=website.group(0).rstrip(".,") if website else "",
    )


def _section(text: str, heading: str) -> str:
    """Return the body of one underlined section of an SPKG.rst, joined on one line."""
    lines = text.splitlines()
    body: list[str] = []
    inside = False
    for number, line in enumerate(lines):
        underlined = number + 1 < len(lines) and re.fullmatch(r"[-=~^]{3,}\s*", lines[number + 1])
        if underlined:
            if inside:
                break
            inside = line.strip().lower() == heading.lower()
            continue
        if inside and not re.fullmatch(r"[-=~^]{3,}\s*", line):
            body.append(line.strip())
    return " ".join(part for part in body if part)
