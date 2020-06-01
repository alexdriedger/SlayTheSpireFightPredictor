import os
import json
from functools import partial
import pprint

BASE_GAME_RELICS = {'Burning Blood', 'Cracked Core', 'PureWater', 'Ring of the Snake', 'Akabeko', 'Anchor', 'Ancient Tea Set', 'Art of War', 'Bag of Marbles', 'Bag of Preparation', 'Blood Vial', 'TestModSTS:BottledPlaceholderRelic', 'Bronze Scales', 'Centennial Puzzle', 'CeramicFish', 'Damaru', 'DataDisk', 'Dream Catcher', 'Happy Flower', 'Juzu Bracelet', 'Lantern', 'MawBank', 'MealTicket', 'Nunchaku', 'Oddly Smooth Stone', 'Omamori', 'Orichalcum', 'Pen Nib', 'TestModSTS:PlaceholderRelic2', 'Potion Belt', 'PreservedInsect', 'Red Skull', 'Regal Pillow', 'TestModSTS:DefaultClickableRelic', 'Smiling Mask', 'Snake Skull', 'Strawberry', 'Boot', 'Tiny Chest', 'Toy Ornithopter', 'Vajra', 'War Paint', 'Whetstone', 'Blue Candle', 'Bottled Flame', 'Bottled Lightning', 'Bottled Tornado', 'Darkstone Periapt', 'Yang', 'Eternal Feather', 'Frozen Egg 2', 'Cables', 'Gremlin Horn', 'HornCleat', 'InkBottle', 'Kunai', 'Letter Opener', 'Matryoshka', 'Meat on the Bone', 'Mercury Hourglass', 'Molten Egg 2', 'Mummified Hand', 'Ninja Scroll', 'Ornamental Fan', 'Pantograph', 'Paper Crane', 'Paper Frog', 'Pear', 'Question Card', 'Self Forming Clay', 'Shuriken', 'Singing Bowl', 'StrikeDummy', 'Sundial', 'Symbiotic Virus', 'TeardropLocket', 'The Courier', 'Toxic Egg 2', 'White Beast Statue', 'Bird Faced Urn', 'Calipers', 'CaptainsWheel', 'Champion Belt', 'Charon\'s Ashes', 'CloakClasp', 'Dead Branch', 'Du-Vu Doll', 'Emotion Chip', 'FossilizedHelix', 'Gambling Chip', 'Ginger', 'Girya', 'GoldenEye', 'Ice Cream', 'Incense Burner', 'Lizard Tail', 'Magic Flower', 'Mango', 'Old Coin', 'Peace Pipe', 'Pocketwatch', 'Prayer Wheel', 'Shovel', 'StoneCalendar', 'The Specimen', 'Thread and Needle', 'Tingsha', 'Torii', 'Tough Bandages', 'TungstenRod', 'Turnip', 'Unceasing Top', 'WingedGreaves', 'Astrolabe', 'Black Blood', 'Black Star', 'Busted Crown', 'Calling Bell', 'Coffee Dripper', 'Cursed Key', 'Ectoplasm', 'Empty Cage', 'FrozenCore', 'Fusion Hammer', 'HolyWater', 'HoveringKite', 'Inserter', 'Mark of Pain', 'Nuclear Battery', 'Pandora\'s Box', 'Philosopher\'s Stone', 'Ring of the Serpent', 'Runic Cube', 'Runic Dome', 'Runic Pyramid', 'SacredBark', 'SlaversCollar', 'Snecko Eye', 'Sozu', 'Tiny House', 'Velvet Choker', 'VioletLotus', 'WristBlade', 'Bloody Idol', 'CultistMask', 'Enchiridion', 'FaceOfCleric', 'Golden Idol', 'GremlinMask', 'Mark of the Bloom', 'MutagenicStrength', 'Nloth\'s Gift', 'NlothsMask', 'Necronomicon', 'NeowsBlessing', 'Nilry\'s Codex', 'Odd Mushroom', 'Red Mask', 'Spirit Poop', 'SsserpentHead', 'WarpedTongs', 'Brimstone', 'Cauldron', 'Chemical X', 'ClockworkSouvenir', 'DollysMirror', 'Frozen Eye', 'HandDrill', 'Lee\'s Waffle', 'Medical Kit', 'Melange', 'Membership Card', 'OrangePellets', 'Orrery', 'PrismaticShard', 'Runic Capacitor', 'Sling', 'Strange Spoon', 'TheAbacus', 'Toolbox', 'TwistedFunnel'}
BASE_GAME_POTIONS = {'BloodPotion', 'Poison Potion', 'FocusPotion', 'BottledMiracle', 'Block Potion', 'Dexterity Potion', 'Energy Potion', 'Explosive Potion', 'Fire Potion', 'Strength Potion', 'Swift Potion', 'Weak Potion', 'FearPotion', 'AttackPotion', 'SkillPotion', 'PowerPotion', 'ColorlessPotion', 'SteroidPotion', 'SpeedPotion', 'BlessingOfTheForge', 'TestModSTS:PlaceholderPotion', 'ElixirPotion', 'CunningPotion', 'PotionOfCapacity', 'StancePotion', 'Regen Potion', 'Ancient Potion', 'LiquidBronze', 'GamblersBrew', 'EssenceOfSteel', 'DuplicationPotion', 'DistilledChaos', 'LiquidMemories', 'HeartOfIron', 'GhostInAJar', 'EssenceOfDarkness', 'Ambrosia', 'CultistPotion', 'Fruit Juice', 'SneckoOil', 'FairyPotion', 'SmokeBomb', 'EntropicBrew'}

