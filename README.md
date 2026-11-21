# Forever Field Notes clips

Original short clips for the Forever Field Notes fan page (WoW: Forever news and tips).
Fan page, not affiliated with Blizzard Entertainment.

## Making a clip
`python3 tools/make_clip.py specs/NAME.json NAME.mp4` (needs Python 3 with Pillow, and ffmpeg).
Spec: `{"title":[line1,line2], "cards":[[title,subtitle], ... up to 3], "footer":[line, call_to_action], "dur":12}`.
Fonts: Poppins (SIL Open Font License, see tools/assets/Poppins-OFL.txt).
