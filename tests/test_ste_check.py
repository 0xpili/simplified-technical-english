"""Tests for scripts/ste_check.py. Run: python3 -m unittest discover tests"""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "ste_check.py"

spec = importlib.util.spec_from_file_location("ste_check", SCRIPT)
ste = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ste)

APPROVED = ste.load_word_list(ROOT / "references" / "word-list.md")


def check(text, mode="mixed", approved=None):
    report = ste.Report()
    ste.check_text(text, mode, report, "t", approved)
    return report


def rules(entries):
    return [rule for _loc, rule, _msg in entries]


class TestHeadings(unittest.TestCase):
    def test_text_under_heading_without_blank_line_is_checked(self):
        r = check("## Steps\nYou should not do this; it is bad.\n")
        self.assertIn("8.1", rules(r.errors))
        self.assertIn("3.2", rules(r.errors))

    def test_heading_line_alone_is_not_checked(self):
        r = check("## Removing the cover; should\n")
        self.assertEqual(r.errors, [])
        self.assertEqual(r.warnings, [])

    def test_table_row_is_not_checked(self):
        r = check("Intro text.\n| a; b | should |\n")
        self.assertEqual(r.errors, [])


class TestContractions(unittest.TestCase):
    def test_straight_apostrophe(self):
        self.assertIn("4.2", rules(check("Don't touch it.").errors))

    def test_curly_apostrophe(self):
        self.assertIn("4.2", rules(check("Don’t touch it.").errors))
        self.assertIn("4.2", rules(check("You’ll see it.").errors))


class TestSentenceSplit(unittest.TestCase):
    def test_abbreviations_do_not_end_a_sentence(self):
        text = "Refer to Fig. 2 for the data. Do e.g. the test. See No. 4 now."
        self.assertEqual(len(list(ste.iter_sentences(text))), 3)

    def test_no_false_paragraph_length_error(self):
        text = ("The engineer checked the valve. It is closed. The value is 3.5 V. "
                "Refer to Fig. 2 for details. Do e.g. the test.")
        self.assertNotIn("6.6", rules(check(text).errors))

    def test_seven_real_sentences_is_an_error(self):
        text = " ".join(["Open the valve."] * 7)
        self.assertIn("6.6", rules(check(text).errors))


class TestWordCount(unittest.TestCase):
    def test_number_with_unit_is_one_word(self):
        self.assertEqual(ste.count_words("Torque to 3.5 N.m."), 3)
        self.assertEqual(ste.count_words("Set 12.5 mm."), 2)
        self.assertEqual(ste.count_words("Keep it at 20 °C."), 4)
        self.assertEqual(ste.count_words("Use 50%."), 2)

    def test_number_and_noun_are_two_words(self):
        self.assertEqual(ste.count_words("Remove the 4 bolts."), 4)

    def test_identifier_is_one_word(self):
        self.assertEqual(ste.count_words("Open circuit breaker 36L7."), 4)

    def test_abbreviation_is_one_word(self):
        self.assertEqual(ste.count_words("Do e.g. the test."), 4)

    def test_procedural_limit_with_numbers(self):
        text = ("Torque the bolt to 3.5 N.m and then make sure that the 12.5 mm "
                "gap is 0.25 mm.")
        self.assertEqual(check(text, "procedural").errors, [])


class TestCodeBlocks(unittest.TestCase):
    def test_indented_code_block_is_removed(self):
        r = check("Text here.\n\n    indented; code block here\n")
        self.assertEqual(r.errors, [])

    def test_fenced_code_block_is_removed(self):
        r = check("Text here.\n\n```\nx = 1; y = 2\n```\n")
        self.assertEqual(r.errors, [])

    def test_nested_list_item_is_still_checked(self):
        r = check("- item one\n\n    - nested; item\n")
        self.assertIn("8.1", rules(r.errors))


class TestVerbs(unittest.TestCase):
    def test_passive_with_by_is_an_error(self):
        self.assertIn("3.6", rules(check("The valve was opened by the operator.").errors))

    def test_past_passive_without_by_is_a_warning(self):
        r = check("The unit was replaced.")
        self.assertEqual(r.errors, [])
        self.assertIn("3.6", rules(r.warnings))

    def test_condition_after_is_is_permitted(self):
        r = check("The wires are disconnected.")
        self.assertEqual(r.errors, [])
        self.assertEqual(r.warnings, [])

    def test_have_participle(self):
        self.assertIn("3.4", rules(check("The operator has adjusted the linkage.").errors))

    def test_progressive(self):
        self.assertIn("3.5", rules(check("The file is being written.").errors))

    def test_banned_modal(self):
        self.assertIn("3.2", rules(check("You should open the valve.").errors))

    def test_ing_nouns_are_not_warned(self):
        r = check("Read the warning about the housing and the wiring.")
        self.assertEqual(r.warnings, [])

    def test_ing_verb_is_warned(self):
        self.assertIn("3.5", rules(check("Removing the cover is easy.").warnings))


class TestVocabulary(unittest.TestCase):
    def test_word_list_typo_fixed(self):
        self.assertIn("walked", APPROVED)
        self.assertNotIn("walked;", APPROVED)

    def test_extra_words_are_accepted(self):
        r = check("A warning has two parts.", approved=APPROVED)
        self.assertNotIn("warning", r.unknown)
        self.assertNotIn("two", r.unknown)

    def test_unknown_word_is_reported(self):
        r = check("Use the frobnicator.", approved=APPROVED)
        self.assertIn("frobnicator", r.unknown)

    def test_allow_list(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# names of the project\nfrobnicator\ntorque-wrench  # tool\n")
        try:
            allowed = ste.load_allow_list(f.name)
        finally:
            os.unlink(f.name)
        self.assertEqual(allowed, {"frobnicator", "torque-wrench"})
        r = check("Use the frobnicator and the torque-wrench.",
                  approved=APPROVED | allowed)
        self.assertEqual(r.unknown, {})


class TestCommandLine(unittest.TestCase):
    def run_tool(self, args, text, cwd=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], input=text,
            capture_output=True, text=True, cwd=cwd,
        )

    def test_exit_codes(self):
        self.assertEqual(self.run_tool([], "Open the valve.\n").returncode, 0)
        self.assertEqual(self.run_tool([], "Open the valve; wait.\n").returncode, 1)

    def test_allow_option_and_default_file(self):
        with tempfile.TemporaryDirectory() as d:
            names = Path(d) / "names.txt"
            names.write_text("frobnicator\n", encoding="utf-8")
            out = self.run_tool(["--allow", str(names)], "Use the frobnicator.\n").stdout
            self.assertNotIn("frobnicator", out)
            (Path(d) / ".ste-allow").write_text("frobnicator\n", encoding="utf-8")
            out = self.run_tool([], "Use the frobnicator.\n", cwd=d).stdout
            self.assertNotIn("frobnicator", out)

    def test_examples_obey_the_rules(self):
        out = self.run_tool(["--mode", "descriptive",
                             str(ROOT / "examples" / "before-after.md")], "")
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_readme_obeys_the_rules(self):
        out = self.run_tool(["--mode", "descriptive", str(ROOT / "README.md")], "")
        self.assertEqual(out.returncode, 0, out.stdout)


if __name__ == "__main__":
    unittest.main()
