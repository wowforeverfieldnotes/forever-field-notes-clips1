# Render a quest-window Short from a JSON spec.
# usage: python3 specs/quest_from_json.py specs/quest/<name>.json   -> shorts/quest/<name>.mp4
# JSON: {"name": "hotfix_2026_11_24", "style": "frost",
#        "objective": "Full notes on the Blizzard forums.",
#        "pages": [["Hotfixes: Nov 24", "Classes", [["Left text", "right pill or null", "small line or null"], ...]], ...]}
# Max 6 rows per page (4 reads best), 12 s per page, styles: dusk parchment frost fel ember arcane.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import make_quest_short as Q
spec = json.load(open(sys.argv[1]))
pages = [(p[0], p[1], [tuple(r) for r in p[2]]) for p in spec['pages']]
out = os.path.join(ROOT, 'shorts', 'quest', spec['name'] + '.mp4')
print(Q.render(spec['name'], pages, out, style=spec.get('style', 'dusk'),
               objective=spec.get('objective', 'Follow Forever Field Notes for more WoW: Forever news.')))
