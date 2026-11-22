# 14 Shorts for Nov 23-29 (gold guide + 13 more). 12 s per page, up to 4 rows per page.
# Facts: Blizzard news (Legacy System, Skyborne, new dungeons), conquestcapped.com gold guide (Oct 21 / Nov 13 data),
# gamertagmythras.com gold guide (Nov hotfixes), warcrafttavern.com camping guide, icy-veins.com First Aid recipes,
# wowhead.com dungeon list, games.gg / icy-veins professions overviews.
# usage: python3 specs/batch_nov23.py [only_name]
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import make_clip as M, make_guide_shorts as G

# name: (style, [ (title1, title2, label, [ (left, right_pill_or_None, sub_or_None), ... ]), ... ])
S = {
 'gold_guide': ('parchment', [
   ('FASTEST WAY TO', 'MAKE GOLD', 'START HERE', [
     ('Skin everything you kill', None, 'Skinning + Herbalism is the cheapest start'),
     ('Sell raw materials', None, 'Crafters buy cloth, ore, herbs and leather'),
     ('Keep every Waylaid Crate', None, 'Fill it for Favor, or sell it'),
     ('Keep questing past 48', None, 'Most quests from level 48 now give gold')]),
   ('GOLD GUIDE', 'SELL SMART', 'AUCTION HOUSE', [
     ('Check the vendor price first', None, 'Never list below what a vendor pays'),
     ('Undercut by a little', None, 'Big undercuts get bought and relisted'),
     ('Hold Scarce materials', None, 'Sell common mats early, keep the rare ones'),
     ('Sell bags and wands to players', None, 'Vendors pay almost nothing for them')]),
   ('GOLD GUIDE', 'DON\'T DO THIS', 'AVOID', [
     ('Never buy gold', None, 'It can trigger a Temporary Economy Hold'),
     ('Skip crafting for vendors', None, 'Blizzard cut vendor prices for crafted gear'),
     ('Mage AoE farms were nerfed', None, 'Cone of Cold and Blizzard got weaker'),
     ('Keep gold on a bank alt', None, 'No misclicks on your main')]),
 ]),
 'mount_costs': ('dusk', [
   ('HOW MUCH IS', 'YOUR MOUNT?', 'RIDING TRAINING', [
     ('Apprentice Riding', '100g', 'Level 40, your first mount included'),
     ('At Honored', '90g', 'With your home faction'),
     ('Journeyman Riding', '1,000g', 'Level 60 (900g at Honored)'),
     ('Extra mount colours', '20g', 'Each (18g at Honored)')]),
   ('MOUNT TIPS', 'SAVE UP', 'GOOD TO KNOW', [
     ('Paladins and Warlocks', None, 'Level 40 mount is free from class quests'),
     ('Bartering perk', None, 'Cuts vendor mount prices, not training'),
     ('No flying mounts', None, 'Ground mounts only in WoW: Forever'),
     ('Keep leveling', None, 'Usually pays for it faster than farming')]),
 ]),
 'waylaid_crates': ('ember', [
   ('WAYLAID CRATES', 'EXPLAINED', 'FREE FAVOR', [
     ('Drop from world mobs', None, 'Keep every one you loot'),
     ('Fill with one material bundle', None, 'For example 20 Copper Ore'),
     ('Crafted fills pay double', None, 'Apprentice 5 or 10, Expert 15 or 30 Favor'),
     ('Spend Favor on rewards', None, 'Reins of the Pack Kodo: 6,000 Favor')]),
   ('WAYLAID CRATES', 'TURN-INS', 'WHERE TO GO', [
     ('Alliance', None, 'Marcy Baker, Redridge Mountains'),
     ('Horde', None, 'Dokimi, outside the Crossroads'),
     ('Don\'t want to fill it?', None, 'Unfilled crates sell on the Auction House'),
     ('Performance perk', None, 'Chance for extra Merchant\'s Favor')]),
 ]),
 'alcaz_secret': ('fel', [
   ('SECRET 25 GOLD', 'IN WESTFALL', 'HIDDEN TRUNK', [
     ('Go to the Moonbrook inn', '43.4, 67.8', 'Westfall'),
     ('Check the loose floorboards', None, 'Connery\'s Trunk is hidden there'),
     ('Loot the Document Box', None, 'From the Alcaz Prison quest chain'),
     ('Vendor it or quest it', '25g', 'Or trade it toward a toy')]),
   ('ALCAZ PRISON', 'THE REST', 'LEVELS 48-53', [
     ('Dungeon on Alcaz Island', None, 'Dustwallow Marsh'),
     ('Chain starts with Mason Connery', None, 'Skip The Questioner at first'),
     ('Turn in "State Secrets"', None, 'Old Town (Alliance), Booty Bay (Horde)'),
     ('6 Fractured Insignias', None, 'Make the Alcaz Operative Insignia toy')]),
 ]),
 'economy_rules': ('arcane', [
   ('WOW: FOREVER', 'ECONOMY RULES', 'KNOW THESE', [
     ('No WoW Token', None, 'Gold can\'t be bought from Blizzard'),
     ('No GDKP raids', None, 'Gold-bid loot runs aren\'t allowed'),
     ('Gold buying is risky', None, 'Can freeze trade, mail and Auction House'),
     ('Paying for a carry?', None, 'Pay the player doing the carry directly')]),
 ]),
 'economy_nerfs': ('frost', [
   ('GOLD FARMS', 'BLIZZARD KILLED', 'DON\'T BOTHER', [
     ('Crafted wands to vendors', '1c', 'Sell them to players instead'),
     ('Crafted gear to vendors', None, 'Weapons, armor and bars cut 20-75%'),
     ('Mage AoE dungeon farms', None, 'Cone of Cold and Blizzard weakened'),
     ('Black Lotus prices', None, 'A vendor now sells it at a fixed price')]),
 ]),
 'first_aid': ('frost', [
   ('FIRST AID IS', 'AMAZING NOW', 'HEALING POTIONS', [
     ('Potions moved from Alchemy', None, 'Every character can make them'),
     ('Minor Healing Potion', '55', 'First Aid skill'),
     ('Lesser Healing Potion', '85', 'First Aid skill'),
     ('Healing Potion', '135', 'First Aid skill')]),
   ('FIRST AID', 'LATER RANKS', 'FROM MANUALS', [
     ('Greater Healing Potion', '155', 'Manual: Greater Healing Potion'),
     ('Superior Healing Potion', '215', 'Manual: Superior Healing Potion'),
     ('Major Healing Potion', '275', 'Manual: Major Healing Potion'),
     ('Uses no profession slot', None, 'Pair it with Herbalism for the herbs')]),
 ]),
 'gold_professions': ('ember', [
   ('BEST PROFESSIONS', 'FOR GOLD', 'PICK ONE', [
     ('Skinning + Herbalism', None, 'Cheapest start for a leveling main'),
     ('Herbalism + Alchemy', None, 'Feed your own crafting'),
     ('Skinning + Leatherworking', None, 'Every beast you kill is leather'),
     ('Gather on main, craft on alts', None, 'Most gold over time')]),
 ]),
 'camping': ('dusk', [
   ('CAMPING', 'EXPLAINED', 'THE BASICS', [
     ('Learn Cooking first', None, 'You need it to light the campfire'),
     ('Fire lasts about 10 minutes', None, 'New one every 5 minutes'),
     ('3, 5 or 10 feature slots', None, 'Depends on the campfire tier'),
     ('/sit for 1 minute', None, 'That\'s how you get the buffs')]),
   ('CAMPING', 'BEST FEATURES', 'WHAT TO PLACE', [
     ('Leatherworking Camp Tent', None, 'More experience for everyone nearby'),
     ('Engineering Repair Bot', None, 'A repair vendor out in the world'),
     ('Cozy Sleeping Bag', None, 'Well-Rested buff stacks with camp buffs'),
     ('One object per character', None, 'On a 1-hour cooldown')]),
 ]),
 'legacy_system': ('arcane', [
   ('LEGACY SYSTEM', 'EXPLAINED', 'HOW IT WORKS', [
     ('First point around level 25', None, 'Open it with the Y key'),
     ('65 Legacy Challenges', None, 'Each one gives 1 account-wide point'),
     ('Three perk trees', None, 'Professions, Adventure, Resourcefulness'),
     ('16 points per character', None, 'Each character spends them separately')]),
   ('LEGACY', 'BEST PERKS', 'GRAB THESE', [
     ('Well Rested', None, 'Faster rested XP'),
     ('Frequent Flier', None, 'Cheaper, faster flights'),
     ('Bountiful Harvest', None, 'More Scarce gathering finds'),
     ('Reins of the Spectral Bear', None, 'Legacy-only mount reward')]),
 ]),
 'skyborne': ('frost', [
   ('MEET THE', 'SKYBORNE', 'NEW PLAYABLE RACE', [
     ('Start on Zephras Isle', '1-12', 'A brand new starting zone'),
     ('Join either faction', None, 'Horde Windshapers or Alliance High Order'),
     ('Their own druid forms', None, 'Made just for the Skyborne'),
     ('Needs a Skyborne Pack', None, 'Not included in a normal subscription')]),
   ('SKYBORNE', 'CLASSES', 'BY FACTION', [
     ('Horde Windshaper', None, 'Druid, Hunter, Rogue, Shaman, Warrior'),
     ('Alliance High Order', None, 'Druid, Hunter, Mage, Rogue, Warrior'),
     ('Six classes in total', None, 'Five on each faction'),
     ('No flying, even as a druid', None, 'There are no flying mounts')]),
 ]),
 'new_dungeons': ('fel', [
   ('NEW DUNGEONS', 'BY LEVEL', 'LEVELS 13-33', [
     ('Hall of Thanes', '13-18', 'Beneath Ironforge'),
     ('Ruins of Lordaeron', '15-20', 'Tirisfal Glades'),
     ('Excavation Site', '24-29', 'Wetlands'),
     ('City of Dalaran', '28-33', 'Eastern Kingdoms')]),
   ('NEW DUNGEONS', 'BY LEVEL', 'LEVELS 40-60', [
     ('Krol\'dok Stronghold', '40-45', 'The Riverglades'),
     ('Alcaz Prison', '48-53', 'Dustwallow Marsh'),
     ('Blackmaw Hold', '55-60', 'Azshara'),
     ('Shaper\'s Terrace', '58-60', 'Un\'Goro Crater')]),
 ]),
 'ah_tips': ('parchment', [
   ('AUCTION HOUSE', 'TIPS', 'SELL MORE', [
     ('Compare with vendor price', None, 'Some items pay more at a vendor'),
     ('Undercut by a little', None, 'Not by half: you just lose gold'),
     ('Don\'t trust addon prices', None, 'Reagent vendor prices can be wrong'),
     ('Park a bank alt', None, 'Level 1 alt by the Auction House and mail')]),
 ]),
 'legacy_gold_perks': ('ember', [
   ('LEGACY PERKS', 'FOR GOLD', 'SAVE AND EARN', [
     ('Bountiful Harvest', None, 'More Scarce mats from gathering'),
     ('Bartering', None, 'Lower vendor prices'),
     ('Performance', None, 'Chance for extra Merchant\'s Favor'),
     ('Reagent Economy', None, 'Some spells need no bought reagents')]),
 ]),
}

