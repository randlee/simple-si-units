#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, contents: str) -> bool:
    if path.exists() and read_text(path) == contents:
        return False
    path.write_text(contents, encoding="utf-8")
    return True


def root_version() -> str:
    payload = json.loads(read_text(ROOT / "version.json"))
    version = payload.get("version")
    if not isinstance(version, str) or not version.strip():
        raise SystemExit("version.json must contain a non-empty string field `version`")
    return version


def assembly_version(version: str) -> str:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version.strip())
    if match is None:
        raise SystemExit(f"unsupported semantic version for assembly conversion: {version}")
    major, minor, patch = match.groups()
    return f"{major}.{minor}.{patch}.0"


def update_toml_scalar(path: Path, section: str, key: str, value: str) -> bool:
    lines = read_text(path).splitlines()
    current_section: str | None = None
    updated = False
    rendered = f'{key} = "{value}"'

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            current_section = stripped[1:-1]
            continue
        if current_section != section:
            continue
        if stripped.startswith(f"{key} = "):
            if line != rendered:
                lines[index] = rendered
                updated = True
            break
    else:
        raise SystemExit(f"{path.relative_to(ROOT).as_posix()} is missing [{section}] {key}")

    return write_text(path, "\n".join(lines) + "\n") if updated else False


def sync_python_runtime_version(version: str) -> bool:
    contents = (
        '"""Generated version metadata for units-x."""\n\n'
        f'__version__ = "{version}"\n'
    )
    return write_text(ROOT / "python" / "units_x" / "_version.py", contents)


def sync_dotnet_props(version: str) -> bool:
    props_path = ROOT / "dotnet" / "Directory.Build.props"
    tree = ET.parse(props_path)
    root = tree.getroot()
    property_group = root.find("PropertyGroup")
    if property_group is None:
        raise SystemExit("dotnet/Directory.Build.props is missing a PropertyGroup")

    mapping = {
        "UnitsXVersion": version,
        "UnitsXAssemblyVersion": assembly_version(version),
        "Version": "$(UnitsXVersion)",
        "PackageVersion": "$(UnitsXVersion)",
        "AssemblyVersion": "$(UnitsXAssemblyVersion)",
        "FileVersion": "$(UnitsXAssemblyVersion)",
        "InformationalVersion": "$(UnitsXVersion)",
    }
    changed = False
    for tag, value in mapping.items():
        node = property_group.find(tag)
        if node is None:
            node = ET.SubElement(property_group, tag)
            changed = True
        if node.text != value:
            node.text = value
            changed = True

    if not changed:
        return False

    ET.indent(tree, space="  ")
    tree.write(props_path, encoding="unicode")
    return True


def main() -> int:
    version = root_version()
    changed_files: list[str] = []

    if update_toml_scalar(ROOT / "Cargo.toml", "workspace.package", "version", version):
        changed_files.append("Cargo.toml")
    if update_toml_scalar(ROOT / "python" / "pyproject.toml", "project", "version", version):
        changed_files.append("python/pyproject.toml")
    if sync_python_runtime_version(version):
        changed_files.append("python/units_x/_version.py")
    if sync_dotnet_props(version):
        changed_files.append("dotnet/Directory.Build.props")

    if changed_files:
        print("synchronized version metadata from version.json:")
        for path in changed_files:
            print(f"  {path}")
    else:
        print("version metadata already synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
