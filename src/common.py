

class StSGlobals:
    """
    Parameters in each run file:
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

    BASE_GAME_RELICS = {'Burning Blood', 'Cracked Core', 'PureWater', 'Ring of the Snake', 'Akabeko', 'Anchor',
                        'Ancient Tea Set', 'Art of War', 'Bag of Marbles', 'Bag of Preparation', 'Blood Vial',
                        'TestModSTS:BottledPlaceholderRelic', 'Bronze Scales', 'Centennial Puzzle', 'CeramicFish',
                        'Damaru', 'DataDisk', 'Dream Catcher', 'Happy Flower', 'Juzu Bracelet', 'Lantern', 'MawBank',
                        'MealTicket', 'Nunchaku', 'Oddly Smooth Stone', 'Omamori', 'Orichalcum', 'Pen Nib',
                        'TestModSTS:PlaceholderRelic2', 'Potion Belt', 'PreservedInsect', 'Red Skull', 'Regal Pillow',
                        'TestModSTS:DefaultClickableRelic', 'Smiling Mask', 'Snake Skull', 'Strawberry', 'Boot',
                        'Tiny Chest', 'Toy Ornithopter', 'Vajra', 'War Paint', 'Whetstone', 'Blue Candle',
                        'Bottled Flame', 'Bottled Lightning', 'Bottled Tornado', 'Darkstone Periapt', 'Yang',
                        'Eternal Feather', 'Frozen Egg 2', 'Cables', 'Gremlin Horn', 'HornCleat', 'InkBottle', 'Kunai',
                        'Letter Opener', 'Matryoshka', 'Meat on the Bone', 'Mercury Hourglass', 'Molten Egg 2',
                        'Mummified Hand', 'Ninja Scroll', 'Ornamental Fan', 'Pantograph', 'Paper Crane', 'Paper Frog',
                        'Pear', 'Question Card', 'Self Forming Clay', 'Shuriken', 'Singing Bowl', 'StrikeDummy',
                        'Sundial', 'Symbiotic Virus', 'TeardropLocket', 'The Courier', 'Toxic Egg 2',
                        'White Beast Statue', 'Bird Faced Urn', 'Calipers', 'CaptainsWheel', 'Champion Belt',
                        'Charon\'s Ashes', 'CloakClasp', 'Dead Branch', 'Du-Vu Doll', 'Emotion Chip', 'FossilizedHelix',
                        'Gambling Chip', 'Ginger', 'Girya', 'GoldenEye', 'Ice Cream', 'Incense Burner', 'Lizard Tail',
                        'Magic Flower', 'Mango', 'Old Coin', 'Peace Pipe', 'Pocketwatch', 'Prayer Wheel', 'Shovel',
                        'StoneCalendar', 'The Specimen', 'Thread and Needle', 'Tingsha', 'Torii', 'Tough Bandages',
                        'TungstenRod', 'Turnip', 'Unceasing Top', 'WingedGreaves', 'Astrolabe', 'Black Blood',
                        'Black Star', 'Busted Crown', 'Calling Bell', 'Coffee Dripper', 'Cursed Key', 'Ectoplasm',
                        'Empty Cage', 'FrozenCore', 'Fusion Hammer', 'HolyWater', 'HoveringKite', 'Inserter',
                        'Mark of Pain', 'Nuclear Battery', 'Pandora\'s Box', 'Philosopher\'s Stone',
                        'Ring of the Serpent', 'Runic Cube', 'Runic Dome', 'Runic Pyramid', 'SacredBark',
                        'SlaversCollar', 'Snecko Eye', 'Sozu', 'Tiny House', 'Velvet Choker', 'VioletLotus',
                        'WristBlade', 'Bloody Idol', 'CultistMask', 'Enchiridion', 'FaceOfCleric', 'Golden Idol',
                        'GremlinMask', 'Mark of the Bloom', 'MutagenicStrength', 'Nloth\'s Gift', 'NlothsMask',
                        'Necronomicon', 'NeowsBlessing', 'Nilry\'s Codex', 'Odd Mushroom', 'Red Mask', 'Spirit Poop',
                        'SsserpentHead', 'WarpedTongs', 'Brimstone', 'Cauldron', 'Chemical X', 'ClockworkSouvenir',
                        'DollysMirror', 'Frozen Eye', 'HandDrill', 'Lee\'s Waffle', 'Medical Kit', 'Melange',
                        'Membership Card', 'OrangePellets', 'Orrery', 'PrismaticShard', 'Runic Capacitor', 'Sling',
                        'Strange Spoon', 'TheAbacus', 'Toolbox', 'TwistedFunnel'}
    BASE_GAME_POTIONS = {'BloodPotion', 'Poison Potion', 'FocusPotion', 'BottledMiracle', 'Block Potion',
                         'Dexterity Potion', 'Energy Potion', 'Explosive Potion', 'Fire Potion', 'Strength Potion',
                         'Swift Potion', 'Weak Potion', 'FearPotion', 'AttackPotion', 'SkillPotion', 'PowerPotion',
                         'ColorlessPotion', 'SteroidPotion', 'SpeedPotion', 'BlessingOfTheForge',
                         'TestModSTS:PlaceholderPotion', 'ElixirPotion', 'CunningPotion', 'PotionOfCapacity',
                         'StancePotion', 'Regen Potion', 'Ancient Potion', 'LiquidBronze', 'GamblersBrew',
                         'EssenceOfSteel', 'DuplicationPotion', 'DistilledChaos', 'LiquidMemories', 'HeartOfIron',
                         'GhostInAJar', 'EssenceOfDarkness', 'Ambrosia', 'CultistPotion', 'Fruit Juice', 'SneckoOil',
                         'FairyPotion', 'SmokeBomb', 'EntropicBrew'}

    BASE_GAME_ATTACKS = {'Immolate', 'Anger', 'Cleave', 'Reaper', 'Iron Wave', 'Reckless Charge', 'Hemokinesis',
                         'Body Slam', 'Blood for Blood', 'Clash', 'Thunderclap', 'Pummel', 'Pommel Strike',
                         'Twin Strike', 'Bash', 'Clothesline', 'Rampage', 'Sever Soul', 'Whirlwind', 'Fiend Fire',
                         'Headbutt', 'Wild Strike', 'Heavy Blade', 'Searing Blow', 'Feed', 'Bludgeon',
                         'Perfected Strike', 'Carnage', 'Dropkick', 'Sword Boomerang', 'Uppercut', 'Strike_R',
                         'Grand Finale', 'Glass Knife', 'Underhanded Strike', 'Dagger Spray', 'Bane', 'Unload',
                         'Dagger Throw', 'Choke', 'Poisoned Stab', 'Endless Agony', 'Riddle With Holes', 'Skewer',
                         'Quick Slash', 'Finisher', 'Die Die Die', 'Heel Hook', 'Eviscerate', 'Dash', 'Backstab',
                         'Slice', 'Flechettes', 'Masterful Stab', 'Strike_G', 'Neutralize', 'Sucker Punch',
                         'All Out Attack', 'Flying Knee', 'Predator', 'Go for the Eyes', 'Core Surge', 'Ball Lightning',
                         'Sunder', 'Streamline', 'Compile Driver', 'All For One', 'Blizzard', 'Barrage',
                         'Meteor Strike', 'Rebound', 'Melter', 'Gash', 'Sweeping Beam', 'FTL', 'Rip and Tear', 'Lockon',
                         'Scrape', 'Beam Cell', 'Cold Snap', 'Strike_B', 'Thunder Strike', 'Hyperbeam',
                         'Doom and Gloom', 'Consecrate', 'BowlingBash', 'WheelKick', 'FlyingSleeves', 'JustLucky',
                         'FlurryOfBlows', 'TalkToTheHand', 'WindmillStrike', 'CarveReality', 'Wallop', 'SashWhip',
                         'Eruption', 'LessonLearned', 'CutThroughFate', 'ReachHeaven', 'Ragnarok', 'FearNoEvil',
                         'SandsOfTime', 'Conclude', 'FollowUp', 'Brilliance', 'CrushJoints', 'Tantrum', 'Weave',
                         'SignatureMove', 'Strike_P', 'EmptyFist', 'Shiv', 'Dramatic Entrance', 'RitualDagger', 'Bite',
                         'Smite', 'Expunger', 'HandOfGreed', 'Flash of Steel', 'ThroughViolence', 'Swift Strike',
                         'Mind Blast'}

    BASE_GAME_SKILLS = {'Spot Weakness', 'Warcry', 'Offering', 'Exhume', 'Power Through', 'Dual Wield', 'Flex',
                        'Infernal Blade', 'Intimidate', 'True Grit', 'Impervious', 'Shrug It Off', 'Flame Barrier',
                        'Burning Pact', 'Shockwave', 'Seeing Red', 'Disarm', 'Armaments', 'Havoc', 'Rage',
                        'Limit Break', 'Entrench', 'Defend_R', 'Sentinel', 'Battle Trance', 'Second Wind',
                        'Bloodletting', 'Ghostly Armor', 'Double Tap', 'Crippling Poison', 'Cloak And Dagger',
                        'Storm of Steel', 'Deadly Poison', 'Leg Sweep', 'Bullet Time', 'Catalyst', 'Tactician',
                        'Blade Dance', 'Deflect', 'Night Terror', 'Expertise', 'Blur', 'Setup', 'Burst', 'Acrobatics',
                        'Doppelganger', 'Adrenaline', 'Calculated Gamble', 'Escape Plan', 'Terror', 'Phantasmal Killer',
                        'Malaise', 'Reflex', 'Survivor', 'Defend_G', 'Corpse Explosion', 'Venomology', 'Bouncing Flask',
                        'Backflip', 'Outmaneuver', 'Concentrate', 'Prepared', 'PiercingWail', 'Distraction',
                        'Dodge and Roll', 'Genetic Algorithm', 'Zap', 'Steam Power', 'Fission', 'Glacier', 'Consume',
                        'Redo', 'Fusion', 'Amplify', 'Reboot', 'Aggregate', 'Chaos', 'Stack', 'Seek', 'Rainbow',
                        'Chill', 'BootSequence', 'Coolheaded', 'Tempest', 'Turbo', 'Undo', 'Force Field', 'Darkness',
                        'Double Energy', 'Reinforced Body', 'Conserve Battery', 'Defend_B', 'Dualcast', 'Auto Shields',
                        'Reprogram', 'Hologram', 'Leap', 'Recycle', 'Skim', 'White Noise', 'Multi-Cast', 'Steam',
                        'DeusExMachina', 'Vengeance', 'Sanctity', 'Halt', 'Protect', 'Indignation', 'ThirdEye',
                        'ForeignInfluence', 'Crescendo', 'SpiritShield', 'ClearTheMind', 'EmptyBody', 'WreathOfFlame',
                        'Collect', 'InnerPeace', 'Omniscience', 'Wish', 'DeceiveReality', 'Alpha', 'Vault', 'Scrawl',
                        'Blasphemy', 'Defend_P', 'WaveOfTheHand', 'Meditate', 'Perseverance', 'Swivel', 'Worship',
                        'Vigilance', 'PathToVictory', 'Evaluate', 'EmptyMind', 'Prostrate', 'ConjureBlade', 'Judgement',
                        'Pray', 'Beta', 'Dark Shackles', 'J.A.X.', 'PanicButton', 'Trip', 'FameAndFortune',
                        'Impatience', 'The Bomb', 'Insight', 'Miracle', 'Blind', 'Bandage Up', 'Secret Technique',
                        'Deep Breath', 'Violence', 'Secret Weapon', 'Apotheosis', 'Forethought', 'Enlightenment',
                        'Purity', 'Panacea', 'Transmutation', 'Ghostly', 'Chrysalis', 'Discovery', 'Finesse',
                        'Master of Strategy', 'Good Instincts', 'Jack Of All Trades', 'Safety', 'Metamorphosis',
                        'Thinking Ahead', 'Madness'}

    BASE_GAME_POWERS = {'Inflame', 'Brutality', 'Juggernaut', 'Berserk', 'Metallicize', 'Combust', 'Dark Embrace',
                        'Barricade', 'Feel No Pain', 'Corruption', 'Rupture', 'Demon Form', 'Fire Breathing', 'Evolve',
                        'A Thousand Cuts', 'After Image', 'Tools of the Trade', 'Caltrops', 'Wraith Form v2', 'Envenom',
                        'Well Laid Plans', 'Noxious Fumes', 'Infinite Blades', 'Accuracy', 'Footwork', 'Storm',
                        'Hello World', 'Creative AI', 'Echo Form', 'Self Repair', 'Loop', 'Static Discharge',
                        'Heatsinks', 'Buffer', 'Electrodynamics', 'Machine Learning', 'Biased Cognition', 'Capacitor',
                        'Defragment', 'Wireheading', 'BattleHymn', 'DevaForm', 'LikeWater', 'Establishment', 'Fasting2',
                        'Adaptation', 'MentalFortress', 'Study', 'Devotion', 'Nirvana', 'MasterReality',
                        'Sadistic Nature', 'LiveForever', 'BecomeAlmighty', 'Panache', 'Mayhem', 'Magnetism', 'Omega'}

    # TODO: Currently not used
    BASE_GAME_CURSES = {'Regret', 'Writhe', 'AscendersBane', 'Decay', 'Necronomicurse', 'Pain', 'Parasite', 'Doubt',
                        'Injury', 'Clumsy', 'CurseOfTheBell', 'Normality', 'Pride', 'Shame'}

    BASE_GAME_CARDS_AND_UPGRADES = {'A Thousand Cuts', 'A Thousand Cuts+1', 'Accuracy', 'Accuracy+1', 'Acrobatics',
                                    'Acrobatics+1', 'Adaptation', 'Adaptation+1', 'Adrenaline', 'Adrenaline+1',
                                    'After Image', 'After Image+1', 'Aggregate', 'Aggregate+1', 'All For One',
                                    'All For One+1', 'All Out Attack', 'All Out Attack+1', 'Alpha', 'Alpha+1',
                                    'Amplify', 'Amplify+1', 'Anger', 'Anger+1', 'Apotheosis', 'Apotheosis+1',
                                    'Armaments', 'Armaments+1', 'AscendersBane', 'Auto Shields', 'Auto Shields+1',
                                    'Backflip', 'Backflip+1', 'Backstab', 'Backstab+1', 'Ball Lightning',
                                    'Ball Lightning+1', 'Bandage Up', 'Bandage Up+1', 'Bane', 'Bane+1', 'Barrage',
                                    'Barrage+1', 'Barricade', 'Barricade+1', 'Bash', 'Bash+1', 'Battle Trance',
                                    'Battle Trance+1', 'BattleHymn', 'BattleHymn+1', 'Beam Cell', 'Beam Cell+1',
                                    'BecomeAlmighty', 'BecomeAlmighty+1', 'Berserk', 'Berserk+1', 'Beta', 'Beta+1',
                                    'Biased Cognition', 'Biased Cognition+1', 'Bite', 'Bite+1', 'Blade Dance',
                                    'Blade Dance+1', 'Blasphemy', 'Blasphemy+1', 'Blind', 'Blind+1', 'Blizzard',
                                    'Blizzard+1', 'Blood for Blood', 'Blood for Blood+1', 'Bloodletting',
                                    'Bloodletting+1', 'Bludgeon', 'Bludgeon+1', 'Blur', 'Blur+1', 'Body Slam',
                                    'Body Slam+1', 'BootSequence', 'BootSequence+1', 'Bouncing Flask',
                                    'Bouncing Flask+1', 'BowlingBash', 'BowlingBash+1', 'Brilliance', 'Brilliance+1',
                                    'Brutality', 'Brutality+1', 'Buffer', 'Buffer+1', 'Bullet Time', 'Bullet Time+1',
                                    'Burn', 'Burn+1', 'Burning Pact', 'Burning Pact+1', 'Burst', 'Burst+1',
                                    'Calculated Gamble', 'Calculated Gamble+1', 'Caltrops', 'Caltrops+1', 'Capacitor',
                                    'Capacitor+1', 'Carnage', 'Carnage+1', 'CarveReality', 'CarveReality+1', 'Catalyst',
                                    'Catalyst+1', 'Chaos', 'Chaos+1', 'Chill', 'Chill+1', 'Choke', 'Choke+1',
                                    'Chrysalis', 'Chrysalis+1', 'Clash', 'Clash+1', 'ClearTheMind', 'ClearTheMind+1',
                                    'Cleave', 'Cleave+1', 'Cloak And Dagger', 'Cloak And Dagger+1', 'Clothesline',
                                    'Clothesline+1', 'Clumsy', 'Cold Snap', 'Cold Snap+1', 'Collect', 'Collect+1',
                                    'Combust', 'Combust+1', 'Compile Driver', 'Compile Driver+1', 'Concentrate',
                                    'Concentrate+1', 'Conclude', 'Conclude+1', 'ConjureBlade', 'ConjureBlade+1',
                                    'Consecrate', 'Consecrate+1', 'Conserve Battery', 'Conserve Battery+1', 'Consume',
                                    'Consume+1', 'Coolheaded', 'Coolheaded+1', 'Core Surge', 'Core Surge+1',
                                    'Corpse Explosion', 'Corpse Explosion+1', 'Corruption', 'Corruption+1',
                                    'Creative AI', 'Creative AI+1', 'Crescendo', 'Crescendo+1', 'Crippling Poison',
                                    'Crippling Poison+1', 'CrushJoints', 'CrushJoints+1', 'CurseOfTheBell',
                                    'CutThroughFate', 'CutThroughFate+1', 'Dagger Spray', 'Dagger Spray+1',
                                    'Dagger Throw', 'Dagger Throw+1', 'Dark Embrace', 'Dark Embrace+1', 'Dark Shackles',
                                    'Dark Shackles+1', 'Darkness', 'Darkness+1', 'Dash', 'Dash+1', 'Dazed', 'Dazed+1',
                                    'Deadly Poison', 'Deadly Poison+1', 'Decay', 'DeceiveReality', 'DeceiveReality+1',
                                    'Deep Breath', 'Deep Breath+1', 'Defend', 'Defend+1', 'Deflect', 'Deflect+1',
                                    'Defragment', 'Defragment+1', 'Demon Form', 'Demon Form+1', 'DeusExMachina',
                                    'DeusExMachina+1', 'DevaForm', 'DevaForm+1', 'Devotion', 'Devotion+1',
                                    'Die Die Die', 'Die Die Die+1', 'Disarm', 'Disarm+1', 'Discovery', 'Discovery+1',
                                    'Distraction', 'Distraction+1', 'Dodge and Roll', 'Dodge and Roll+1',
                                    'Doom and Gloom', 'Doom and Gloom+1', 'Doppelganger', 'Doppelganger+1',
                                    'Double Energy', 'Double Energy+1', 'Double Tap', 'Double Tap+1', 'Doubt',
                                    'Dramatic Entrance', 'Dramatic Entrance+1', 'Dropkick', 'Dropkick+1', 'Dual Wield',
                                    'Dual Wield+1', 'Dualcast', 'Dualcast+1', 'Echo Form', 'Echo Form+1',
                                    'Electrodynamics', 'Electrodynamics+1', 'EmptyBody', 'EmptyBody+1', 'EmptyFist',
                                    'EmptyFist+1', 'EmptyMind', 'EmptyMind+1', 'Endless Agony', 'Endless Agony+1',
                                    'Enlightenment', 'Enlightenment+1', 'Entrench', 'Entrench+1', 'Envenom',
                                    'Envenom+1', 'Eruption', 'Eruption+1', 'Escape Plan', 'Escape Plan+1',
                                    'Establishment', 'Establishment+1', 'Evaluate', 'Evaluate+1', 'Eviscerate',
                                    'Eviscerate+1', 'Evolve', 'Evolve+1', 'Exhume', 'Exhume+1', 'Expertise',
                                    'Expertise+1', 'Expunger', 'Expunger+1', 'FTL', 'FTL+1', 'FameAndFortune',
                                    'FameAndFortune+1', 'Fasting2', 'Fasting2+1', 'FearNoEvil', 'FearNoEvil+1', 'Feed',
                                    'Feed+1', 'Feel No Pain', 'Feel No Pain+1', 'Fiend Fire', 'Fiend Fire+1', 'Finesse',
                                    'Finesse+1', 'Finisher', 'Finisher+1', 'Fire Breathing', 'Fire Breathing+1',
                                    'Fission', 'Fission+1', 'Flame Barrier', 'Flame Barrier+1', 'Flash of Steel',
                                    'Flash of Steel+1', 'Flechettes', 'Flechettes+1', 'Flex', 'Flex+1', 'FlurryOfBlows',
                                    'FlurryOfBlows+1', 'Flying Knee', 'Flying Knee+1', 'FlyingSleeves',
                                    'FlyingSleeves+1', 'FollowUp', 'FollowUp+1', 'Footwork', 'Footwork+1',
                                    'Force Field', 'Force Field+1', 'ForeignInfluence', 'ForeignInfluence+1',
                                    'Forethought', 'Forethought+1', 'Fusion', 'Fusion+1', 'Gash', 'Gash+1',
                                    'Genetic Algorithm', 'Genetic Algorithm+1', 'Ghostly', 'Ghostly Armor',
                                    'Ghostly Armor+1', 'Ghostly+1', 'Glacier', 'Glacier+1', 'Glass Knife',
                                    'Glass Knife+1', 'Go for the Eyes', 'Go for the Eyes+1', 'Good Instincts',
                                    'Good Instincts+1', 'Grand Finale', 'Grand Finale+1', 'Halt', 'Halt+1',
                                    'HandOfGreed', 'HandOfGreed+1', 'Havoc', 'Havoc+1', 'Headbutt', 'Headbutt+1',
                                    'Heatsinks', 'Heatsinks+1', 'Heavy Blade', 'Heavy Blade+1', 'Heel Hook',
                                    'Heel Hook+1', 'Hello World', 'Hello World+1', 'Hemokinesis', 'Hemokinesis+1',
                                    'Hologram', 'Hologram+1', 'Hyperbeam', 'Hyperbeam+1', 'Immolate', 'Immolate+1',
                                    'Impatience', 'Impatience+1', 'Impervious', 'Impervious+1', 'Indignation',
                                    'Indignation+1', 'Infernal Blade', 'Infernal Blade+1', 'Infinite Blades',
                                    'Infinite Blades+1', 'Inflame', 'Inflame+1', 'Injury', 'InnerPeace', 'InnerPeace+1',
                                    'Insight', 'Insight+1', 'Intimidate', 'Intimidate+1', 'Iron Wave', 'Iron Wave+1',
                                    'J.A.X.', 'J.A.X.+1', 'Jack Of All Trades', 'Jack Of All Trades+1', 'Judgement',
                                    'Judgement+1', 'Juggernaut', 'Juggernaut+1', 'JustLucky', 'JustLucky+1', 'Leap',
                                    'Leap+1', 'Leg Sweep', 'Leg Sweep+1', 'LessonLearned', 'LessonLearned+1',
                                    'LikeWater', 'LikeWater+1', 'Limit Break', 'Limit Break+1', 'LiveForever',
                                    'LiveForever+1', 'Lockon', 'Lockon+1', 'Loop', 'Loop+1', 'Machine Learning',
                                    'Machine Learning+1', 'Madness', 'Madness+1', 'Magnetism', 'Magnetism+1', 'Malaise',
                                    'Malaise+1', 'Master of Strategy', 'Master of Strategy+1', 'MasterReality',
                                    'MasterReality+1', 'Masterful Stab', 'Masterful Stab+1', 'Mayhem', 'Mayhem+1',
                                    'Meditate', 'Meditate+1', 'Melter', 'Melter+1', 'MentalFortress',
                                    'MentalFortress+1', 'Metallicize', 'Metallicize+1', 'Metamorphosis',
                                    'Metamorphosis+1', 'Meteor Strike', 'Meteor Strike+1', 'Mind Blast', 'Mind Blast+1',
                                    'Miracle', 'Miracle+1', 'Multi-Cast', 'Multi-Cast+1', 'Necronomicurse',
                                    'Neutralize', 'Neutralize+1', 'Night Terror', 'Night Terror+1', 'Nirvana',
                                    'Nirvana+1', 'Normality', 'Noxious Fumes', 'Noxious Fumes+1', 'Offering',
                                    'Offering+1', 'Omega', 'Omega+1', 'Omniscience', 'Omniscience+1', 'Outmaneuver',
                                    'Outmaneuver+1', 'Pain', 'Panacea', 'Panacea+1', 'Panache', 'Panache+1',
                                    'PanicButton', 'PanicButton+1', 'Parasite', 'PathToVictory', 'PathToVictory+1',
                                    'Perfected Strike', 'Perfected Strike+1', 'Perseverance', 'Perseverance+1',
                                    'Phantasmal Killer', 'Phantasmal Killer+1', 'PiercingWail', 'PiercingWail+1',
                                    'Poisoned Stab', 'Poisoned Stab+1', 'Pommel Strike', 'Pommel Strike+1',
                                    'Power Through', 'Power Through+1', 'Pray', 'Pray+1', 'Predator', 'Predator+1',
                                    'Prepared', 'Prepared+1', 'Pride', 'Prostrate', 'Prostrate+1', 'Protect',
                                    'Protect+1', 'Pummel', 'Pummel+1', 'Purity', 'Purity+1', 'Quick Slash',
                                    'Quick Slash+1', 'Rage', 'Rage+1', 'Ragnarok', 'Ragnarok+1', 'Rainbow', 'Rainbow+1',
                                    'Rampage', 'Rampage+1', 'ReachHeaven', 'ReachHeaven+1', 'Reaper', 'Reaper+1',
                                    'Reboot', 'Reboot+1', 'Rebound', 'Rebound+1', 'Reckless Charge',
                                    'Reckless Charge+1', 'Recycle', 'Recycle+1', 'Redo', 'Redo+1', 'Reflex', 'Reflex+1',
                                    'Regret', 'Reinforced Body', 'Reinforced Body+1', 'Reprogram', 'Reprogram+1',
                                    'Riddle With Holes', 'Riddle With Holes+1', 'Rip and Tear', 'Rip and Tear+1',
                                    'RitualDagger', 'RitualDagger+1', 'Rupture', 'Rupture+1', 'Sadistic Nature',
                                    'Sadistic Nature+1', 'Safety', 'Safety+1', 'Sanctity', 'Sanctity+1', 'SandsOfTime',
                                    'SandsOfTime+1', 'SashWhip', 'SashWhip+1', 'Scrape', 'Scrape+1', 'Scrawl',
                                    'Scrawl+1', 'Searing Blow', 'Searing Blow+1', 'Searing Blow+2', 'Searing Blow+3',
                                    'Searing Blow+4', 'Searing Blow+5', 'Searing Blow+6', 'Searing Blow+7',
                                    'Searing Blow+8', 'Searing Blow+9', 'Searing Blow+10', 'Searing Blow+11',
                                    'Searing Blow+12', 'Searing Blow+13', 'Searing Blow+14', 'Searing Blow+16',
                                    'Searing Blow+17', 'Second Wind', 'Second Wind+1', 'Secret Technique',
                                    'Secret Technique+1', 'Secret Weapon', 'Secret Weapon+1', 'Seeing Red',
                                    'Seeing Red+1', 'Seek', 'Seek+1', 'Self Repair', 'Self Repair+1', 'Sentinel',
                                    'Sentinel+1', 'Setup', 'Setup+1', 'Sever Soul', 'Sever Soul+1', 'Shame', 'Shiv',
                                    'Shiv+1', 'Shockwave', 'Shockwave+1', 'Shrug It Off', 'Shrug It Off+1',
                                    'SignatureMove', 'SignatureMove+1', 'Skewer', 'Skewer+1', 'Skim', 'Skim+1', 'Slice',
                                    'Slice+1', 'Slimed', 'Slimed+1', 'Smite', 'Smite+1', 'SpiritShield',
                                    'SpiritShield+1', 'Spot Weakness', 'Spot Weakness+1', 'Stack', 'Stack+1',
                                    'Static Discharge', 'Static Discharge+1', 'Steam', 'Steam Power', 'Steam Power+1',
                                    'Steam+1', 'Storm', 'Storm of Steel', 'Storm of Steel+1', 'Storm+1', 'Streamline',
                                    'Streamline+1', 'Strike', 'Strike+1', 'Study', 'Study+1', 'Sucker Punch',
                                    'Sucker Punch+1', 'Sunder', 'Sunder+1', 'Survivor', 'Survivor+1', 'Sweeping Beam',
                                    'Sweeping Beam+1', 'Swift Strike', 'Swift Strike+1', 'Swivel', 'Swivel+1',
                                    'Sword Boomerang', 'Sword Boomerang+1', 'Tactician', 'Tactician+1', 'TalkToTheHand',
                                    'TalkToTheHand+1', 'Tantrum', 'Tantrum+1', 'Tempest', 'Tempest+1', 'Terror',
                                    'Terror+1', 'The Bomb', 'The Bomb+1', 'Thinking Ahead', 'Thinking Ahead+1',
                                    'ThirdEye', 'ThirdEye+1', 'ThroughViolence', 'ThroughViolence+1', 'Thunder Strike',
                                    'Thunder Strike+1', 'Thunderclap', 'Thunderclap+1', 'Tools of the Trade',
                                    'Tools of the Trade+1', 'Transmutation', 'Transmutation+1', 'Trip', 'Trip+1',
                                    'True Grit', 'True Grit+1', 'Turbo', 'Turbo+1', 'Twin Strike', 'Twin Strike+1',
                                    'Underhanded Strike', 'Underhanded Strike+1', 'Undo', 'Undo+1', 'Unload',
                                    'Unload+1', 'Uppercut', 'Uppercut+1', 'Vault', 'Vault+1', 'Vengeance',
                                    'Vengeance+1', 'Venomology', 'Venomology+1', 'Vigilance', 'Vigilance+1', 'Violence',
                                    'Violence+1', 'Void', 'Void+1', 'Wallop', 'Wallop+1', 'Warcry', 'Warcry+1',
                                    'WaveOfTheHand', 'WaveOfTheHand+1', 'Weave', 'Weave+1', 'Well Laid Plans',
                                    'Well Laid Plans+1', 'WheelKick', 'WheelKick+1', 'Whirlwind', 'Whirlwind+1',
                                    'White Noise', 'White Noise+1', 'Wild Strike', 'Wild Strike+1', 'WindmillStrike',
                                    'WindmillStrike+1', 'Wireheading', 'Wireheading+1', 'Wish', 'Wish+1', 'Worship',
                                    'Worship+1', 'Wound', 'Wound+1', 'Wraith Form v2', 'Wraith Form v2+1',
                                    'WreathOfFlame', 'WreathOfFlame+1', 'Writhe', 'Zap', 'Zap+1', 'Strike_R',
                                    'Strike_R+1', 'Strike_G', 'Strike_G+1', 'Strike_B', 'Strike_B+1', 'Strike_P',
                                    'Strike_P+1', 'Defend_R', 'Defend_R+1', 'Defend_G', 'Defend_G+1', 'Defend_B',
                                    'Defend_B+1', 'Defend_P', 'Defend_P+1'}
