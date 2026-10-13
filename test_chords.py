import io
import unittest
from unittest import mock

import chords


class FretSymbolTests(unittest.TestCase):
    def test_open_string_is_O(self):
        self.assertEqual(chords.fret_symbol(0), "O")

    def test_muted_string_is_X(self):
        self.assertEqual(chords.fret_symbol(-1), "X")

    def test_fretted_string_is_its_number(self):
        self.assertEqual(chords.fret_symbol(3), "3")


class ChordTableTests(unittest.TestCase):
    def test_at_least_five_chords(self):
        self.assertGreaterEqual(len(chords.CHORDS), 5)

    def test_every_chord_has_six_valid_frets(self):
        for name, frets in chords.CHORDS.items():
            with self.subTest(chord=name):
                self.assertEqual(len(frets), 6)
                for fret in frets:
                    self.assertGreaterEqual(fret, -1)


class DiagramTests(unittest.TestCase):
    def test_c_diagram(self):
        expected = (
            "Chord: C\n"
            "--------\n"
            "6: O\n"
            "5: 3\n"
            "4: 2\n"
            "3: O\n"
            "2: 1\n"
            "1: O"
        )
        self.assertEqual(chords.diagram("C"), expected)

    def test_g_differs_from_c(self):
        lines = chords.diagram("G").splitlines()
        self.assertEqual(lines[2:], ["6: 3", "5: 2", "4: O", "3: O", "2: O", "1: 3"])
        self.assertNotEqual(chords.diagram("G"), chords.diagram("C"))

    def test_muted_strings_show_X(self):
        lines = chords.diagram("D").splitlines()
        self.assertEqual(lines[2], "6: X")
        self.assertEqual(lines[3], "5: X")

    def test_underline_matches_heading_length(self):
        lines = chords.diagram("Am").splitlines()
        self.assertEqual(lines[0], "Chord: Am")
        self.assertEqual(lines[1], "-" * len(lines[0]))

    def test_every_diagram_is_plain_text(self):
        for name in chords.CHORDS:
            with self.subTest(chord=name):
                text = chords.diagram(name)
                self.assertTrue(text.isascii())
                self.assertEqual(len(text.splitlines()), 8)

    def test_decorator_keeps_function_name(self):
        self.assertEqual(chords.diagram.__name__, "diagram")


class MainTests(unittest.TestCase):
    def run_main(self, typed):
        with mock.patch("builtins.input", return_value=typed):
            with mock.patch("sys.stdout", new_callable=io.StringIO) as out:
                chords.main()
        return out.getvalue()

    def test_known_chord_prints_diagram(self):
        output = self.run_main("G")
        self.assertEqual(output, chords.diagram("G") + "\n")

    def test_spaces_around_name_are_ignored(self):
        output = self.run_main("  Am  ")
        self.assertIn("Chord: Am", output)

    def test_unknown_chord(self):
        self.assertEqual(self.run_main("H7"), "Chord not found.\n")

    def test_name_is_case_sensitive(self):
        self.assertEqual(self.run_main("am"), "Chord not found.\n")


if __name__ == "__main__":
    unittest.main()

