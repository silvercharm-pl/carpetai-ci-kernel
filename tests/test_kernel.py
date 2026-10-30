import unittest
from kernel import Policy, classify


def item(path="tests/test_example.py", status="added", patch="+assert True"):
    return {"path": path, "status": status, "patch": patch}


class KernelTests(unittest.TestCase):
    def test_green(self): self.assertEqual(classify([item("docs/notes.md")])["level"], "GREEN")
    def test_executable_test_not_green(self): self.assertEqual(classify([item("tests/test_example.py", patch="+import os; os.system(\"echo unsafe\")")])["level"], "YELLOW")
    def test_yellow(self): self.assertEqual(classify([item("src/example.py")])["level"], "YELLOW")
    def test_unknown_is_red(self): self.assertEqual(classify([item("internal/example.py")])["level"], "RED")
    def test_security_is_red(self): self.assertEqual(classify([item("security/guard.py")])["level"], "RED")
    def test_missing_patch_is_red(self): self.assertEqual(classify([item(patch=None)])["level"], "RED")
    def test_empty_patch_is_red(self): self.assertEqual(classify([item(patch="")])["level"], "RED")
    def test_whitespace_patch_is_red(self): self.assertEqual(classify([item(patch="  ")])["level"], "RED")
    def test_deletion_is_red(self): self.assertEqual(classify([item(status="removed")])["level"], "RED")
    def test_traversal_is_red(self): self.assertEqual(classify([item("../secret")])["level"], "RED")
    def test_nested_traversal_is_red(self): self.assertEqual(classify([item("tests/../secret")])["level"], "RED")
    def test_windows_path_is_red(self): self.assertEqual(classify([item("C:/tests/test.py")])["level"], "RED")
    def test_backslash_is_red(self): self.assertEqual(classify([item("tests\\test.py")])["level"], "RED")
    def test_repeated_slash_is_red(self): self.assertEqual(classify([item("tests//test.py")])["level"], "RED")
    def test_empty_is_red(self): self.assertEqual(classify([])["level"], "RED")
    def test_limit_is_red(self): self.assertEqual(classify([item()] * 2, Policy(max_green_files=1))["level"], "RED")
    def test_nested_green(self): self.assertEqual(classify([item("docs/a/b.md")])["level"], "GREEN")
    def test_red_priority(self): self.assertEqual(classify([item(), item("security/s.py")])["level"], "RED")
    def test_prefix_confusion(self): self.assertEqual(classify([item("tests-private/x.py")])["level"], "RED")
    def test_invalid_policy(self): self.assertEqual(classify([item()], Policy(max_green_files=0))["level"], "RED")
    def test_bool_green_limit_is_red(self): self.assertEqual(classify([item()], Policy(max_green_files=True))["level"], "RED")
    def test_nonpolicy_is_red(self): self.assertEqual(classify([item()], None)["level"], "RED")
    def test_malformed_green_rules_are_red(self): self.assertEqual(classify([item()], Policy(green=(None,)))["level"], "RED")
    def test_malformed_yellow_rules_are_red(self): self.assertEqual(classify([item()], Policy(yellow=["src/**"]))["level"], "RED")
    def test_malformed_red_rules_are_red(self): self.assertEqual(classify([item()], Policy(red=("../secret/**",)))["level"], "RED")
    def test_invalid_entry(self): self.assertEqual(classify([item(), None])["level"], "RED")


if __name__ == "__main__":
    unittest.main()
