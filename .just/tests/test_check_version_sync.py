from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from check_version_sync import root_version
from check_version_sync import validate_dotnet_version
from check_version_sync import validate_python_version
from check_version_sync import workspace_version


class VersionSyncSmokeTests(unittest.TestCase):
    def test_root_version_is_first_publish_version(self) -> None:
        self.assertEqual(root_version(), "0.1.0")

    def test_workspace_version_matches_root_version(self) -> None:
        self.assertEqual(workspace_version(), root_version())

    def test_python_version_is_wired(self) -> None:
        self.assertTrue(validate_python_version(root_version()))

    def test_dotnet_version_is_wired(self) -> None:
        self.assertTrue(validate_dotnet_version(root_version()))


if __name__ == "__main__":
    unittest.main()