# Gathering guide (Nov 22): timesaver.gg Forever Mining/Herbalism routes (Nov 9 data), rankedboost.com ranks,
# warcraft.wiki.gg Forever skinning formula, leprestore.com (Mining Pick), skycoach.gg (Herbalism needs no tool).
S['gathering_guide'] = ('dusk', [
   ('GATHERING', 'PROFESSIONS', 'WHAT YOU NEED', [
     ('Mining', None, 'A Mining Pick in your bags'),
     ('Herbalism', None, 'No tool needed, just pick'),
     ('Skinning', None, 'A Skinning Knife in your bags'),
     ('Train up at the trainer', '75 / 150 / 225', 'Journeyman, Expert, Artisan')]),
   ('MINING', 'ORE BY SKILL', 'WHERE TO MINE', [
     ('Copper', '1', 'Westfall, Loch Modan / Durotar, Silverpine'),
     ('Tin', '65', 'Wetlands, Duskwood, Loch Modan'),
     ('Iron', '125', 'Arathi, Alterac, Stranglethorn'),
     ('Mithril', '175', 'Badlands, The Hinterlands'),
     ('Truesilver', '230', 'Badlands, The Hinterlands'),
     ('Thorium', '245', 'Winterspring, Blasted Lands')]),
   ('HERBALISM', 'HERBS BY SKILL', 'WHERE TO PICK', [
     ('Peacebloom, Silverleaf', '1', 'Any starting zone'),
     ('Mageroyal', '50', 'Westfall, Darkshore / The Barrens'),
     ('Bruiseweed', '100', 'Stonetalon, Hillsbrad, Wetlands'),
     ('Liferoot', '150', 'Stranglethorn, Wetlands, Arathi'),
     ('Sungrass', '230', 'The Hinterlands, Feralas, Azshara'),
     ('Dreamfoil', '270', 'Un\'Goro, Eastern Plaguelands')]),
   ('SKINNING', 'SKILL NEEDED', 'BY BEAST LEVEL', [
     ('Level 1-10 beasts', '1', 'Skin anything in starting zones'),
     ('Level 20 beasts', '100', 'Levels 11-20: (level - 10) x 10'),
     ('Level 21+ beasts', 'LVL x 5', 'A level 30 beast needs 150'),
     ('Level 60 beasts', '300', 'Skin where you quest')]),
   # trainers teaching all ranks to 300: timesaver.gg (Mining, Herbalism), wow-professions.com (Skinning)
   ('TRAINERS', 'ALLIANCE', 'ALL RANKS UP TO 300', [
     ('Mining: Stormwind / Ironforge', None, 'Gelman Stonehand / Geofram Bouldertoe'),
     ('Mining: Darkshore', None, 'Kurdram Stonehammer'),
     ('Herbalism: Stormwind / Ironforge', None, 'Tel\'Athir / Reyna Stonebranch'),
     ('Herbalism: Darnassus', None, 'Firodren Mooncaller'),
     ('Skinning: Stormwind / Ironforge', None, 'Maris Granger / Balthus Stoneflayer'),
     ('Skinning: Darnassus', None, 'Eladriel, Craftsmen\'s Terrace')]),
   ('TRAINERS', 'HORDE', 'ALL RANKS UP TO 300', [
     ('Mining: Orgrimmar', None, 'Makaru'),
     ('Mining: Thunder Bluff / Undercity', None, 'Brek Stonehoof / Brom Killian'),
     ('Herbalism: Orgrimmar', None, 'Jandi'),
     ('Herbalism: Thunder Bluff / Undercity', None, 'Komin Winterhoof / Martha Alliestar'),
     ('Skinning: Orgrimmar', None, 'Thuwd, The Drag'),
     ('Skinning: Thunder Bluff / Undercity', None, 'Mooranta / Killian Hagey')]),
])

def build(name):
    style, P = S[name]; th = M.THEMES[style]; M._SHADOW[0] = th.get('shadow', True)
    pages = []
    for i, (t1, t2, label, rows) in enumerate(P):
        hh = 140 if len(rows) <= 4 else 118
        cards = [G.row_card(th, a, r, sub=b, h=hh) for a, r, b in rows]
        pages.append(G.page(th, (t1, t2), cards, i * 12.0, (i + 1) * 12.0, label=label, footer=None))
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shorts')
    return G.render(name, pages, style, out_dir, 12.0 * len(P))

if __name__ == '__main__':
    only = sys.argv[1:] or list(S)
    for n in only: build(n)
