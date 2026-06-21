#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def fail(message: str) -> None:
    raise SystemExit(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_toml(path: Path) -> dict:
    return tomllib.loads(read_text(path))


def root_version() -> str:
    payload = json.loads(read_text(ROOT / "version.json"))
    version = payload.get("version")
    if not isinstance(version, str) or not version.strip():
        fail("version.json must contain a non-empty string field `version`")
    return version


def workspace_version() -> str:
    manifest = load_toml(ROOT / "Cargo.toml")
    version = manifest.get("workspace", {}).get("package", {}).get("version")
    if not isinstance(version, str) or not version.strip():
        fail("Cargo.toml is missing [workspace.package].version")
    return version


def workspace_manifests() -> list[Path]:
    manifest = load_toml(ROOT / "Cargo.toml")
    members = manifest.get("workspace", {}).get("members", [])
    manifests: list[Path] = []
    for member in members:
        if not isinstance(member, str):
            continue
        manifest_path = ROOT / member / "Cargo.toml"
        if manifest_path.exists():
            manifests.append(manifest_path)
    return manifests


def package_version(manifest: dict, label: str, workspace_fallback: str) -> str:
    package = manifest.get("package", {})
    version = package.get("version")
    if isinstance(version, dict) and version.get("workspace") is True:
        return workspace_fallback
    if not isinstance(version, str) or not version.strip():
        fail(f"{label} is missing [package].version")
    return version


def dependency_sections(manifest: dict) -> list[tuple[str, dict]]:
    sections: list[tuple[str, dict]] = []
    for section_name in ("dependencies", "dev-dependencies", "build-dependencies"):
        dependencies = manifest.get(section_name)
        if isinstance(dependencies, dict):
            sections.append((section_name, dependencies))
    return sections


def validate_path_dependency_versions() -> None:
    fallback = workspace_version()
    manifests = workspace_manifests()
    versions: dict[Path, str] = {}
    parsed: dict[Path, tuple[str, dict]] = {}
    for manifest_path in manifests:
        rel_manifest = manifest_path.relative_to(ROOT).as_posix()
        manifest = load_toml(manifest_path)
        parsed[manifest_path] = (rel_manifest, manifest)
        versions[manifest_path.parent.resolve()] = package_version(manifest, rel_manifest, fallback)

    for manifest_path, (rel_manifest, manifest) in parsed.items():
        for section_name, dependencies in dependency_sections(manifest):
            for dependency_name, dependency in dependencies.items():
                if not isinstance(dependency, dict):
                    continue
                dependency_path = dependency.get("path")
                if not isinstance(dependency_path, str):
                    continue
                resolved = (manifest_path.parent / dependency_path).resolve()
                expected_version = versions.get(resolved)
                if expected_version is None:
                    continue
                pinned_version = dependency.get("version")
                if pinned_version != expected_version:
                    fail(
                        f"{rel_manifest} [{section_name}.{dependency_name}] "
                        f'version "{pinned_version}" does not match target crate version "{expected_version}"'
                    )


def validate_python_version(expected_version: str) -> bool:
    pyproject = ROOT / "python" / "pyproject.toml"
    if not pyproject.exists():
        return False
    manifest = load_toml(pyproject)
    project_version = manifest.get("project", {}).get("version")
    if project_version != expected_version:
        fail(
            f"python/pyproject.toml project.version ({project_version}) "
            f"does not match version.json ({expected_version})"
        )
    version_module = ROOT / "python" / "units_x" / "_version.py"
    text = read_text(version_module)
    match = re.search(r'__version__ = "([^"]+)"', text)
    if match is None:
        fail("python/units_x/_version.py is missing a __version__ assignment")
    if match.group(1) != expected_version:
        fail(
            f"python/units_x/_version.py __version__ ({match.group(1)}) "
            f"does not match version.json ({expected_version})"
        )
    return True


def expected_assembly_version(version: str) -> str:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version.strip())
    if match is None:
        fail(f"unsupported semantic version for assembly conversion: {version}")
    major, minor, patch = match.groups()
    return f"{major}.{minor}.{patch}.0"


def validate_dotnet_version(expected_version: str) -> bool:
    props_path = ROOT / "dotnet" / "Directory.Build.props"
    if not props_path.exists():
        return False
    root = ET.fromstring(read_text(props_path))
    property_group = root.find("PropertyGroup")
    if property_group is None:
        fail("dotnet/Directory.Build.props is missing a PropertyGroup")

    expected_values = {
        "UnitsXVersion": expected_version,
        "UnitsXAssemblyVersion": expected_assembly_version(expected_version),
        "Version": "$(UnitsXVersion)",
        "PackageVersion": "$(UnitsXVersion)",
        "AssemblyVersion": "$(UnitsXAssemblyVersion)",
        "FileVersion": "$(UnitsXAssemblyVersion)",
        "InformationalVersion": "$(UnitsXVersion)",
    }
    for tag, expected_value in expected_values.items():
        node = property_group.find(tag)
        if node is None or (node.text or "").strip() != expected_value:
            actual_value = None if node is None else (node.text or "").strip()
            fail(
                f"dotnet/Directory.Build.props {tag} ({actual_value}) "
                f"does not match expected value ({expected_value})"
            )
    return True


def main() -> int:
    expected = root_version()
    workspace = workspace_version()
    if workspace != expected:
        fail(f"Cargo.toml workspace version ({workspace}) does not match version.json ({expected})")

    validate_path_dependency_versions()

    checked = ["version.json", "Cargo.toml", "workspace path dependency versions"]
    if validate_python_version(expected):
        checked.extend(["python/pyproject.toml", "python/units_x/_version.py"])
    if validate_dotnet_version(expected):
        checked.append("dotnet/Directory.Build.props")

    print(f"version sync check passed: {expected} [{', '.join(checked)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
