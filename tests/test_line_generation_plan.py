"""Contract for one controlled still-image generation per actually sung lyric."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent.parent
STORY=json.loads((ROOT/"production/FULL_SONG_STORYBOARD.json").read_text())
PLAN=json.loads((ROOT/"production/LINE_GENERATION_PLAN.json").read_text())

class LineByLineGeneration(unittest.TestCase):
    def test_full_line_coverage_and_pairwise_chain(self):
        jobs=PLAN["generation_jobs"]
        shots=STORY["shots"]
        self.assertEqual(len(jobs),106)
        self.assertEqual(len(shots),106)
        self.assertTrue(PLAN["creative_constraints"]["per_line_generation"])
        self.assertEqual(PLAN["status"],"ready-for-human-review-NOT-generated")
        for i,(job,shot) in enumerate(zip(jobs,shots)):
            with self.subTest(id=job["id"]):
                self.assertEqual(job["id"],shot["id"])
                self.assertEqual(job["lyrics"],shot["lyric"])
                self.assertEqual(job["song_start_s"],shot["start_s"])
                self.assertEqual(job["planned_static_image"],shot["story_frame"])
                self.assertEqual(job["previous_id"], jobs[i-1]["id"] if i else None)
                self.assertEqual(job["next_id"],jobs[i+1]["id"] if i<len(jobs)-1 else None)
                self.assertIn(shot["lyric"],job["prompt"])
                self.assertIn(shot["story_frame"],job["prompt"])
                self.assertIn("OUTPAINTING",job["prompt"])
                self.assertTrue(job["asset_path"].endswith(".png"))
                if i:
                    self.assertIn(shots[i-1]["lyric"],job["prompt"])
                if i<len(jobs)-1:
                    self.assertIn(shots[i+1]["lyric"],job["prompt"])

    def test_review_visual_map_exists(self):
        svg=(ROOT/"production/STORYBOARD_MAP.svg").read_text(encoding="utf-8")
        self.assertIn('<svg xmlns=',svg)
        self.assertIn('106 sung lines',svg)
        for shot in STORY["shots"]:
            self.assertIn(shot["id"],svg)

    def test_no_chapter_as_individual_generation_unit(self):
        self.assertEqual(len(PLAN["generation_jobs"]),STORY["shot_count"])
        self.assertIn("storage/render groups",PLAN["source_of_truth"])
        self.assertIn("outpaint",PLAN["creative_constraints"]["seam_protection"].lower())

if __name__=="__main__":
    unittest.main()
