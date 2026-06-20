from __future__ import annotations

import unittest

from print_help import render_help, render_topic_help


class PrintHelpTests(unittest.TestCase):
    def test_help_mentions_sc_boundary_and_identity_literals(self) -> None:
        output = render_help("units-x")
        self.assertIn("lint sc-boundary", output)
        self.assertIn("lint identity-literals", output)

    def test_build_help_is_available(self) -> None:
        output = render_topic_help("build")
        self.assertIn("just build help", output)

    def test_generate_help_is_available(self) -> None:
        output = render_topic_help("generate")
        self.assertIn("just generate help", output)


if __name__ == "__main__":
    unittest.main()
