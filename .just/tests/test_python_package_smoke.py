from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = ROOT / ".just" / "run_python_package_smoke.py"
SPEC = importlib.util.spec_from_file_location("run_python_package_smoke", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class PythonPackageSmokeTests(unittest.TestCase):
    def test_build_and_import_uses_run_scoped_wheelhouse(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-python-smoke-test-") as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "python").mkdir(parents=True, exist_ok=True)

            commands: list[list[str]] = []

            def fake_run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> int:
                commands.append(command)
                if command[:3] == [smoke.sys.executable or "python3", "-m", "build"]:
                    outdir = Path(command[command.index("--outdir") + 1])
                    self.assertNotEqual(outdir, repo_root / "python" / "dist")
                    outdir.mkdir(parents=True, exist_ok=True)
                    (outdir / "units_x-0.1.0-py3-none-any.whl").write_text("", encoding="utf-8")
                return 0

            with mock.patch.object(smoke, "run", side_effect=fake_run):
                code = smoke.build_and_import(repo_root)

            self.assertEqual(code, 0)
            self.assertEqual(len(commands), 3)
            install_command = commands[1]
            wheel_path = Path(install_command[-1])
            self.assertEqual(wheel_path.name, "units_x-0.1.0-py3-none-any.whl")
            self.assertNotEqual(wheel_path.parent, repo_root / "python" / "dist")


if __name__ == "__main__":
    unittest.main()
