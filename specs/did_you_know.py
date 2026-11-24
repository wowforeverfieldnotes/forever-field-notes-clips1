# "Did you know?" WoW: Forever secrets Short, quest-window style, 6 pages x 12 s = 72 s.
# Sources: Icy Veins (12,594 hidden items, encryption keys, missing mounts; Cozy Sleeping Bag + unsolved secret),
# Mobalytics "Biggest secrets" (Coldflame Saber, First Mate Band, Fang set / snake form), Kami-labs (wands scale
# with spell power, Blizzard forums), TechRadar (Greenfield: thousands of secrets off during beta),
# guided.news / expcarry (Ashbringer + Scarlet Enclave confirmed, podcast ep. 7), Warcraft Tavern (Taldramir legendary),
# YouTube: "10 WoW Forever Secrets Nobody Tells You", "The WoW: Forever Podcast - End of Beta Special".
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import make_quest_short as Q

PAGES = [
 ('Did You Know?', 'Hidden items', [
   ('40% of items are hidden', None, '12,594 of 31,800+ launched without stats'),
   ('Find one and everyone sees it', None, 'Blizzard reveals its stats to all players'),
   ('75 mounts have no entry yet', None, '56 of them are brand new'),
   ('10 encrypted content keys', None, 'Two likely hold Hyjal and Barrow Deeps')]),
 ('Did You Know?', 'Druids can be snakes', [
   ('Collect the Fang set', None, 'Five pieces from Wailing Caverns'),
   ('Become a Viper of the Fang', None, 'A brand new druid form'),
   ('Colour depends on your race', None, "Confirmed by Blizzard's Aidan Moon"),
   ('Prowl to slither', None, 'You slink down along the ground')]),
 ('Did You Know?', 'Battle Mage?', [
   ('Scroll of the Saber', None, 'Found by deciphering mage scrolls'),
   ('Use it on Blade of Silverlaine', None, 'Drops in Shadowfang Keep'),
   ('Coldflame Saber', '+98', 'Fire damage on frozen targets'),
   ('Wands scale with spell power', None, 'No mana cost, real damage')]),
 ('Did You Know?', 'Secret sleeping bag', [
   ('Cozy Sleeping Bag', None, 'A 12-slot bag from a hidden quest chain'),
   ("Starts at Alexston's Farmstead", None, 'Westfall, or Camp Taurajo for Horde'),
   ('Jumping puzzles in 3 zones', None, "Stonetalon, Loch Modan, Thoradin's Wall"),
   ('A new secret starts there', None, 'Still unsolved: look for "Page 155"')]),
 ('Did You Know?', 'Rings and lotus', [
   ('First Mate Band', None, 'A Deadmines ring from Mr. Smite'),
   ('Pair it with its partner ring', None, '"Angry": +50 Strength for 10 seconds'),
   ('Partner ring is level 60', None, 'Where it drops is still a mystery'),
   ('A vendor sells Black Lotus', None, 'At a fixed price, no herbing needed')]),
 ('Did You Know?', 'Still to come', [
   ('Ashbringer is coming', None, "Confirmed by Blizzard's Josh Greenfield"),
   ('Scarlet Enclave returns too', None, 'No date announced yet'),
   ('First legendary revealed', None, 'Taldramir, the Whispering Wood'),
   ('"Thousands" of secrets', None, 'Many were switched off during beta')]),
]

if __name__ == '__main__':
    out = os.path.join(ROOT, 'shorts', 'quest', 'did_you_know_secrets.mp4')
    print(Q.render('did_you_know_secrets', PAGES, out, style='arcane',
                   objective='Which secret did you know? Tell us in the comments.'))