BASE_GAME_ATTACKS = {'Immolate', 'Anger', 'Cleave', 'Reaper', 'Iron Wave', 'Reckless Charge', 'Hemokinesis', 'Body Slam', 'Blood for Blood', 'Clash', 'Thunderclap', 'Pummel', 'Pommel Strike', 'Twin Strike', 'Bash', 'Clothesline', 'Rampage', 'Sever Soul', 'Whirlwind', 'Fiend Fire', 'Headbutt', 'Wild Strike', 'Heavy Blade', 'Searing Blow', 'Feed', 'Bludgeon', 'Perfected Strike', 'Carnage', 'Dropkick', 'Sword Boomerang', 'Uppercut', 'Strike_R', 'Grand Finale', 'Glass Knife', 'Underhanded Strike', 'Dagger Spray', 'Bane', 'Unload', 'Dagger Throw', 'Choke', 'Poisoned Stab', 'Endless Agony', 'Riddle With Holes', 'Skewer', 'Quick Slash', 'Finisher', 'Die Die Die', 'Heel Hook', 'Eviscerate', 'Dash', 'Backstab', 'Slice', 'Flechettes', 'Masterful Stab', 'Strike_G', 'Neutralize', 'Sucker Punch', 'All Out Attack', 'Flying Knee', 'Predator', 'Go for the Eyes', 'Core Surge', 'Ball Lightning', 'Sunder', 'Streamline', 'Compile Driver', 'All For One', 'Blizzard', 'Barrage', 'Meteor Strike', 'Rebound', 'Melter', 'Gash', 'Sweeping Beam', 'FTL', 'Rip and Tear', 'Lockon', 'Scrape', 'Beam Cell', 'Cold Snap', 'Strike_B', 'Thunder Strike', 'Hyperbeam', 'Doom and Gloom', 'Consecrate', 'BowlingBash', 'WheelKick', 'FlyingSleeves', 'JustLucky', 'FlurryOfBlows', 'TalkToTheHand', 'WindmillStrike', 'CarveReality', 'Wallop', 'SashWhip', 'Eruption', 'LessonLearned', 'CutThroughFate', 'ReachHeaven', 'Ragnarok', 'FearNoEvil', 'SandsOfTime', 'Conclude', 'FollowUp', 'Brilliance', 'CrushJoints', 'Tantrum', 'Weave', 'SignatureMove', 'Strike_P', 'EmptyFist', 'Shiv', 'Dramatic Entrance', 'RitualDagger', 'Bite', 'Smite', 'Expunger', 'HandOfGreed', 'Flash of Steel', 'ThroughViolence', 'Swift Strike', 'Mind Blast'}
BASE_GAME_SKILLS = {'Spot Weakness', 'Warcry', 'Offering', 'Exhume', 'Power Through', 'Dual Wield', 'Flex', 'Infernal Blade', 'Intimidate', 'True Grit', 'Impervious', 'Shrug It Off', 'Flame Barrier', 'Burning Pact', 'Shockwave', 'Seeing Red', 'Disarm', 'Armaments', 'Havoc', 'Rage', 'Limit Break', 'Entrench', 'Defend_R', 'Sentinel', 'Battle Trance', 'Second Wind', 'Bloodletting', 'Ghostly Armor', 'Double Tap', 'Crippling Poison', 'Cloak And Dagger', 'Storm of Steel', 'Deadly Poison', 'Leg Sweep', 'Bullet Time', 'Catalyst', 'Tactician', 'Blade Dance', 'Deflect', 'Night Terror', 'Expertise', 'Blur', 'Setup', 'Burst', 'Acrobatics', 'Doppelganger', 'Adrenaline', 'Calculated Gamble', 'Escape Plan', 'Terror', 'Phantasmal Killer', 'Malaise', 'Reflex', 'Survivor', 'Defend_G', 'Corpse Explosion', 'Venomology', 'Bouncing Flask', 'Backflip', 'Outmaneuver', 'Concentrate', 'Prepared', 'PiercingWail', 'Distraction', 'Dodge and Roll', 'Genetic Algorithm', 'Zap', 'Steam Power', 'Fission', 'Glacier', 'Consume', 'Redo', 'Fusion', 'Amplify', 'Reboot', 'Aggregate', 'Chaos', 'Stack', 'Seek', 'Rainbow', 'Chill', 'BootSequence', 'Coolheaded', 'Tempest', 'Turbo', 'Undo', 'Force Field', 'Darkness', 'Double Energy', 'Reinforced Body', 'Conserve Battery', 'Defend_B', 'Dualcast', 'Auto Shields', 'Reprogram', 'Hologram', 'Leap', 'Recycle', 'Skim', 'White Noise', 'Multi-Cast', 'Steam', 'DeusExMachina', 'Vengeance', 'Sanctity', 'Halt', 'Protect', 'Indignation', 'ThirdEye', 'ForeignInfluence', 'Crescendo', 'SpiritShield', 'ClearTheMind', 'EmptyBody', 'WreathOfFlame', 'Collect', 'InnerPeace', 'Omniscience', 'Wish', 'DeceiveReality', 'Alpha', 'Vault', 'Scrawl', 'Blasphemy', 'Defend_P', 'WaveOfTheHand', 'Meditate', 'Perseverance', 'Swivel', 'Worship', 'Vigilance', 'PathToVictory', 'Evaluate', 'EmptyMind', 'Prostrate', 'ConjureBlade', 'Judgement', 'Pray', 'Beta', 'Dark Shackles', 'J.A.X.', 'PanicButton', 'Trip', 'FameAndFortune', 'Impatience', 'The Bomb', 'Insight', 'Miracle', 'Blind', 'Bandage Up', 'Secret Technique', 'Deep Breath', 'Violence', 'Secret Weapon', 'Apotheosis', 'Forethought', 'Enlightenment', 'Purity', 'Panacea', 'Transmutation', 'Ghostly', 'Chrysalis', 'Discovery', 'Finesse', 'Master of Strategy', 'Good Instincts', 'Jack Of All Trades', 'Safety', 'Metamorphosis', 'Thinking Ahead', 'Madness'}
BASE_GAME_POWERS = {'Inflame', 'Brutality', 'Juggernaut', 'Berserk', 'Metallicize', 'Combust', 'Dark Embrace', 'Barricade', 'Feel No Pain', 'Corruption', 'Rupture', 'Demon Form', 'Fire Breathing', 'Evolve', 'A Thousand Cuts', 'After Image', 'Tools of the Trade', 'Caltrops', 'Wraith Form v2', 'Envenom', 'Well Laid Plans', 'Noxious Fumes', 'Infinite Blades', 'Accuracy', 'Footwork', 'Storm', 'Hello World', 'Creative AI', 'Echo Form', 'Self Repair', 'Loop', 'Static Discharge', 'Heatsinks', 'Buffer', 'Electrodynamics', 'Machine Learning', 'Biased Cognition', 'Capacitor', 'Defragment', 'Wireheading', 'BattleHymn', 'DevaForm', 'LikeWater', 'Establishment', 'Fasting2', 'Adaptation', 'MentalFortress', 'Study', 'Devotion', 'Nirvana', 'MasterReality', 'Sadistic Nature', 'LiveForever', 'BecomeAlmighty', 'Panache', 'Mayhem', 'Magnetism', 'Omega'}
BASE_GAME_CURSES = {'Regret', 'Writhe', 'AscendersBane', 'Decay', 'Necronomicurse', 'Pain', 'Parasite', 'Doubt', 'Injury', 'Clumsy', 'CurseOfTheBell', 'Normality', 'Pride', 'Shame'}


