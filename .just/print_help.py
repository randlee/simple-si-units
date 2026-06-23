#!/usr/bin/env python3
from __future__ import annotations

SECTIONS = (
    (
        "General",
        (
            ("help", "Show this help."),
            ("build", "Run the fast lint gate, then build the workspace with all features."),
            ("test", "Run the full repo test pass."),
            ("test all", "Clean, regenerate, lint, and run the full repo verification pass."),
            ("test unit", "Run Rust unit tests."),
            ("test python", "Run Python helper-script tests."),
            ("test dotnet", "Run .NET tests when the .NET surface exists."),
            ("test integration", "Run integration-style tests."),
            ("test rust", "Run all Rust workspace tests."),
            ("clean", "Remove workspace build artifacts."),
            ("version", "Verify the shared version source stays synchronized."),
            ("ci", "Run the local CI-equivalent command set."),
        ),
    ),
    (
        "Formatting",
        (
            ("fmt", "Check Rust formatting."),
            ("fmt check", "Check Rust formatting."),
            ("fmt write", "Format the Rust workspace in place."),
            ("fmt apply", "Format the Rust workspace in place."),
        ),
    ),
    (
        "Lint",
        (
            ("lint", "Run the default full lint profile."),
            ("lint fast", "Run the fast lint subset used by `just build`."),
            ("lint full", "Run the stronger local lint profile."),
            ("lint fmt", "Run only the format check."),
            ("lint version", "Run only the version synchronization check."),
            ("lint check", "Run only `sc-lint check native`."),
            ("lint clippy", "Run only `sc-lint clippy native`."),
            ("lint sc-boundary", "Run the boundary analyzer wrapper."),
            ("lint identity-literals", "Run the string-duplication/canonical-literal lint."),
            ("lint pytests", "Run the Python helper-script unit tests."),
        ),
    ),
)


TOPIC_ALIASES = {
    "build": "build",
    "generate": "generate",
    "clean": "clean",
    "version": "version",
    "ci": "ci",
    "test": "test",
    "tests": "test",
    "lint": "lint",
    "fmt": "fmt",
    "format": "fmt",
}


def render_help(repo_name: str) -> str:
    lines = [
        f"{repo_name} task runner",
        "",
        "Usage:",
        "  just <recipe>",
        "",
    ]
    width = max(len(name) for _, recipes in SECTIONS for name, _ in recipes)
    for section_name, recipes in SECTIONS:
        lines.append(f"{section_name}:")
        for name, description in recipes:
            lines.append(f"  {name.ljust(width)}  {description}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_topic_help(topic: str) -> str:
    normalized = TOPIC_ALIASES.get(topic.lower(), topic.lower())
    if normalized == "build":
        return (
            "Build commands:\n"
            "  just build       Regenerate code, run the fast lint gate, and build the workspace.\n"
            "  just build help  Show this build help.\n"
        )
    if normalized == "generate":
        return (
            "Generate commands:\n"
            "  just generate       Run the code-generation step and format generated Rust.\n"
            "  just generate help  Show this generate help.\n"
        )
    if normalized == "clean":
        return (
            "Clean commands:\n"
            "  just clean       Remove workspace build artifacts with `cargo clean`.\n"
            "  just clean help  Show this clean help.\n"
        )
    if normalized == "version":
        return (
            "Version commands:\n"
            "  just version       Verify the shared version source stays synchronized.\n"
            "  just version help  Show this version help.\n"
        )
    if normalized == "ci":
        return (
            "CI commands:\n"
            "  just ci       Run `just test`, then the shipped-scope clippy and sc-boundary gates.\n"
            "  just ci help  Show this CI help.\n"
        )
    if normalized == "test":
        return (
            "Test scopes:\n"
            "  just test           Run the full repo test pass.\n"
            "  just test all       Alias for the full repo test pass.\n"
            "  just test unit      Run Rust unit tests.\n"
            "  just test python    Run Python helper-script tests and native wheel smoke.\n"
            "  just test dotnet    Run .NET tests when configured.\n"
            "  just test integration  Run integration-style tests.\n"
            "  just test rust      Run all Rust workspace tests.\n"
        )
    if normalized == "lint":
        return (
            "Lint targets:\n"
            "  just lint             Run the default full lint profile.\n"
            "  just lint fast        Run the fast lint subset.\n"
            "  just lint full        Run the stronger local lint profile.\n"
            "  just lint fmt         Run only the format check.\n"
            "  just lint version     Run only the version synchronization check.\n"
            "  just lint check       Run only `sc-lint check native`.\n"
            "  just lint clippy      Run only `sc-lint clippy native`.\n"
            "  just lint sc-boundary Run the boundary analyzer wrapper.\n"
            "  just lint identity-literals  Run the canonical literal lint.\n"
            "  just lint pytests     Run the Python helper-script unit tests.\n"
        )
    if normalized == "fmt":
        return (
            "Format modes:\n"
            "  just fmt         Check Rust formatting.\n"
            "  just fmt check   Check Rust formatting.\n"
            "  just fmt write   Format the Rust workspace in place.\n"
            "  just fmt apply   Format the Rust workspace in place.\n"
        )
    return f"unknown help topic: {topic}\n"


def main() -> int:
    import sys

    topic = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else ""
    if topic:
        text = render_topic_help(topic)
        if text.startswith("unknown help topic:"):
            print(text, end="", file=sys.stderr)
            return 2
        print(text, end="")
        return 0
    print(render_help("units-x"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
