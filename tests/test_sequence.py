"""Sanity checks: no provenance gaps or silently mismatched cue durations."""
import json
import unittest
from pathlib import Path

DATA=json.loads((Path(__file__).resolve().parent.parent/'sequence.json').read_text())

class CueContract(unittest.TestCase):
    def test_complete_timeline(self):
        scenes=DATA['scenes']
        self.assertEqual(scenes[0]['start'],0)
        self.assertAlmostEqual(scenes[-1]['end'],DATA['runtime_s'])
        for a,b in zip(scenes,scenes[1:]):
            self.assertAlmostEqual(a['end'],b['start'],places=5)
    def test_source_traceability(self):
        for scene in DATA['scenes']:
            self.assertGreater(scene['end'],scene['start'])
            self.assertGreaterEqual(scene['source_s'],0)
            self.assertTrue(scene['source_claim'])
            self.assertTrue(scene['motif'])
            self.assertTrue(scene['id'])
    def test_source_atlas_dependency_documented(self):
        self.assertTrue((Path(__file__).resolve().parent.parent/'assets/README.md').is_file())

if __name__=='__main__': unittest.main()
