# Quest-window versions of the Shorts in batch_nov23.py (same facts, new look).
# Output: shorts/quest/<name>.mp4, music reused from shorts/<name>.mp4.
# usage: python3 specs/quest_batch.py name [name ...]
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import make_quest_short as Q
spec = importlib.util.spec_from_file_location('batch', os.path.join(HERE, 'batch_nov23.py'))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)

SMALL = {'by', 'for', 'of', 'the', 'to', 'in', 'and', 'a', 'on'}
def nice(s):
    w = s.lower().split()
    return ' '.join(x if (i and x in SMALL) else ('WoW' if x.startswith('wow') else x[:1].upper() + x[1:]) for i, x in enumerate(w))

TITLE_FIX = {'WOW: FOREVER ECONOMY RULES': 'Economy Rules', 'GOLD FARMS BLIZZARD KILLED': 'Gold Farms Blizzard Killed',
             'AUCTION HOUSE TIPS': 'Auction House Tips', 'FIRST AID IS AMAZING NOW': 'First Aid Is Amazing Now'}
def page_name(t1, t2):
    key = f'{t1} {t2}'.upper()
    if key in TITLE_FIX: return TITLE_FIX[key]
    if t1 == t2: return nice(t2)
    if t2.split()[0].lower() in ('for', 'by', 'in') or t1.split()[-1].lower() in SMALL:
        return nice(f'{t1} {t2}')
    return f'{nice(t1)}: {nice(t2)}'

# Noon news clips (from specs/clipN_*.json), one quest page each
NEWS = {
 'clip2_onyxia_attunement': ('Onyxia Attunement', 'How to get attuned', [
     ('Everyone needs it', None, 'The Drakefire Amulet in your bags'),
     ('Alliance start', None, '"Dragonkin Menace", Burning Steppes'),
     ('Horde start', None, '"Blood and Thunder", Kargath'),
     ('Both chains end', None, 'At General Drakkisath in Upper Blackrock Spire')],
     'Start now. Raids unlock December 9.'),
 'clip3_world_first_52_hours': ('World First 60', 'Took 52 hours', [
     ('5-player group', None, '3 mages, a paladin and a shaman'),
     ('EU Normal ruleset', None, 'WoW: Forever'),
     ('Source', None, 'Icy Veins')],
     'What level are you right now? Tell us in the comments.'),
 'clip5_hyjal_summit': ('Hyjal Summit', 'December 9', [
     ('20 players', None, 'Level 60 raid'),
     ('13 bosses', None, 'Starts with an ancient guardian'),
     ('Multiple paths', None, 'Across Mount Hyjal to Nordrassil')],
     'Are you ready for December 9?'),
 'clip6_barrow_deeps': ('Barrow Deeps', "Illidan's prison", [
     ('10 players', None, 'Level 60 raid, 8 bosses'),
     ('10,000 years', None, 'The prison that held Illidan'),
     ('3 entrances', None, 'Mount Hyjal, Winterspring, Blackmaw Hold')],
     "Who's bringing the 10?"),
 'clip7_whats_new': ('New in WoW: Forever', 'Original Azeroth, reimagined', [
     ('Skyborne', None, 'New playable race, Zephras Isle'),
     ('Darkspear Islands', None, 'New 15v15 battleground'),
     ('3 raids on December 9', None, 'Onyxia, Hyjal Summit, Barrow Deeps')],
     'What are you most excited for?'),
 'clip8_countdown_10': ('Raid Countdown', '10 days until raids', [
     ("Onyxia's Lair", '40', 'Players'),
     ('Hyjal Summit', '20', 'Players'),
     ('Barrow Deeps', '10', 'Players')],
     'Got your Drakefire Amulet yet?'),
}

def build(name):
    out_dir = os.path.join(ROOT, 'shorts', 'quest'); os.makedirs(out_dir, exist_ok=True)
    if name in NEWS:
        pname, label, rows, obj = NEWS[name]
        return Q.render(name, [(pname, label, rows)], os.path.join(out_dir, name + '.mp4'),
                        audio_from=os.path.join(ROOT, name + '.mp4'), objective=obj)
    return _build_guide(name)

def _build_guide(name):
    _, P = B.S[name]
    pages = [(page_name(t1, t2), label, rows) for t1, t2, label, rows in P]
    out_dir = os.path.join(ROOT, 'shorts', 'quest'); os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(ROOT, 'shorts', name + ('_v2' if name == 'gathering_guide' else '') + '.mp4')
    return Q.render(name, pages, os.path.join(out_dir, name + '.mp4'), audio_from=src)

if __name__ == '__main__':
    for n in sys.argv[1:]: print(build(n))
