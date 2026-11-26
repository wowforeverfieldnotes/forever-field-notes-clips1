# Detailed (dense) versions of the 12 videos scheduled Nov 26-29. Writes specs/quest/<name>.json.
# Sources: Blizzard (Legacy System, Skyborne, raid overview, dungeons, Darkspear Islands, Nov 10 hotfixes),
# Icy Veins First Aid guide, ConquestCapped Auction House guide (Nov 13-16), Warcraft Tavern (Temporary Economy Holds,
# GDKP), Warcraft Wiki (raid boss names), Kami Labs (mage AoE, Black Market), Blizzard forums (wand vendor price).
# usage: python3 specs/detailed_nov26.py && for f in ...; python3 specs/quest_from_json.py specs/quest/<name>.json
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
N = None
V = {
'first_aid': ('frost', 'Which potion are you crafting first? Source: Icy Veins First Aid guide.', [
  ('First Aid', 'Potions for everyone', [
    ('Moved from Alchemy', N, 'In WoW: Forever healing potions are made with First Aid, not Alchemy.'),
    ('No profession slot', N, 'First Aid is a secondary profession, so every character can learn it.'),
    ('Instant in combat', N, 'Potions share a 2-minute cooldown. Bandages still work as before.'),
    ('Pair it with Herbalism', N, 'Every potion needs an herb, a vial and spices.')]),
  ('First Aid', 'Trainer potions', [
    ('Minor Healing Potion', N, 'Skill 1. Heals 70-90. Peacebloom, Empty Vial, Mild Spices.'),
    ('Lesser Healing Potion', N, 'Skill 55. Heals 140-180. Briarthorn, Empty Vial, Mild Spices.'),
    ('Healing Potion', N, 'Skill 110. Heals 280-360. Bruiseweed, Leaded Vial, Hot Spices.')]),
  ('First Aid', 'Potions from manuals', [
    ('Greater Healing Potion', N, 'Skill 155. Heals 455-585. Manual drops from a Syndicate Mercenary in Arathi Highlands.'),
    ('Superior Healing Potion', N, 'Skill 215. Heals 700-900. Learned from its manual.'),
    ('Major Healing Potion', N, 'Skill 275. Heals 1,050-1,750. Manual sold by Pexmit in Mount Hyjal.')]),
  ('First Aid', 'New cures', [
    ('Anti-Venoms', N, 'Remove poisons, usable in combat. From Anti-Venom at 80 up to Powerful Anti-Venom at 300 (Argent Dawn, Honored).'),
    ('Poultices', N, 'Remove diseases, out of combat. Simple Poultice at 90 from the trainer.'),
    ('Tourniquets', N, 'Remove bleeds, out of combat. Woolen Tourniquet at 120 from the trainer.'),
    ('Best bandage', N, 'Heavy Runecloth Bandage: 290 skill to make, heals 2,000 over 8 seconds.')]),
  ('First Aid', 'Ranks up to 300', [
    ('Apprentice and Journeyman', N, 'Any First Aid trainer, up to 75 and 150 skill.'),
    ('Expert (225)', N, 'Buy Expert First Aid - Under Wraps at 125 skill: Deneb Walker, Stromgarde (Alliance) or Balai Lok\'Wein, Brackenwall (Horde).'),
    ('Artisan (300)', N, 'Level 35 and 225 skill. Quest "Triage" in Theramore (Alliance) or Hammerfall (Horde).'),
    ('First Aid Kit (20)', N, 'Campfire item: Stamina buff up to +56 at level 60. Does not stack with Fortitude.')]),
]),
'clip5_hyjal_summit': ('ember', 'Are you ready for December 9? Sources: Blizzard raid overview, Warcraft Wiki, Icy Veins.', [
  ('Hyjal Summit', 'Raid basics', [
    ('Unlocks December 9', N, 'Level 60, together with Barrow Deeps and Onyxia\'s Lair.'),
    ('20 players, 13 bosses', N, 'The biggest of the new raids. Forever raids don\'t scale, so plan for exactly 20 (per Icy Veins).'),
    ('Weekly reset', N, 'All WoW: Forever raids are currently planned to reset weekly.')]),
  ('Hyjal Summit', 'The climb', [
    ('Location', N, 'The summit of Mount Hyjal, near the World Tree Nordrassil.'),
    ('First fight', N, 'The raid opens with a battle against an ancient guardian.'),
    ('Many routes', N, 'Paths cross the mountain through ruins above and below ground.'),
    ('The finale', N, 'Clear the forces threatening Hyjal to open the way to the final encounters.')]),
  ('Hyjal Summit', 'What we know', [
    ('Boss names so far', N, 'Bandalar, Time-Lost Battalion, Old Gloomlurker, Kathris the Haunted, Elder Minderel, Council of Thorns (Warcraft Wiki).'),
    ('Final boss', N, 'Nythus the Dreambound, per Warcraft Wiki.'),
    ('A legendary', N, 'Icy Veins reports Forever\'s first legendary is tied to Hyjal Summit.'),
    ('Legacy point', N, 'Defeat all 13 bosses for 1 account-wide Legacy point.')]),
]),
'economy_rules': ('arcane', 'Sources: Blizzard, Warcraft Tavern, ConquestCapped.', [
  ('Economy Rules', 'No shortcuts', [
    ('No WoW Token', N, 'There is no way to buy gold from Blizzard in WoW: Forever.'),
    ('No GDKP', N, 'Blizzard confirmed at its Sept 17 developer Q&A that gold-bid loot runs aren\'t allowed.'),
    ('Why', N, 'Blizzard says GDKP makes raiding harder to join for new players and pushes people to buy gold.')]),
  ('Economy Rules', 'Buying gold', [
    ('Temporary Economy Holds', N, 'Announced Oct 13. A flagged account loses trade, mail, guild bank and Auction House while Blizzard investigates.'),
    ('Both sides', N, 'Buyers and sellers of illicit gold can both be flagged.'),
    ('If you\'re cleared', N, 'The hold lifts automatically and leaves no permanent strike.'),
    ('If it\'s proven', N, 'Blizzard says it will punish gold buyers aggressively, up to permanent account loss.')]),
  ('Economy Rules', 'How the market works', [
    ('One market per faction', N, 'All three capitals of a faction share one Auction House (per ConquestCapped).'),
    ('Trading across factions', N, 'Only at the neutral houses in Gadgetzan, Booty Bay and Everlook, which take 15% instead of 5%.'),
    ('Price-capped reagents', N, 'Mister Graphed at the Black Market in the Riverglades sells rare reagents like Black Lotus at a fixed price.'),
    ('More quest gold', N, 'Since Nov 10, most quests level 48 and up also reward gold.')]),
]),
'legacy_system': ('parchment', 'Which perk are you taking first? Source: Blizzard.', [
  ('Legacy System', 'How it works', [
    ('Account-wide points', N, '65 Legacy Challenges, 1 point each, shared across your Battle.net account (not Hardcore).'),
    ('When it unlocks', N, 'With your first point, usually level 25. Also 150 in a crafting profession, or exploring the whole map.'),
    ('Open it', N, 'Shield icon on the menu bar, or press Y.'),
    ('16 points per character', N, 'Each character spends its own. One character alone can earn 29, so alts are optional.')]),
  ('Legacy System', 'Earning points', [
    ('Classes (27)', N, 'Reach level 25, 45 and 60 on each class.'),
    ('Tradeskills (18)', N, 'Reach 150, 225 and 300 in each crafting profession.'),
    ('PvP (12)', N, 'Ranks 3, 7, 10, 13 and 14, Exalted with each battleground faction, and Season\'s Journey quests.'),
    ('Dungeons, Raids, Adventure (8)', N, 'Final bosses of each dungeon bracket, Onyxia plus full Hyjal and Barrow Deeps clears, exploring the map, and the Lord Valthalak questline.')]),
  ('Legacy System', 'Three perk trees', [
    ('Professions', N, 'Working Overtime, Bountiful Harvest, Bartering, Performance, Master Chef, Luremaster, Dedicated Study.'),
    ('Adventure', N, 'Well Rested, Thrill of Adventure, High Alert, Field Guide, Field Medicine, Talented, Frequent Flier.'),
    ('Resourcefulness', N, 'Gourmand, The Quick and the Dead, Reinforce, For Great Honor, Permanence, Diplomat, Reagent Economy.')]),
  ('Legacy System', 'Standouts and rewards', [
    ('Talented', N, 'Talent points unlock up to 5 levels earlier.'),
    ('Well Rested', N, 'A bigger rested XP pool that fills faster.'),
    ('Reagent Economy', N, 'Class spells stop needing bought reagents, and tier 1 camp features cost nothing.'),
    ('Rewards', N, 'Replica Ironforge Air Rifle toy, Spectral Bear Cub, Spectral Bear Tabard and the Reins of the Spectral Bear.')]),
]),
'clip6_barrow_deeps': ('fel', "Who's bringing the 10? Sources: Blizzard, Warcraft Wiki.", [
  ('Barrow Deeps', 'Raid basics', [
    ('Unlocks December 9', N, 'Level 60, 10 players, 8 bosses.'),
    ("Illidan's prison", N, 'It held Illidan Stormrage for 10,000 years. Now its passages have been opened.'),
    ('Where', N, 'Hidden beneath Kalimdor, inside Mount Hyjal.'),
    ('Three ways in', N, 'Entrances connect through Mount Hyjal, Winterspring and Blackmaw Hold.')]),
  ('Barrow Deeps', 'What waits inside', [
    ('The story', N, 'Find out what happened to those left behind, and how the wardens plan to contain the danger.'),
    ('Multiple paths', N, 'Method reports several routes and changing themes as you go deeper.'),
    ('Weekly reset', N, 'All WoW: Forever raids are currently planned to reset weekly.'),
    ('Legacy point', N, 'Defeat all 8 bosses for 1 account-wide Legacy point.')]),
  ('Barrow Deeps', 'The bosses', [
    ('First four', N, 'Deepscar Matriarch, Khalith the Dreadspinner, Amethrax, Ravus and Darlissa.'),
    ('Next three', N, 'Elder Tangleclaw, Well of Sorrow, Del\'lynar Songwood.'),
    ('Final boss', N, 'Sonya Darkhallow. Boss names per Warcraft Wiki.')]),
]),
'ah_tips': ('dusk', 'Sources: ConquestCapped Auction House guide (Nov 13-16), Blizzard Nov 10 hotfixes.', [
  ('Auction House Tips', 'How it works', [
    ('One market per faction', N, 'A stack posted in Orgrimmar shows in Thunder Bluff and Undercity at the same moment.'),
    ('5% or 15%', N, 'Faction houses keep 5% of a sale. Neutral houses (Gadgetzan, Booty Bay, Everlook) keep 15%.'),
    ('Deposits', N, 'You only get it back if the item sells. The minimum deposit dropped to 1 copper in the Nov 10 hotfixes.'),
    ('Getting paid', N, 'Buyers get items instantly. Your gold arrives by mail about an hour later.')]),
  ('Auction House Tips', 'Sell smarter', [
    ('Vendor price is your floor', N, 'If the sale after the cut is worth less than the vendor price, just vendor it.'),
    ('Stacks', N, 'Ore, herbs and cloth sell cheapest first. Matching the lowest price puts you in line; undercutting by a copper rarely pays.'),
    ('Gear', N, 'Price where most listings sit, not at the cheapest outlier.'),
    ('Timing', N, 'Post in the evening. Prices tend to be higher before raid nights.')]),
  ('Auction House Tips', 'Watch out', [
    ('Addon prices', N, 'Early tooltip prices swing fast. Check the market yourself before big trades.'),
    ('Flooded markets', N, 'Lesser and Greater Magic Wands were saturated in week one.'),
    ('Steady sellers', N, 'Leather, cloth and leveling potions have held their value.'),
    ('Bank alt', N, 'Park one in the capital closest to the Auction House, bank and mailbox.')]),
]),
'skyborne': ('frost', 'Horde or Alliance Skyborne? Source: Blizzard.', [
  ('Meet the Skyborne', 'Quick facts', [
    ('Who they are', N, 'Elves also called shen\'dorei, the "hidden people".'),
    ('Starting zone', N, 'Zephras Isle, a brand new zone for levels 1-12.'),
    ('Pick a side', N, 'Windshapers join the Horde, the High Order joins the Alliance.'),
    ('How to unlock', N, 'Needs a Skyborne Heroic Pack or higher. Not included in a normal subscription.')]),
  ('Meet the Skyborne', 'Classes', [
    ('Both factions', N, 'Druid, Hunter, Rogue and Warrior.'),
    ('Horde Windshaper', N, 'Can also be a Shaman.'),
    ('Alliance High Order', N, 'Can also be a Mage.'),
    ('Druid forms', N, 'New druid forms made just for the Skyborne.')]),
  ('Meet the Skyborne', 'Racial abilities', [
    ('Walk on Air', N, 'Glide downward through the air for 10 seconds.'),
    ('Wind Blessed', N, 'Passive: +1% melee, ranged and spell Haste.'),
    ('Elemental Insight', N, 'Passive: +5% damage against Elementals.'),
    ('Faction racial', N, 'Horde Skysight: +10% run speed. Alliance Read Ley Line: activate a ley line for +100% health and mana regen.')]),
  ('Meet the Skyborne', 'Their story', [
    ('Origins', N, 'Highborne exiles made a pact with wind spirits and built a civilization in Skywall.'),
    ('Zephras Isle today', N, 'The wind spirits that protected it have vanished, its structures are failing, and the Skyborne are divided.'),
    ('Windshapers', N, 'Descended from the first shen\'dorei given the wind spirits\' gift of skysight.'),
    ('High Order', N, 'Descended from the Highborne scholars of Eldre\'Thalas.')]),
]),
'clip7_whats_new': ('arcane', 'What are you most excited for? Source: Blizzard.', [
  ('New in WoW: Forever', 'The basics', [
    ('Launched Nov 4, 2026', N, 'A permanent version of original Azeroth, level 60. Blizzard: not a mode, a season or a new version of Classic.'),
    ('Every class, both sides', N, 'All nine classes are playable on both factions.'),
    ('Talents and specs', N, 'Talents unlock at level 10. Dual Specialization at level 40.'),
    ('New race', N, 'The Skyborne, starting on Zephras Isle.')]),
  ('New in WoW: Forever', 'New content', [
    ('9 new dungeons', N, 'From Hall of Thanes at level 13 to Shaper\'s Terrace at 58-60.'),
    ('3 raids on December 9', N, 'Onyxia\'s Lair (40), Hyjal Summit (20) and Barrow Deeps (10).'),
    ('Darkspear Islands', N, '15v15 battleground for levels 30-60 off Dustwallow Marsh: four bases, a central flag, first to 2000 points.'),
    ('Legacy System', N, 'Account-wide challenges unlock perks and rewards like the Spectral Bear mount.')]),
  ('New in WoW: Forever', 'Changed systems', [
    ('Healing potions', N, 'Now made with First Aid, so every character can craft them.'),
    ('Camping', N, 'Build campfires and place profession features for group buffs.'),
    ('Waylaid Crates', N, 'Fill them with materials for Merchant\'s Favor rewards.'),
    ('Coming later', N, 'More raids, dungeons, PvP and Hardcore, no dates yet. Scarlet Enclave and Ashbringer are confirmed to return.')]),
]),
'economy_nerfs': ('ember', 'Sources: Blizzard Nov 10 hotfixes, Blizzard forums, ConquestCapped, Kami Labs.', [
  ('Gold Farms Blizzard Killed', 'Vendor shuffles', [
    ('Crafted wands', N, 'Enchanting wands sell to vendors for just 1 copper. Players report the AH is flooded too.'),
    ('Crafted armor', N, 'Nov 10: vendors pay less for some Leatherworking, Tailoring and Blacksmithing armor. Blizzard: they were meant to be crafted once.'),
    ('Iron Grenades', N, 'Vendor price cut to 1 silver 25 copper (was 5 silver). Crafting them to sell now loses gold.'),
    ('Minor Arcane Elixir', N, 'Sells for 5 copper (was 25 copper).')]),
  ('Gold Farms Blizzard Killed', 'And the rest', [
    ('Mage AoE farms', N, 'The Frost slows behind giant AoE pulls were weakened, so classic mage farming is much less profitable (per Kami Labs).'),
    ('Black Lotus', N, 'A Black Market vendor, Mister Graphed in the Riverglades, sells it at a fixed price, capping what it\'s worth.'),
    ('What still works', N, 'Most quests level 48 and up now give gold. Leather, cloth and potions sell steadily (ConquestCapped).'),
    ('Rule of thumb', N, 'Before crafting to vendor, compare the sell price with what the materials cost.')]),
]),
'new_dungeons': ('fel', 'Which one is your favorite so far? Source: Blizzard.', [
  ('New Dungeons', 'Levels 13-29', [
    ('Hall of Thanes (13-18)', N, 'Beneath Ironforge. The tomb of the dwarven kings, invaded by suspected Dark Iron dwarves. Alliance enter from their capital.'),
    ('Ruins of Lordaeron (15-20)', N, 'The ruined city above the Undercity. The Forsaken are retaking it while a necromancer gathers power.'),
    ('Excavation Site (24-29)', N, 'Wetlands, near Thelgen Rock and Dun Algaz. A strange mist and a time-frozen area full of titan constructs.')]),
  ('New Dungeons', 'Levels 28-45', [
    ('City of Dalaran (28-33)', N, 'Alterac Mountains. Needs an attunement: "An Alarming Request" in Southshore or "Key to the City" in Tarren Mill. Enter through the sewers.'),
    ('The Drowned City (35-40)', N, 'Off Stranglethorn, west of Grom\'gol. Dive to find the entrance. Trolls, naga and a storm that builds to the last fight.'),
    ("Krol'dok Stronghold (40-45)", N, 'An ogre fortress in the Riverglades with workshops and camps. Strange chanting after nightfall.')]),
  ('New Dungeons', 'Levels 48-60', [
    ('Alcaz Prison (48-53)', N, 'Alcaz Island, Dustwallow Marsh. Defias and naga at war inside; rumored prisoners include King Varian Wrynn.'),
    ('Blackmaw Hold (55-60)', N, 'Through a long-sealed gate in Azshara. A corrupted furbolg city with multiple routes.'),
    ("Shaper's Terrace (58-60)", N, 'A titan facility in northern Un\'Goro. Bring power crystals from the crater to its consoles.'),
    ('Good to know', N, 'Dungeon enemies give 50% more XP since Nov 9, and final bosses count toward Legacy points.')]),
]),
'clip8_countdown_10': ('dusk', 'Got your Drakefire Amulet yet? Source: Blizzard raid overview.', [
  ('Raid Countdown', '10 days to go', [
    ("Onyxia's Lair (40)", N, 'Dustwallow Marsh. Three phases of heavy fire: build fire resistance and be ready to move.'),
    ('Hyjal Summit (20)', N, '13 bosses on the summit near Nordrassil, starting with an ancient guardian.'),
    ('Barrow Deeps (10)', N, '8 bosses in the prison that held Illidan, with entrances in Hyjal, Winterspring and Blackmaw Hold.'),
    ('Weekly reset', N, 'All three unlock December 9 and are planned to reset weekly.')]),
  ('Raid Countdown', 'Onyxia attunement', [
    ('Everyone needs it', N, 'Every raider must carry the Drakefire Amulet in their bags. It doesn\'t need to be equipped.'),
    ('Alliance', N, '"Dragonkin Menace" (Burning Steppes), The True Masters, rescue Marshal Windsor from Blackrock Depths, The Great Masquerade, The Dragon\'s Eye.'),
    ('Horde', N, '"Blood and Thunder" (Kargath), Rend\'s head, Rexxar in Desolace, Myranda the Hag, Emberstrife and four dragon skulls.'),
    ('Both end the same way', N, 'Take the Blood of the Black Dragon Champion from General Drakkisath in Upper Blackrock Spire.')]),
  ('Raid Countdown', 'Get ready', [
    ('Start now', N, 'Blizzard advises starting early, bringing friends for elite quests, and planning several dungeon runs.'),
    ('Stock potions', N, 'Healing potions are made with First Aid in Forever, so anyone can craft a stack.'),
    ('Legacy points', N, 'Onyxia, a full Hyjal clear and a full Barrow Deeps clear are worth 1 point each.')]),
]),
'legacy_gold_perks': ('parchment', 'Source: Blizzard Legacy System preview.', [
  ('Legacy Perks for Gold', 'Earn more', [
    ('Bountiful Harvest', N, 'Extra Scarce resources from Mining, Herbalism and Skinning. Scarce mats are the ones worth holding.'),
    ('Performance', N, 'Sometimes extra Merchant\'s Favor from the Azeroth Commerce Authority or Durotar Supply and Logistics.'),
    ('Master Chef and Luremaster', N, 'A chance for extra cooking results, and a chance to catch extra fish.'),
    ('Dedicated Study', N, 'A daily cooldown that speeds up skill-ups. With every tradeskill at 300 it gives free Elemental Essences.')]),
  ('Legacy Perks for Gold', 'Spend less', [
    ('Bartering', N, 'Lower prices on items bought from vendors (Blizzard gives no exact amount).'),
    ('Reagent Economy', N, 'Class spells stop needing bought reagents, and tier 1 camp features need no materials.'),
    ('Reinforce', N, 'Less durability lost when you die, so smaller repair bills.'),
    ('Frequent Flier', N, 'Cheaper and faster flight paths.')]),
  ('Legacy Perks for Gold', 'How to spend', [
    ('16 points per character', N, 'Each character picks its own perks, so a gatherer and a crafter can take different trees.'),
    ('Points are account-wide', N, 'Every challenge you finish on any character adds to the pool for all of them.')]),
]),
}
for name, (style, obj, pages) in V.items():
    spec = {'name': name, 'style': style, 'dense': True, 'objective': obj,
            'pages': [[a, b, [list(r) for r in rows]] for a, b, rows in pages]}
    json.dump(spec, open(os.path.join(HERE, 'quest', name + '.json'), 'w'), indent=1, ensure_ascii=False)
    print(name)
