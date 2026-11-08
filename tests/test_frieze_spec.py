"""MOSAIC structural tests: evidence about specs, never claims about final artwork."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
MANIFEST=json.loads((ROOT/"production/frieze_manifest.json").read_text(encoding="utf-8"))
ANCHORS=json.loads((ROOT/"production/take1_word_anchors.json").read_text(encoding="utf-8"))

def load(path):
    spec=importlib.util.spec_from_file_location(path.stem,str(path))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

SCROLL=load(ROOT/"production/preview_side_scroll.py")
ASSEMBLER=load(ROOT/"production/assemble_frieze.py")

class StoryContract(unittest.TestCase):
    def test_one_way_nonoverlapping_story(self):
        plates=MANIFEST["assets"]
        self.assertEqual(len(plates),13)
        self.assertEqual(plates[0]["start_s"],0)
        self.assertAlmostEqual(plates[-1]["end_s"],268.252)
        self.assertEqual(MANIFEST["outro_reveal_s"],[268.252,276.56])
        for i,p in enumerate(plates):
            self.assertEqual(i,p["index"])
            self.assertAlmostEqual(p["uv_left"],i/13)
            self.assertAlmostEqual(p["uv_right"],(i+1)/13)
            self.assertLess(p["start_s"],p["end_s"])
            self.assertGreater(len(p["lyrics"]),0)
            self.assertGreater(len(p["visual"]),80)
            if i: self.assertAlmostEqual(plates[i-1]["end_s"],p["start_s"])

    def test_no_reverse_camera(self):
        last=-1
        for i in range(2770):
            t=i/10
            x=SCROLL.x_for_song_time(t,MANIFEST)
            self.assertGreaterEqual(x+1e-9,last,f"Camera reversed at {t}")
            self.assertLessEqual(x,1)
            last=x
        self.assertAlmostEqual(last,1)

    def test_alignment_derived_events(self):
        beats=ANCHORS["anchors"]
        self.assertGreaterEqual(len(beats),40)
        self.assertEqual(ANCHORS["progress_direction"],"left-to-right; u never decreases")
        last_t,last_u=-1,-1
        for a in beats:
            self.assertGreaterEqual(a["song_s"],last_t)
            self.assertGreaterEqual(a["story_u"],last_u)
            self.assertTrue(a["alignment_success"])
            last_t,last_u=a["song_s"],a["story_u"]
        self.assertEqual(beats[0]["phrase"],"One little piece")
        self.assertEqual(beats[-1]["phrase"],"And the seams still show")

    def test_one_static_art_plane_size(self):
        p=MANIFEST["layout"]["segment_px"]
        master=MANIFEST["layout"]["master_px"]
        self.assertEqual(master["width"],len(MANIFEST["assets"])*p["width"])
        self.assertEqual(master["height"],p["height"])
        self.assertEqual(MANIFEST["layout"]["physical_m"],{"width":39,"height":2})

    def test_repeated_chorus_occupies_new_x(self):
        chorus=[b for b in ANCHORS["anchors"] if b["phrase"]=="More on the shelves less on the tags"]
        self.assertEqual(len(chorus),3)
        self.assertLess(chorus[0]["story_u"],chorus[1]["story_u"])
        self.assertLess(chorus[1]["story_u"],chorus[2]["story_u"])

class ImageAssemblyContract(unittest.TestCase):
    def test_missing_and_wrong_dimensions_fail(self):
        from PIL import Image
        tiny={"layout":{"segment_px":{"width":20,"height":12},
                        "master_px":{"width":40,"height":12}},
              "assets":[{"id":"first","file":"assets/incoming/00.png"},
                        {"id":"next","file":"assets/incoming/01.png"}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"assets/incoming").mkdir(parents=True)
            with self.assertRaises(FileNotFoundError):
                ASSEMBLER.check(tiny,root)
            Image.new("RGB",(18,12),(24,61,82)).save(root/"assets/incoming/00.png")
            Image.new("RGB",(20,12),(200,150,90)).save(root/"assets/incoming/01.png")
            with self.assertRaises(ValueError):
                ASSEMBLER.check(tiny,root)

    def test_same_source_image_cannot_fake_new_chorus(self):
        from PIL import Image
        tiny={"layout":{"segment_px":{"width":20,"height":12},"master_px":{"width":40,"height":12}},
              "assets":[{"id":"first","file":"assets/incoming/00.png"},
                        {"id":"next","file":"assets/incoming/01.png"}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"assets/incoming").mkdir(parents=True)
            for idx in range(2):
                Image.new("RGB",(20,12),(100,100,100)).save(root/f"assets/incoming/0{idx}.png")
            with self.assertRaises(ValueError):
                ASSEMBLER.check(tiny,root)

    def test_one_immutable_master_and_hash_receipt(self):
        from PIL import Image
        tiny={"layout":{"segment_px":{"width":20,"height":12},"master_px":{"width":40,"height":12}},
              "assets":[{"id":"first","file":"assets/incoming/00.png"},
                        {"id":"next","file":"assets/incoming/01.png"}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"assets/incoming").mkdir(parents=True)
            Image.new("RGB",(20,12),(24,61,82)).save(root/"assets/incoming/00.png")
            Image.new("RGB",(20,12),(200,150,90)).save(root/"assets/incoming/01.png")
            records=ASSEMBLER.check(tiny,root)
            target=root/"master.png"
            receipt=ASSEMBLER.build(tiny,records,target,root/"seams.jpg")
            with Image.open(target) as img:
                self.assertEqual(img.size,(40,12))
                self.assertEqual(img.getpixel((1,1)),(24,61,82))
                self.assertEqual(img.getpixel((21,1)),(200,150,90))
            self.assertTrue((root/"seams.jpg").is_file())
            self.assertEqual(receipt["master_sha256"],ASSEMBLER.digest(target))

if __name__=="__main__":
    unittest.main()