def heart_fight_data_process(data):
    # gold_per_floor?, seed_source_timestamp?,
    # master_deck, relics, seed_played, character_chosen, current_hp_per_floor (second last floor and last floor), gold,
    # victory, max_hp_per_floor (second last floor)
    new_data = dict()

    new_data['gold'] = data['gold']
    new_data['master_deck'] = data['master_deck']
    new_data['relics'] = data['relics']
    new_data['seed_played'] = data['seed_played']
    new_data['character_chosen'] = data['character_chosen']
    new_data['entering_hp'] = data['current_hp_per_floor'][-2]
    new_data['end_hp'] = data['current_hp_per_floor'][-1]
    new_data['victory'] = data['victory']
    new_data['map_hp'] = data['max_hp_per_floor'][-2]
    new_data['potions_obtained'] = [x['key'] for x in data['potions_obtained']]
    # Add potions that were picked up to at some point. Pick some random ones for Silver and Bronze

    return new_data


def process_runs(data_dir):
    runs = list()
    bad_file_count = 0
    total_file_count = 0
    file_not_processed_count = 0
    file_processed_count = 0
    file_master_not_match_count = 0
    fight_training_examples = list()
    for filename in os.listdir(data_dir):
        if filename.endswith(".run"):
            with open(f"{data_dir}/{filename}", 'r') as file:
                data = json.load(file)
                if is_bad_file(data):
                    bad_file_count += 1
                else:
                    total_file_count += 1
                    processed_run = list()
                    try:
                        processed_run = process_run(data)
                        file_processed_count += 1
                        print(f'Processed file sucessfully: {filename}')
                        print(processed_run)
                    except RuntimeError as e:
                        file_master_not_match_count += 1
                        print(filename)
                        pass
                    except Exception as e:
                        file_not_processed_count += 1
                        print(filename)
                    fight_training_examples.extend(processed_run)

    print(f'Files filtered with pre-filter: {bad_file_count}')
    print(f'Files SUCCESSFULLY processed: {file_processed_count}')
    print(f'Files with master deck not matching created deck: {file_master_not_match_count}')
    print(f'Files not processed: {file_not_processed_count}')
    print(f'Total files: {total_file_count}')
    print(f'Number of Training Examples: {len(fight_training_examples)}')
    return runs


