#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tomllib
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


def load_toml(path: Path) -> dict:
    return tomllib.loads(read_text(path))


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


def workspace_member_manifests() -> list[Path]:
    manifest = load_toml(ROOT / "Cargo.toml")
    members = manifest.get("workspace", {}).get("members", [])
    manifests: list[Path] = []
    for member in members:
        if isinstance(member, str):
            manifest_path = ROOT / member / "Cargo.toml"
            if manifest_path.exists():
                manifests.append(manifest_path)
    return manifests


def update_inline_table_dependency_version(
    manifest_path: Path,
    section_name: str,
    dependency_name: str,
    version: str,
) -> bool:
    lines = read_text(manifest_path).splitlines()
    current_section: str | None = None
    updated = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            current_section = stripped[1:-1]
            continue
        if current_section != section_name:
            continue
        if not stripped.startswith(f"{dependency_name} = "):
            continue
        if "{" not in line or "}" not in line:
            raise SystemExit(
                f"{manifest_path.relative_to(ROOT).as_posix()} dependency "
                f"{dependency_name} in [{section_name}] must use a single-line inline table"
            )
        if 'version = "' in line:
            rendered = re.sub(r'version = "[^"]*"', f'version = "{version}"', line)
        else:
            rendered = line.replace(" }", f', version = "{version}" }}')
            rendered = rendered.replace("}", f', version = "{version}" }}', 1)
        if rendered != line:
            lines[index] = rendered
            updated = True
        break
    else:
        raise SystemExit(
            f"{manifest_path.relative_to(ROOT).as_posix()} is missing "
            f"[{section_name}] {dependency_name}"
        )

    return write_text(manifest_path, "\n".join(lines) + "\n") if updated else False


def sync_workspace_path_dependency_versions(version: str) -> list[str]:
    manifests = workspace_member_manifests()
    workspace_dirs = {manifest.parent.resolve() for manifest in manifests}
    changed_files: list[str] = []

    for manifest_path in manifests:
        manifest = load_toml(manifest_path)
        changed = False
        for section_name in ("dependencies", "dev-dependencies", "build-dependencies"):
            dependencies = manifest.get(section_name)
            if not isinstance(dependencies, dict):
                continue
            for dependency_name, dependency in dependencies.items():
                if not isinstance(dependency, dict):
                    continue
                dependency_path = dependency.get("path")
                if not isinstance(dependency_path, str):
                    continue
                resolved = (manifest_path.parent / dependency_path).resolve()
                if resolved not in workspace_dirs:
                    continue
                if update_inline_table_dependency_version(
                    manifest_path,
                    section_name,
                    dependency_name,
                    version,
                ):
                    changed = True
        if changed:
            changed_files.append(manifest_path.relative_to(ROOT).as_posix())

    return changed_files


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
    changed_files.extend(sync_workspace_path_dependency_versions(version))
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
