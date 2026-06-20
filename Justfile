set windows-shell := ["pwsh", "-NoLogo", "-Command"]

python_cmd := if os_family() == "windows" { "python" } else { "python3" }

default: help

help topic='':
    {{python_cmd}} .just/print_help.py {{topic}}

[private]
_fmt-write:
    cargo fmt --all

[private]
_fmt-check:
    cargo fmt --all --check

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

generate topic='run':
    {{python_cmd}} .just/run_general.py generate {{topic}}

build topic='run':
    {{python_cmd}} .just/run_general.py build {{topic}}

test scope='all':
    {{python_cmd}} .just/run_tests.py {{scope}}

clean topic='run':
    {{python_cmd}} .just/run_general.py clean {{topic}}

version topic='run':
    {{python_cmd}} .just/run_general.py version {{topic}}

lint target='full':
    {{python_cmd}} .just/run_lint.py {{target}}

ci topic='run':
    {{python_cmd}} .just/run_general.py ci {{topic}}
