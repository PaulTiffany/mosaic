"""Verify all 106 sung lines, 12 non-vocal windows and one-way mural sequence."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parent.parent
STORY=json.loads((ROOT/"production/FULL_SONG_STORYBOARD.json").read_text(encoding="utf-8"))
SOURCE=json.loads((ROOT/"production/suno_take1_alignment.json").read_text(encoding="utf-8"))
MANIFEST=json.loads((ROOT/"production/frieze_manifest.json").read_text(encoding="utf-8"))

def letters(s):
    return re.sub(r"[^a-z0-9]","",s.lower())

class StoryboardContract(unittest.TestCase):
    def test_all_sung_lines_have_unique_visual_and_timing(self):
        s=STORY["shots"]
        self.assertEqual(len(s),106)
        self.assertEqual(STORY["shot_count"],106)
        self.assertEqual(s[0]["lyric"],"One little piece")
        self.assertEqual(s[-1]["lyric"],"And the seams still show.")
        last_t,last_u=-1.,-1.
        for i,shot in enumerate(s):
            self.assertEqual(shot["index"],i+1)
            self.assertEqual(shot["id"],"S%03d"%(i+1))
            self.assertTrue(shot["alignment_all_success"])
            self.assertGreater(shot["end_s"],shot["start_s"])
            self.assertGreaterEqual(shot["start_s"],last_t)
            self.assertGreaterEqual(shot["mural_u"],last_u)
            self.assertGreater(len(shot["story_frame"]),40)
            self.assertIn(shot["chapter_id"],[a["id"] for a in MANIFEST["assets"]])
            last_t,last_u=shot["start_s"],shot["mural_u"]
        self.assertEqual(len({x["story_frame"] for x in s}),106)

    def test_suno_lyric_source_replays_verbatim(self):
        observed="".join(re.sub(r"\[[^\]]*\]","",w["word"]) for w in SOURCE["words"])
        expected="".join(s["lyric"] for s in STORY["shots"])
        self.assertEqual(letters(observed),letters(expected))

    def test_gaps_and_song_end(self):
        gaps=STORY["instrumental_windows"]
        self.assertEqual(len(gaps),12)
        self.assertEqual(gaps[0]["start_s"],0)
        self.assertAlmostEqual(gaps[-1]["end_s"],276.56)
        for a in gaps:
            self.assertGreaterEqual(round(a["end_s"]-a["start_s"],3),1.2)
        self.assertAlmostEqual(STORY["shots"][-1]["start_s"],268.252)
        self.assertIn("Camera-only",gaps[-1]["camera_picture"])

    def test_three_chorus_positions_increase(self):
        phrase="More on the shelves, less on the tags"
        x=[s["mural_u"] for s in STORY["shots"] if s["lyric"]==phrase]
        self.assertEqual(len(x),3)
        self.assertLess(x[0],x[1])
        self.assertLess(x[1],x[2])

if __name__=="__main__":
    unittest.main()
