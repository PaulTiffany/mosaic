"""Contract: causal, current-line-only outpainting with protected prior pixels."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent.parent
STORY=json.loads((ROOT/"production/FULL_SONG_STORYBOARD.json").read_text(encoding="utf-8"))
PLAN=json.loads((ROOT/"production/LINE_GENERATION_PLAN.json").read_text(encoding="utf-8"))

class LineByLineGeneration(unittest.TestCase):
    def test_line_coverage_and_no_future_context(self):
        jobs=PLAN["generation_jobs"]
        shots=STORY["shots"]
        self.assertEqual(len(jobs),106)
        self.assertEqual(len(shots),106)
        self.assertTrue(PLAN["no_lookahead"])
        self.assertTrue(PLAN["no_past_lyric_text"])
        self.assertEqual(PLAN["status"],"ready-for-review-NOT-generated")
        self.assertEqual(PLAN["director_only_story"],"production/FULL_SONG_STORYBOARD.json")
        self.assertNotIn("future_lyric",PLAN["image_inference_inputs"])
        for i,(job,shot) in enumerate(zip(jobs,shots)):
            with self.subTest(id=job["id"]):
                self.assertEqual(job["id"],shot["id"])
                self.assertEqual(job["lyric"],shot["lyric"])
                self.assertEqual(job["audio_start_s"],shot["start_s"])
                self.assertEqual(job["audio_end_s"],shot["end_s"])
                self.assertEqual(job["target_image"],shot["story_frame"])
                self.assertIn("CURRENT LYRIC: "+shot["lyric"],job["inference_prompt"])
                self.assertIn("DEPICT ONLY THIS NEW BEAT: "+shot["story_frame"],job["inference_prompt"])
                self.assertFalse(job["has_future_context"])
                self.assertTrue(job["output_segment"].endswith(".png"))
                self.assertTrue(job["output_accepted_mural"].endswith(".png"))
                self.assertTrue("NEXT LYRIC:" not in job["inference_prompt"])
                self.assertNotIn("next_id",job)
                self.assertNotIn("successor_transition",job)
                self.assertNotIn("previous_lyric",job)
                if i == 0:
                    self.assertIsNone(job["accepted_prior_segment"])
                    self.assertIsNone(job["locked_context_crop"])
                    self.assertIn("FIRST section",job["inference_prompt"])
                else:
                    self.assertEqual(job["accepted_prior_segment"],jobs[i-1]["output_accepted_mural"])
                    self.assertIn("right-edge crop",job["locked_context_crop"])
                    self.assertIn("LOCKED INPUT:",job["inference_prompt"])
                    self.assertIn("blank masked region on the RIGHT",job["inference_prompt"])

    def test_review_visual_map_exists(self):
        svg=(ROOT/"production/STORYBOARD_MAP.svg").read_text(encoding="utf-8")
        self.assertIn('<svg xmlns=',svg)
        self.assertIn("106 sung lines",svg)
        for shot in STORY["shots"]:
            self.assertIn(shot["id"],svg)

    def test_director_sees_all_lines_but_inference_does_not(self):
        self.assertEqual(len(PLAN["generation_jobs"]),STORY["shot_count"])
        self.assertIn("coming_lyrics",PLAN["director_only_inputs"])
        self.assertNotIn("coming_lyrics",PLAN["image_inference_inputs"])
        self.assertIn("future",PLAN["principle"].lower())
        self.assertTrue(PLAN["invariants"]["entire_art_static"])

if __name__=="__main__":
    unittest.main()
