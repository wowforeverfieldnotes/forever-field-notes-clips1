# Forever Field Notes clips

Original short clips for the Forever Field Notes fan page (WoW: Forever news and tips).
Fan page, not affiliated with Blizzard Entertainment.

## Making a clip
`python3 tools/make_clip.py specs/NAME.json NAME.mp4` (needs Python 3 with Pillow and numpy, and ffmpeg).

Spec: `{"title":[line1,line2], "cards":[[title,subtitle], ... up to 3], "footer":[line, call_to_action], "dur":12,
"style":"dusk|parchment|frost|fel|ember|arcane", "layout":"cards|list|big",
"footage":"footage/file.mp4", "footage_credit":"@creator", "footage_start":0, "footage_audio":false}`

Every clip gets original synthesised music and sound effects (different per style): no licensed audio.
Fonts: Poppins, Lora, Inter (SIL Open Font License).