def process_run(data):
    battle_stats_by_floor = {battle_stat['floor']: battle_stat for battle_stat in data['damage_taken']}
    events_by_floor = {event_stat['floor']: event_stat for event_stat in data['event_choices']}
    card_choices_by_floor = {card_choice['floor']: card_choice for card_choice in data['card_choices']}
    relics_by_floor = get_relics_by_floor(data)
    campfire_choices_by_floor = {campfire_choice['floor']: campfire_choice for campfire_choice in
                                 data['campfire_choices']}
    purchases_by_floor = get_stat_with_separate_floor_list(data, 'items_purchased', 'item_purchase_floors')
    purges_by_floor = get_stat_with_separate_floor_list(data, 'items_purged', 'items_purged_floors')
    potion_use_by_floor = list(set(data['potions_floor_usage']))

    current_deck = get_starting_deck(data['character_chosen'], data['ascension_level'])
    current_relics = get_starting_relics(data['character_chosen'])

    unknown_removes_by_floor = dict()
    unknown_upgrades_by_floor = dict()
    unknown_transforms_by_floor = dict()

    processed_fights = list()
    process_neow(data['neow_bonus'], current_deck, current_relics, data['relics'])
    for floor in range(1, data['floor_reached']):
        if floor in battle_stats_by_floor and floor != 1:
            fight_data = try_process_data(partial(process_battle, data, battle_stats_by_floor[floor], potion_use_by_floor,
                                     current_deck, current_relics, floor),
                             floor, current_deck, data)
            processed_fights.append(fight_data)

        if floor in relics_by_floor:
            current_relics.extend(relics_by_floor[floor])

        if floor in card_choices_by_floor:
            process_card_choice(card_choices_by_floor[floor], current_deck, current_relics)

        if floor in campfire_choices_by_floor:
            try_process_data(partial(process_campfire_choice, campfire_choices_by_floor[floor], current_deck), floor, current_deck, data)

        if floor in purchases_by_floor:
            try_process_data(partial(process_purchases, purchases_by_floor[floor], current_deck, current_relics), floor, current_deck, data)

        if floor in purges_by_floor:
            try_process_data(partial(process_purges, purges_by_floor[floor], current_deck), floor, current_deck, data)

        if floor in events_by_floor:
            try_process_data(partial(process_events, events_by_floor[floor], current_deck, current_relics), floor, current_deck, data)

    current_deck.sort()
    master_deck = sorted(data['master_deck'])
    current_relics.sort()
    master_relics = sorted(data['relics'])
    if current_deck != master_deck or current_relics != master_relics:
        if current_deck == master_deck:
            print(f'\nSo close!!!!!   XX Relics XX')
        elif current_relics == master_relics:
            print(f'\nSo close!!!!!   XX Deck XX')
        else:
            print(f'\nLess close!!!!!   XX Deck and Relics XX')


        print(f'Current Deck\t: {sorted(current_deck)}')
        print(f'Master Deck\t\t: {sorted(master_deck)}')
        print(f'Current Relics\t: {sorted(current_relics)}')
        print(f'Master Relics\t: {sorted(master_relics)}\n')
        raise RuntimeError('Final decks or relics did not match')
    else:
        return processed_fights


