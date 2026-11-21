# Beginner / returning player tips Short (3 pages x 4 tips). Facts: wow.gg leveling guides, Blizzard Nov 9 hotfixes, Blizzard class deep dives, Method.gg
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import make_clip as M, make_guide_shorts as G
style = 'frost'; th = M.THEMES[style]; M._SHADOW[0] = th.get('shadow', True)
P = [
 (('NEW OR RETURNING?', 'THE BASICS'), [('Zones don\'t scale to you', 'Elites can hit far harder than they look'),
   ('Log out in an inn or city', 'Rested XP speeds up your next session'),
   ('Grab every flight path', 'It saves hours of running'),
   ('Stuck? Switch zones', 'Same level range, fresh quests')]),
 (('WOW: FOREVER TIPS', 'LEVEL FASTER'), [('Run dungeons', 'Blizzard raised dungeon XP by 50%'),
   ('Group up for elite quests', 'Many quest items now drop for the party'),
   ('Casters: get a wand early', 'Damage without spending mana'),
   ('Grab dungeon quests first', 'Pick them up before you go in')]),
 (('TALENTS AND', 'ENDGAME'), [('Talents start at level 10', 'One point every level after'),
   ('Big talents: 20, 25, 30, 40', 'Plan your build around them'),
   ('Two specs from level 40', 'Leveling spec plus a dungeon spec'),
   ('Raids unlock December 9', 'Start your Onyxia attunement now')]),
]
pages = []
for i, (title, tips) in enumerate(P):
    t0, t1 = i * 12.0, (i + 1) * 12.0
    rows = [G.row_card(th, a, None, sub=b, h=140) for a, b in tips]
    pages.append(G.page(th, title, rows, t0, t1, label='TIPS ' + ['1-4', '5-8', '9-12'][i], footer=None))
G.render('tips_beginners_returning', pages, style, os.path.dirname(os.path.abspath(__file__)) + '/..', 36.0)
