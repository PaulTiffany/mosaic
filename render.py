#!/usr/bin/env python3
"""MOSAIC: reproducible, SILENT, source-attributed opening animatic.

This renders an illustrated tile study, not independent character animations.
The original cover is an external input in this branch: assets/cover.png.
"""
import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SEQUENCE = json.loads((ROOT / "sequence.json").read_text(encoding="utf-8"))
GOLD = (215, 181, 103)


def font(size, bold=False):
    choices = [
        ROOT / "assets" / ("Lato-Bold.ttf" if bold else "Lato-Regular.ttf"),
        Path("/usr/share/fonts/truetype/lato/Lato-Bold.ttf" if bold
             else "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in choices:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0*x)


def interpolation(t, points):
    if t <= points[0][0]:
        return np.asarray(points[0][1:], dtype=float)
    if t >= points[-1][0]:
        return np.asarray(points[-1][1:], dtype=float)
    for p, q in zip(points, points[1:]):
        if p[0] <= t <= q[0]:
            z = ease((t - p[0]) / (q[0] - p[0]))
            return (1.0-z)*np.asarray(p[1:]) + z*np.asarray(q[1:])
    return np.asarray(points[-1][1:], dtype=float)


def make_tiles(cover, world_side=840, grid=6):
    rng = np.random.default_rng(1729)
    cover = cv2.resize(cover, (world_side, world_side), interpolation=cv2.INTER_AREA)
    side = world_side // grid
    tiles = []
    for row in range(grid):
        for col in range(grid):
            patch = cover[row*side:(row+1)*side, col*side:(col+1)*side].copy()
            if (row, col) in {(0,0), (0,1)}:
                reveal = -2.0
            elif (row, col) in {(1,0), (1,1)}:
                reveal = 3.0 + row + col
            else:
                reveal = 5.5 + row*5.0 + col*2.2 + float(rng.uniform(-1.5,1.5))
            tiles.append({
                "row": row, "col": col, "patch": patch, "reveal": reveal,
                "dx": float(rng.uniform(-105,105)),
                "dy": float(rng.uniform(-90,90)),
            })
    return tiles


def background(size):
    image = np.full((size,size,3), (22,14,12), dtype=np.uint8)
    rng = np.random.default_rng(31)
    for x,y in rng.integers(0, size, (400,2)):
        val = int(rng.integers(16,48))
        image[y,x] = (val, max(0,val-14), max(0,val-20))
    for i in range(0,size,70):
        cv2.line(image, (i,0),(i,size-1),(26,22,21),1,cv2.LINE_AA)
        cv2.line(image, (0,i),(size-1,i),(26,22,21),1,cv2.LINE_AA)
    return image


def assemble(time_s, tiles, base):
    world = base.copy()
    side = len(world)//6
    for item in tiles:
        age = time_s - item["reveal"]
        if age < -0.02:
            continue
        opacity = ease(age/1.8)
        arrival = ease(age/8.0)
        x = int(round(item["col"]*side + (1-arrival)*item["dx"]))
        y = int(round(item["row"]*side + (1-arrival)*item["dy"]))
        pad = 3
        tile = item["patch"][pad:-pad,pad:-pad]
        px,py = x+pad,y+pad
        h,w = tile.shape[:2]
        x1,y1 = max(0,px),max(0,py)
        x2,y2 = min(len(world),px+w),min(len(world),py+h)
        if x2 <= x1 or y2 <= y1:
            continue
        crop = tile[y1-py:y2-py, x1-px:x2-px]
        destination = world[y1:y2,x1:x2]
        destination[:] = np.clip(destination*(1-opacity)+crop*opacity,0,255).astype(np.uint8)
        light = 60+int(125*min(1.0,opacity))
        cv2.rectangle(world,(x+1,y+1),(x+side-2,y+side-2),
                      (max(20,light-35),light,min(255,light+40)),1,cv2.LINE_AA)
        if 0 <= age <= 1.2:
            cv2.rectangle(world,(x+2,y+2),(x+side-3,y+side-3),
                          (154,210,255),2,cv2.LINE_AA)
    return world


CAMERA = [
    (0.0, .185,.16,2.30),
    (8.984, .28,.23,1.95),
    (22.36, .20,.40,1.90),
    (31.5, .22,.37,1.75),
    (40.008, .45,.35,1.38),
    (48.0, .50,.50,1.06),
    (58.412, .50,.50,1.02),
]


def current_scene(time_s):
    for scene in SEQUENCE["scenes"]:
        if scene["start"] <= time_s < scene["end"]:
            return scene
    return SEQUENCE["scenes"][-1]


def annotate(frame, scene, time_s):
    height,width = frame.shape[:2]
    canvas = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).convert("RGBA")
    overlay = Image.new("RGBA",(width,height),(0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    small = font(max(9,int(width/640*12)))
    label = font(max(10,int(width/640*14)))
    headline = font(max(16,int(width/640*27)),bold=True)
    margin = int(width*.047)
    draw.rounded_rectangle((margin-8,margin-13,margin+245,margin+20),
                           radius=8,fill=(8,17,33,135))
    draw.text((margin,margin-10),"M O S A I C    /    FILM STUDY 01",
              font=label,fill=(241,217,166,235))
    y = int(height*.792)
    draw.rounded_rectangle((margin-12,y-13,width-margin+5,height-margin+8),
                           radius=12,fill=(7,15,29,205))
    draw.line((margin,y-4,margin+86,y-4),fill=(241,188,105,235),width=3)
    caption = scene["caption"]
    if len(caption)>31 and width<680:
        if " / " in caption:
            a,b = caption.split(" / ",1)
        else:
            a,b = caption[:29],caption[29:]
        draw.text((margin,y+7),a,font=headline,fill=(245,238,219,255))
        draw.text((margin,y+39),b,font=headline,fill=(245,238,219,255))
    else:
        draw.text((margin,y+7),caption,font=headline,fill=(245,238,219,255))
    second=int(scene["source_s"])
    draw.text((margin,height-margin-17),
              f"SOURCE  •  ML STREET TALK  •  {second//60:02}:{second%60:02}  /  cB1GNO95iog",
              font=small,fill=(189,204,220,245))
    bar=height-9
    draw.rectangle((0,bar,width,bar+3),fill=(45,53,66,220))
    draw.rectangle((0,bar,int(width*time_s/SEQUENCE["runtime_s"]),bar+3),
                   fill=(236,180,105,240))
    canvas=Image.alpha_composite(canvas,overlay)
    return cv2.cvtColor(np.asarray(canvas.convert("RGB")),cv2.COLOR_RGB2BGR)


def frame_at(time_s, side, tiles, base):
    world = assemble(time_s,tiles,base)
    cx,cy,zoom = interpolation(time_s,CAMERA)
    scale=(side/len(world))*float(zoom)
    matrix=np.float32([[scale,0,side/2-cx*len(world)*scale],
                       [0,scale,side/2-cy*len(world)*scale]])
    canvas=cv2.warpAffine(world,matrix,(side,side),flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT,borderValue=(10,10,17))
    yy,xx=np.ogrid[:side,:side]
    radius=((xx-side/2)/(side*.72))**2 + ((yy-side/2)/(side*.72))**2
    vignette=np.clip(1-.39*radius,.54,1.)
    canvas=(canvas.astype(np.float32)*vignette[:,:,None]).astype(np.uint8)
    return annotate(canvas,current_scene(time_s),time_s)


def render(args):
    cover=cv2.imread(str(args.cover))
    if cover is None:
        raise FileNotFoundError(
            f"Original MOSAIC cover required at {args.cover}. See assets/README.md."
        )
    tiles=make_tiles(cover)
    backdrop=background(840)
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(output),cv2.VideoWriter_fourcc(*"mp4v"),
                           args.fps,(args.size,args.size))
    if not writer.isOpened():
        raise RuntimeError(f"Could not initialize output codec: {output}")
    frames=int(round(args.seconds*args.fps))
    sample_times=[0,4,9,14,22.4,30,40,47]
    samples=[]
    try:
        for i in range(frames):
            t=i/args.fps
            frame=frame_at(t,args.size,tiles,backdrop)
            writer.write(frame)
            if sample_times and t>=sample_times[0]-1e-6:
                samples.append((sample_times.pop(0),
                                cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
    finally:
        writer.release()
    if args.contact_sheet and samples:
        thumb,gap,cols=320,12,4
        rows=math.ceil(len(samples)/cols)
        sheet=Image.new("RGB",(cols*(thumb+gap)+gap,
                               rows*(thumb+gap+27)+gap),(9,14,24))
        draw=ImageDraw.Draw(sheet)
        for i,(t,pixels) in enumerate(samples):
            x=gap+(i%cols)*(thumb+gap)
            y=gap+(i//cols)*(thumb+gap+27)
            sheet.paste(Image.fromarray(pixels).resize(
                (thumb,thumb),Image.Resampling.LANCZOS),(x,y))
            draw.text((x+8,y+thumb+3),f"SONG {t:05.1f}s",
                      font=font(17),fill=(227,204,154))
        contact=Path(args.contact_sheet)
        contact.parent.mkdir(parents=True,exist_ok=True)
        sheet.save(contact)
    print(f"Silent prototype: {output}")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--cover",type=Path,default=ROOT/"assets"/"cover.png")
    parser.add_argument("--seconds",type=float,default=48.0)
    parser.add_argument("--fps",type=int,default=20)
    parser.add_argument("--size",type=int,default=640)
    parser.add_argument("--output",default=str(ROOT/"outputs"/"intro_animatic_silent.mp4"))
    parser.add_argument("--contact-sheet",default=str(ROOT/"outputs"/"contact_sheet.png"))
    render(parser.parse_args())