def try_process_data(func, floor, current_deck, master_data):
    try:
        return func()
    except Exception as e:
        floor_reached = master_data['floor_reached']
        master_deck = master_data['master_deck']
        print(f'\nFunction {func.func.__name__} failed on floor {floor} of {floor_reached}')
        print(f'Reason for exception: {e}')
        print(f'Current Deck\t: {sorted(current_deck)}')
        print(f'Master Deck\t\t: {sorted(master_deck)}\n')
        raise e


def process_battle(master_data, battle_stat, potion_use_by_floor, current_deck, current_relics, floor):
    fight_data = dict()
    fight_data['cards'] = list(current_deck)
    fight_data['relics'] = list(current_relics)
    fight_data['max_hp'] = master_data['max_hp_per_floor'][floor - 2]
    fight_data['entering_hp'] = master_data['current_hp_per_floor'][floor - 2]
    fight_data['character'] = master_data['character_chosen']
    fight_data['ascension'] = master_data['ascension_level']
    fight_data['enemies'] = battle_stat['enemies']
    fight_data['potion_used'] = floor in potion_use_by_floor
    fight_data['floor'] = floor
    if master_data['current_hp_per_floor'] == 0:
        hp_change = battle_stat['damage']
    else:
        hp_change = master_data['current_hp_per_floor'][floor - 2] - master_data['current_hp_per_floor'][floor - 1]
    fight_data['damage_taken'] = hp_change
    return fight_data


def process_card_choice(card_choice_data, current_deck, current_relics):
    picked_card = card_choice_data['picked']
    if picked_card != 'SKIP' and picked_card != 'Singing Bowl':
        if 'Molten Egg 2' in current_relics and picked_card in BASE_GAME_ATTACKS and picked_card[-2] != '+1':
            picked_card += '+1'
        if 'Toxic Egg 2' in current_relics and picked_card in BASE_GAME_SKILLS and picked_card[-2] != '+1':
            picked_card += '+1'
        if 'Frozen Egg 2' in current_relics and picked_card in BASE_GAME_POWERS and picked_card[-2] != '+1':
            picked_card += '+1'
        current_deck.append(picked_card)


def process_campfire_choice(campfire_data, current_deck):
    choice = campfire_data['key']
    if choice == 'SMITH':
        upgrade_card(current_deck, campfire_data['data'])
    if choice == 'PURGE':
        current_deck.remove(campfire_data['data'])


def process_purchases(purchase_data, current_deck, current_relics):
    purchased_cards = [x for x in purchase_data if x not in BASE_GAME_RELICS and x not in BASE_GAME_POTIONS]
    purchased_relics = [x for x in purchase_data if x not in purchased_cards and x not in BASE_GAME_POTIONS]
    current_deck.extend(purchased_cards)
    current_relics.extend(purchased_relics)


def process_purges(purge_data, current_deck):
    for card in purge_data:
        current_deck.remove(card)


def process_events(event_data, current_deck, current_relics):
    if 'relics_obtained' in event_data:
        current_relics.extend(event_data['relics_obtained'])
    if 'relics_lost' in event_data:
        for relic in event_data['relics_lost']:
            current_relics.remove(relic)
    if 'cards_obtained' in event_data:
        current_deck.extend(event_data['cards_obtained'])
    if 'cards_removed' in event_data:
        for card in event_data['cards_removed']:
            current_deck.remove(card)
    if 'cards_upgraded' in event_data:
        for card in event_data['cards_upgraded']:
            upgrade_card(current_deck, card)


def process_neow(neow_bonus, current_deck, current_relics, master_relics):
    # {'THREE_ENEMY_KILL', 'UPGRADE_CARD', 'REMOVE_CARD', 'THREE_SMALL_POTIONS', 'REMOVE_TWO', 'THREE_CARDS', 'THREE_RARE_CARDS', 'TRANSFORM_CARD', 'TWENTY_PERCENT_HP_BONUS', 'ONE_RANDOM_RARE_CARD', 'TEN_PERCENT_HP_BONUS', 'HUNDRED_GOLD', 'TWO_FIFTY_GOLD'}
    if neow_bonus == 'ONE_RARE_RELIC' or neow_bonus == 'RANDOM_COMMON_RELIC':
        current_relics.append(master_relics[1])
    if neow_bonus == 'BOSS_RELIC':
        current_relics[0] = master_relics[0]
    if neow_bonus == 'THREE_ENEMY_KILL':
        current_relics.append('NeowsBlessing')





def upgrade_card(current_deck, card_to_upgrade):
    card_to_upgrade_index = current_deck.index(card_to_upgrade)
    if 'earing' in card_to_upgrade:
        print(f'Probably Searing Blow id: {card_to_upgrade}')
    current_deck[card_to_upgrade_index] += '+1'


def get_stats_by_floor_with_list(data, data_key):
    stats_by_floor = dict()
    if data_key in data:
        for stat in data[data_key]:
            floor = stat['floor']
            if floor not in stats_by_floor:
                stats_by_floor[floor] = list()
            stats_by_floor[floor].append(stat['key'])
    return stats_by_floor


def get_stat_with_separate_floor_list(data, obtain_key, floor_key):
    stats_by_floor = dict()
    if obtain_key in data and floor_key in data and len(data[obtain_key]) == len(data[floor_key]):
        obtains = data[obtain_key]
        floors = data[floor_key]
        for index, obt in enumerate(obtains):
            flr = floors[index]
            obt = obtains[index]
            if flr not in stats_by_floor:
                stats_by_floor[flr] = list()
            stats_by_floor[flr].append(obt)
    return stats_by_floor


def get_relics_by_floor(data):
    relics_by_floor = get_stats_by_floor_with_list(data, 'relics_obtained')
    boss_relics = data['boss_relics']
    if len(boss_relics) >= 1:
        picked_relic = boss_relics[0]['picked']
        if picked_relic != 'SKIP':
            relics_by_floor[17] = [picked_relic]
    if len(boss_relics) == 2:
        picked_relic = boss_relics[1]['picked']
        if picked_relic != 'SKIP':
            relics_by_floor[34] = [picked_relic]
    return relics_by_floor


def get_starting_relics(character):
    if character == 'IRONCLAD':
        return ['Burning Blood']
    elif character == 'THE_SILENT':
        return ['Ring of the Snake']
    elif character == 'DEFECT':
        return ['Cracked Core']
    elif character == 'WATCHER':
        return ['PureWater']
    else:
        print(f'Unsupported character {character}')


def get_starting_deck(character, ascension):
    basic_deck = ['Strike', 'Strike', 'Strike', 'Strike', 'Defend', 'Defend', 'Defend', 'Defend']
    if character == 'IRONCLAD':
        basic_deck.extend(['Strike', 'Bash'])
        character_spefic_basic_cards(basic_deck, '_R')
    elif character == 'THE_SILENT':
        basic_deck.extend(['Strike', 'Defend', 'Survivor', 'Neutralize'])
        character_spefic_basic_cards(basic_deck, '_G')
    elif character == 'DEFECT':
        basic_deck.extend(['Zap', 'Dualcast'])
        character_spefic_basic_cards(basic_deck, '_B')
    elif character == 'WATCHER':
        basic_deck.extend(['Eruption', 'Vigilance'])
        character_spefic_basic_cards(basic_deck, '_P')
    else:
        print(f'Unsupported character {character}')
    if ascension >= 10:
        basic_deck.append('AscendersBane')
    return basic_deck


def character_spefic_basic_cards(deck, suffix):
    for index, card in enumerate(deck):
        if card == 'Strike' or card == 'Defend':
            deck[index] = card + suffix


def is_bad_file(data):
    necessary_fields = ['damage_taken', 'event_choices', 'card_choices', 'relics_obtained', 'campfire_choices',
                        'items_purchased', 'item_purchase_floors', 'items_purged', 'items_purged_floors',
                        'character_chosen', 'boss_relics']
    for field in necessary_fields:
        if field not in data:
            print(f'File missing field: {field}')
            return True

    key = 'character_chosen'
    if key not in data or data[key] not in ['IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER']:
        print(f'Modded character: {data[key]}')
        return True

    key = 'floor_reached'
    if key not in data or data[key] < 4:
        return True

    key = 'score'
    if key not in data or data[key] < 10:
        return True

    key = 'is_trial'
    if key not in data or data[key] is True:
        return True

    key = 'is_daily'
    if key not in data or data[key] is True:
        return True

    key = 'chose_seed'
    if key not in data or data[key] is True:
        return True

    key = 'is_endless'
    if key not in data or data[key] is True:
        return True

    key = 'daily_mods'
    if key in data:
        return True


def write_file(data):
    with open('out/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def process_single_file(data_dir, filename):
    with open(f"{data_dir}/{filename}", 'r') as file:
        data = json.load(file)
        result = process_run(data)
        print(f'Result: {result}')


directory = '2019SpireRuns'
processed_runs = process_runs(directory)
# process_single_file(directory, '1547407389.run')
# pprint.pprint(processed_runs[0])
# write_file(processed_runs)

"""
# Keys

gold_per_floor
floor_reached
playtime
items_purged
score
play_id
local_time
is_ascension_mode
campfire_choices
neow_cost
seed_source_timestamp
circlet_count
master_deck
relics
potions_floor_usage
damage_taken
seed_played
potions_obtained
is_trial
path_per_floor
character_chosen
items_purchased
campfire_rested
item_purchase_floors
current_hp_per_floor
gold
neow_bonus
is_prod
is_daily
chose_seed
campfire_upgraded
win_rate
timestamp
path_taken
build_version
purchased_purges
victory
max_hp_per_floor
card_choices
player_experience
relics_obtained
event_choices
is_beta
boss_relics
items_purged_floors
is_endless
potions_floor_spawned
killed_by
ascension_level
"""
