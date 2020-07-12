import datetime
import gc
import json
import os
import re
import time
from collections import Counter
from functools import partial

BASE_GAME_RELICS = {'Burning Blood', 'Cracked Core', 'PureWater', 'Ring of the Snake', 'Akabeko', 'Anchor',
                    'Ancient Tea Set', 'Art of War', 'Bag of Marbles', 'Bag of Preparation', 'Blood Vial',
                    'TestModSTS:BottledPlaceholderRelic', 'Bronze Scales', 'Centennial Puzzle', 'CeramicFish', 'Damaru',
                    'DataDisk', 'Dream Catcher', 'Happy Flower', 'Juzu Bracelet', 'Lantern', 'MawBank', 'MealTicket',
                    'Nunchaku', 'Oddly Smooth Stone', 'Omamori', 'Orichalcum', 'Pen Nib',
                    'TestModSTS:PlaceholderRelic2', 'Potion Belt', 'PreservedInsect', 'Red Skull', 'Regal Pillow',
                    'TestModSTS:DefaultClickableRelic', 'Smiling Mask', 'Snake Skull', 'Strawberry', 'Boot',
                    'Tiny Chest', 'Toy Ornithopter', 'Vajra', 'War Paint', 'Whetstone', 'Blue Candle', 'Bottled Flame',
                    'Bottled Lightning', 'Bottled Tornado', 'Darkstone Periapt', 'Yang', 'Eternal Feather',
                    'Frozen Egg 2', 'Cables', 'Gremlin Horn', 'HornCleat', 'InkBottle', 'Kunai', 'Letter Opener',
                    'Matryoshka', 'Meat on the Bone', 'Mercury Hourglass', 'Molten Egg 2', 'Mummified Hand',
                    'Ninja Scroll', 'Ornamental Fan', 'Pantograph', 'Paper Crane', 'Paper Frog', 'Pear',
                    'Question Card', 'Self Forming Clay', 'Shuriken', 'Singing Bowl', 'StrikeDummy', 'Sundial',
                    'Symbiotic Virus', 'TeardropLocket', 'The Courier', 'Toxic Egg 2', 'White Beast Statue',
                    'Bird Faced Urn', 'Calipers', 'CaptainsWheel', 'Champion Belt', 'Charon\'s Ashes', 'CloakClasp',
                    'Dead Branch', 'Du-Vu Doll', 'Emotion Chip', 'FossilizedHelix', 'Gambling Chip', 'Ginger', 'Girya',
                    'GoldenEye', 'Ice Cream', 'Incense Burner', 'Lizard Tail', 'Magic Flower', 'Mango', 'Old Coin',
                    'Peace Pipe', 'Pocketwatch', 'Prayer Wheel', 'Shovel', 'StoneCalendar', 'The Specimen',
                    'Thread and Needle', 'Tingsha', 'Torii', 'Tough Bandages', 'TungstenRod', 'Turnip', 'Unceasing Top',
                    'WingedGreaves', 'Astrolabe', 'Black Blood', 'Black Star', 'Busted Crown', 'Calling Bell',
                    'Coffee Dripper', 'Cursed Key', 'Ectoplasm', 'Empty Cage', 'FrozenCore', 'Fusion Hammer',
                    'HolyWater', 'HoveringKite', 'Inserter', 'Mark of Pain', 'Nuclear Battery', 'Pandora\'s Box',
                    'Philosopher\'s Stone', 'Ring of the Serpent', 'Runic Cube', 'Runic Dome', 'Runic Pyramid',
                    'SacredBark', 'SlaversCollar', 'Snecko Eye', 'Sozu', 'Tiny House', 'Velvet Choker', 'VioletLotus',
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
                     'StancePotion', 'Regen Potion', 'Ancient Potion', 'LiquidBronze', 'GamblersBrew', 'EssenceOfSteel',
                     'DuplicationPotion', 'DistilledChaos', 'LiquidMemories', 'HeartOfIron', 'GhostInAJar',
                     'EssenceOfDarkness', 'Ambrosia', 'CultistPotion', 'Fruit Juice', 'SneckoOil', 'FairyPotion',
                     'SmokeBomb', 'EntropicBrew'}

BASE_GAME_ATTACKS = {'Immolate', 'Anger', 'Cleave', 'Reaper', 'Iron Wave', 'Reckless Charge', 'Hemokinesis',
                     'Body Slam', 'Blood for Blood', 'Clash', 'Thunderclap', 'Pummel', 'Pommel Strike', 'Twin Strike',
                     'Bash', 'Clothesline', 'Rampage', 'Sever Soul', 'Whirlwind', 'Fiend Fire', 'Headbutt',
                     'Wild Strike', 'Heavy Blade', 'Searing Blow', 'Feed', 'Bludgeon', 'Perfected Strike', 'Carnage',
                     'Dropkick', 'Sword Boomerang', 'Uppercut', 'Strike_R', 'Grand Finale', 'Glass Knife',
                     'Underhanded Strike', 'Dagger Spray', 'Bane', 'Unload', 'Dagger Throw', 'Choke', 'Poisoned Stab',
                     'Endless Agony', 'Riddle With Holes', 'Skewer', 'Quick Slash', 'Finisher', 'Die Die Die',
                     'Heel Hook', 'Eviscerate', 'Dash', 'Backstab', 'Slice', 'Flechettes', 'Masterful Stab', 'Strike_G',
                     'Neutralize', 'Sucker Punch', 'All Out Attack', 'Flying Knee', 'Predator', 'Go for the Eyes',
                     'Core Surge', 'Ball Lightning', 'Sunder', 'Streamline', 'Compile Driver', 'All For One',
                     'Blizzard', 'Barrage', 'Meteor Strike', 'Rebound', 'Melter', 'Gash', 'Sweeping Beam', 'FTL',
                     'Rip and Tear', 'Lockon', 'Scrape', 'Beam Cell', 'Cold Snap', 'Strike_B', 'Thunder Strike',
                     'Hyperbeam', 'Doom and Gloom', 'Consecrate', 'BowlingBash', 'WheelKick', 'FlyingSleeves',
                     'JustLucky', 'FlurryOfBlows', 'TalkToTheHand', 'WindmillStrike', 'CarveReality', 'Wallop',
                     'SashWhip', 'Eruption', 'LessonLearned', 'CutThroughFate', 'ReachHeaven', 'Ragnarok', 'FearNoEvil',
                     'SandsOfTime', 'Conclude', 'FollowUp', 'Brilliance', 'CrushJoints', 'Tantrum', 'Weave',
                     'SignatureMove', 'Strike_P', 'EmptyFist', 'Shiv', 'Dramatic Entrance', 'RitualDagger', 'Bite',
                     'Smite', 'Expunger', 'HandOfGreed', 'Flash of Steel', 'ThroughViolence', 'Swift Strike',
                     'Mind Blast'}
BASE_GAME_SKILLS = {'Spot Weakness', 'Warcry', 'Offering', 'Exhume', 'Power Through', 'Dual Wield', 'Flex',
                    'Infernal Blade', 'Intimidate', 'True Grit', 'Impervious', 'Shrug It Off', 'Flame Barrier',
                    'Burning Pact', 'Shockwave', 'Seeing Red', 'Disarm', 'Armaments', 'Havoc', 'Rage', 'Limit Break',
                    'Entrench', 'Defend_R', 'Sentinel', 'Battle Trance', 'Second Wind', 'Bloodletting', 'Ghostly Armor',
                    'Double Tap', 'Crippling Poison', 'Cloak And Dagger', 'Storm of Steel', 'Deadly Poison',
                    'Leg Sweep', 'Bullet Time', 'Catalyst', 'Tactician', 'Blade Dance', 'Deflect', 'Night Terror',
                    'Expertise', 'Blur', 'Setup', 'Burst', 'Acrobatics', 'Doppelganger', 'Adrenaline',
                    'Calculated Gamble', 'Escape Plan', 'Terror', 'Phantasmal Killer', 'Malaise', 'Reflex', 'Survivor',
                    'Defend_G', 'Corpse Explosion', 'Venomology', 'Bouncing Flask', 'Backflip', 'Outmaneuver',
                    'Concentrate', 'Prepared', 'PiercingWail', 'Distraction', 'Dodge and Roll', 'Genetic Algorithm',
                    'Zap', 'Steam Power', 'Fission', 'Glacier', 'Consume', 'Redo', 'Fusion', 'Amplify', 'Reboot',
                    'Aggregate', 'Chaos', 'Stack', 'Seek', 'Rainbow', 'Chill', 'BootSequence', 'Coolheaded', 'Tempest',
                    'Turbo', 'Undo', 'Force Field', 'Darkness', 'Double Energy', 'Reinforced Body', 'Conserve Battery',
                    'Defend_B', 'Dualcast', 'Auto Shields', 'Reprogram', 'Hologram', 'Leap', 'Recycle', 'Skim',
                    'White Noise', 'Multi-Cast', 'Steam', 'DeusExMachina', 'Vengeance', 'Sanctity', 'Halt', 'Protect',
                    'Indignation', 'ThirdEye', 'ForeignInfluence', 'Crescendo', 'SpiritShield', 'ClearTheMind',
                    'EmptyBody', 'WreathOfFlame', 'Collect', 'InnerPeace', 'Omniscience', 'Wish', 'DeceiveReality',
                    'Alpha', 'Vault', 'Scrawl', 'Blasphemy', 'Defend_P', 'WaveOfTheHand', 'Meditate', 'Perseverance',
                    'Swivel', 'Worship', 'Vigilance', 'PathToVictory', 'Evaluate', 'EmptyMind', 'Prostrate',
                    'ConjureBlade', 'Judgement', 'Pray', 'Beta', 'Dark Shackles', 'J.A.X.', 'PanicButton', 'Trip',
                    'FameAndFortune', 'Impatience', 'The Bomb', 'Insight', 'Miracle', 'Blind', 'Bandage Up',
                    'Secret Technique', 'Deep Breath', 'Violence', 'Secret Weapon', 'Apotheosis', 'Forethought',
                    'Enlightenment', 'Purity', 'Panacea', 'Transmutation', 'Ghostly', 'Chrysalis', 'Discovery',
                    'Finesse', 'Master of Strategy', 'Good Instincts', 'Jack Of All Trades', 'Safety', 'Metamorphosis',
                    'Thinking Ahead', 'Madness'}
BASE_GAME_POWERS = {'Inflame', 'Brutality', 'Juggernaut', 'Berserk', 'Metallicize', 'Combust', 'Dark Embrace',
                    'Barricade', 'Feel No Pain', 'Corruption', 'Rupture', 'Demon Form', 'Fire Breathing', 'Evolve',
                    'A Thousand Cuts', 'After Image', 'Tools of the Trade', 'Caltrops', 'Wraith Form v2', 'Envenom',
                    'Well Laid Plans', 'Noxious Fumes', 'Infinite Blades', 'Accuracy', 'Footwork', 'Storm',
                    'Hello World', 'Creative AI', 'Echo Form', 'Self Repair', 'Loop', 'Static Discharge', 'Heatsinks',
                    'Buffer', 'Electrodynamics', 'Machine Learning', 'Biased Cognition', 'Capacitor', 'Defragment',
                    'Wireheading', 'BattleHymn', 'DevaForm', 'LikeWater', 'Establishment', 'Fasting2', 'Adaptation',
                    'MentalFortress', 'Study', 'Devotion', 'Nirvana', 'MasterReality', 'Sadistic Nature', 'LiveForever',
                    'BecomeAlmighty', 'Panache', 'Mayhem', 'Magnetism', 'Omega'}
BASE_GAME_CURSES = {'Regret', 'Writhe', 'AscendersBane', 'Decay', 'Necronomicurse', 'Pain', 'Parasite', 'Doubt',
                    'Injury', 'Clumsy', 'CurseOfTheBell', 'Normality', 'Pride', 'Shame'}

BASE_GAME_CARDS_AND_UPGRADES = {'A Thousand Cuts', 'A Thousand Cuts+1', 'Accuracy', 'Accuracy+1', 'Acrobatics',
                                'Acrobatics+1', 'Adaptation', 'Adaptation+1', 'Adrenaline', 'Adrenaline+1',
                                'After Image', 'After Image+1', 'Aggregate', 'Aggregate+1', 'All For One',
                                'All For One+1', 'All Out Attack', 'All Out Attack+1', 'Alpha', 'Alpha+1', 'Amplify',
                                'Amplify+1', 'Anger', 'Anger+1', 'Apotheosis', 'Apotheosis+1', 'Armaments',
                                'Armaments+1', 'AscendersBane', 'Auto Shields', 'Auto Shields+1', 'Backflip',
                                'Backflip+1', 'Backstab', 'Backstab+1', 'Ball Lightning', 'Ball Lightning+1',
                                'Bandage Up', 'Bandage Up+1', 'Bane', 'Bane+1', 'Barrage', 'Barrage+1', 'Barricade',
                                'Barricade+1', 'Bash', 'Bash+1', 'Battle Trance', 'Battle Trance+1', 'BattleHymn',
                                'BattleHymn+1', 'Beam Cell', 'Beam Cell+1', 'BecomeAlmighty', 'BecomeAlmighty+1',
                                'Berserk', 'Berserk+1', 'Beta', 'Beta+1', 'Biased Cognition', 'Biased Cognition+1',
                                'Bite', 'Bite+1', 'Blade Dance', 'Blade Dance+1', 'Blasphemy', 'Blasphemy+1', 'Blind',
                                'Blind+1', 'Blizzard', 'Blizzard+1', 'Blood for Blood', 'Blood for Blood+1',
                                'Bloodletting', 'Bloodletting+1', 'Bludgeon', 'Bludgeon+1', 'Blur', 'Blur+1',
                                'Body Slam', 'Body Slam+1', 'BootSequence', 'BootSequence+1', 'Bouncing Flask',
                                'Bouncing Flask+1', 'BowlingBash', 'BowlingBash+1', 'Brilliance', 'Brilliance+1',
                                'Brutality', 'Brutality+1', 'Buffer', 'Buffer+1', 'Bullet Time', 'Bullet Time+1',
                                'Burn', 'Burn+1', 'Burning Pact', 'Burning Pact+1', 'Burst', 'Burst+1',
                                'Calculated Gamble', 'Calculated Gamble+1', 'Caltrops', 'Caltrops+1', 'Capacitor',
                                'Capacitor+1', 'Carnage', 'Carnage+1', 'CarveReality', 'CarveReality+1', 'Catalyst',
                                'Catalyst+1', 'Chaos', 'Chaos+1', 'Chill', 'Chill+1', 'Choke', 'Choke+1', 'Chrysalis',
                                'Chrysalis+1', 'Clash', 'Clash+1', 'ClearTheMind', 'ClearTheMind+1', 'Cleave',
                                'Cleave+1', 'Cloak And Dagger', 'Cloak And Dagger+1', 'Clothesline', 'Clothesline+1',
                                'Clumsy', 'Cold Snap', 'Cold Snap+1', 'Collect', 'Collect+1', 'Combust', 'Combust+1',
                                'Compile Driver', 'Compile Driver+1', 'Concentrate', 'Concentrate+1', 'Conclude',
                                'Conclude+1', 'ConjureBlade', 'ConjureBlade+1', 'Consecrate', 'Consecrate+1',
                                'Conserve Battery', 'Conserve Battery+1', 'Consume', 'Consume+1', 'Coolheaded',
                                'Coolheaded+1', 'Core Surge', 'Core Surge+1', 'Corpse Explosion', 'Corpse Explosion+1',
                                'Corruption', 'Corruption+1', 'Creative AI', 'Creative AI+1', 'Crescendo',
                                'Crescendo+1', 'Crippling Poison', 'Crippling Poison+1', 'CrushJoints', 'CrushJoints+1',
                                'CurseOfTheBell', 'CutThroughFate', 'CutThroughFate+1', 'Dagger Spray',
                                'Dagger Spray+1', 'Dagger Throw', 'Dagger Throw+1', 'Dark Embrace', 'Dark Embrace+1',
                                'Dark Shackles', 'Dark Shackles+1', 'Darkness', 'Darkness+1', 'Dash', 'Dash+1', 'Dazed',
                                'Dazed+1', 'Deadly Poison', 'Deadly Poison+1', 'Decay', 'DeceiveReality',
                                'DeceiveReality+1', 'Deep Breath', 'Deep Breath+1', 'Defend', 'Defend+1', 'Deflect',
                                'Deflect+1', 'Defragment', 'Defragment+1', 'Demon Form', 'Demon Form+1',
                                'DeusExMachina', 'DeusExMachina+1', 'DevaForm', 'DevaForm+1', 'Devotion', 'Devotion+1',
                                'Die Die Die', 'Die Die Die+1', 'Disarm', 'Disarm+1', 'Discovery', 'Discovery+1',
                                'Distraction', 'Distraction+1', 'Dodge and Roll', 'Dodge and Roll+1', 'Doom and Gloom',
                                'Doom and Gloom+1', 'Doppelganger', 'Doppelganger+1', 'Double Energy',
                                'Double Energy+1', 'Double Tap', 'Double Tap+1', 'Doubt', 'Dramatic Entrance',
                                'Dramatic Entrance+1', 'Dropkick', 'Dropkick+1', 'Dual Wield', 'Dual Wield+1',
                                'Dualcast', 'Dualcast+1', 'Echo Form', 'Echo Form+1', 'Electrodynamics',
                                'Electrodynamics+1', 'EmptyBody', 'EmptyBody+1', 'EmptyFist', 'EmptyFist+1',
                                'EmptyMind', 'EmptyMind+1', 'Endless Agony', 'Endless Agony+1', 'Enlightenment',
                                'Enlightenment+1', 'Entrench', 'Entrench+1', 'Envenom', 'Envenom+1', 'Eruption',
                                'Eruption+1', 'Escape Plan', 'Escape Plan+1', 'Establishment', 'Establishment+1',
                                'Evaluate', 'Evaluate+1', 'Eviscerate', 'Eviscerate+1', 'Evolve', 'Evolve+1', 'Exhume',
                                'Exhume+1', 'Expertise', 'Expertise+1', 'Expunger', 'Expunger+1', 'FTL', 'FTL+1',
                                'FameAndFortune', 'FameAndFortune+1', 'Fasting2', 'Fasting2+1', 'FearNoEvil',
                                'FearNoEvil+1', 'Feed', 'Feed+1', 'Feel No Pain', 'Feel No Pain+1', 'Fiend Fire',
                                'Fiend Fire+1', 'Finesse', 'Finesse+1', 'Finisher', 'Finisher+1', 'Fire Breathing',
                                'Fire Breathing+1', 'Fission', 'Fission+1', 'Flame Barrier', 'Flame Barrier+1',
                                'Flash of Steel', 'Flash of Steel+1', 'Flechettes', 'Flechettes+1', 'Flex', 'Flex+1',
                                'FlurryOfBlows', 'FlurryOfBlows+1', 'Flying Knee', 'Flying Knee+1', 'FlyingSleeves',
                                'FlyingSleeves+1', 'FollowUp', 'FollowUp+1', 'Footwork', 'Footwork+1', 'Force Field',
                                'Force Field+1', 'ForeignInfluence', 'ForeignInfluence+1', 'Forethought',
                                'Forethought+1', 'Fusion', 'Fusion+1', 'Gash', 'Gash+1', 'Genetic Algorithm',
                                'Genetic Algorithm+1', 'Ghostly', 'Ghostly Armor', 'Ghostly Armor+1', 'Ghostly+1',
                                'Glacier', 'Glacier+1', 'Glass Knife', 'Glass Knife+1', 'Go for the Eyes',
                                'Go for the Eyes+1', 'Good Instincts', 'Good Instincts+1', 'Grand Finale',
                                'Grand Finale+1', 'Halt', 'Halt+1', 'HandOfGreed', 'HandOfGreed+1', 'Havoc', 'Havoc+1',
                                'Headbutt', 'Headbutt+1', 'Heatsinks', 'Heatsinks+1', 'Heavy Blade', 'Heavy Blade+1',
                                'Heel Hook', 'Heel Hook+1', 'Hello World', 'Hello World+1', 'Hemokinesis',
                                'Hemokinesis+1', 'Hologram', 'Hologram+1', 'Hyperbeam', 'Hyperbeam+1', 'Immolate',
                                'Immolate+1', 'Impatience', 'Impatience+1', 'Impervious', 'Impervious+1', 'Indignation',
                                'Indignation+1', 'Infernal Blade', 'Infernal Blade+1', 'Infinite Blades',
                                'Infinite Blades+1', 'Inflame', 'Inflame+1', 'Injury', 'InnerPeace', 'InnerPeace+1',
                                'Insight', 'Insight+1', 'Intimidate', 'Intimidate+1', 'Iron Wave', 'Iron Wave+1',
                                'J.A.X.', 'J.A.X.+1', 'Jack Of All Trades', 'Jack Of All Trades+1', 'Judgement',
                                'Judgement+1', 'Juggernaut', 'Juggernaut+1', 'JustLucky', 'JustLucky+1', 'Leap',
                                'Leap+1', 'Leg Sweep', 'Leg Sweep+1', 'LessonLearned', 'LessonLearned+1', 'LikeWater',
                                'LikeWater+1', 'Limit Break', 'Limit Break+1', 'LiveForever', 'LiveForever+1', 'Lockon',
                                'Lockon+1', 'Loop', 'Loop+1', 'Machine Learning', 'Machine Learning+1', 'Madness',
                                'Madness+1', 'Magnetism', 'Magnetism+1', 'Malaise', 'Malaise+1', 'Master of Strategy',
                                'Master of Strategy+1', 'MasterReality', 'MasterReality+1', 'Masterful Stab',
                                'Masterful Stab+1', 'Mayhem', 'Mayhem+1', 'Meditate', 'Meditate+1', 'Melter',
                                'Melter+1', 'MentalFortress', 'MentalFortress+1', 'Metallicize', 'Metallicize+1',
                                'Metamorphosis', 'Metamorphosis+1', 'Meteor Strike', 'Meteor Strike+1', 'Mind Blast',
                                'Mind Blast+1', 'Miracle', 'Miracle+1', 'Multi-Cast', 'Multi-Cast+1', 'Necronomicurse',
                                'Neutralize', 'Neutralize+1', 'Night Terror', 'Night Terror+1', 'Nirvana', 'Nirvana+1',
                                'Normality', 'Noxious Fumes', 'Noxious Fumes+1', 'Offering', 'Offering+1', 'Omega',
                                'Omega+1', 'Omniscience', 'Omniscience+1', 'Outmaneuver', 'Outmaneuver+1', 'Pain',
                                'Panacea', 'Panacea+1', 'Panache', 'Panache+1', 'PanicButton', 'PanicButton+1',
                                'Parasite', 'PathToVictory', 'PathToVictory+1', 'Perfected Strike',
                                'Perfected Strike+1', 'Perseverance', 'Perseverance+1', 'Phantasmal Killer',
                                'Phantasmal Killer+1', 'PiercingWail', 'PiercingWail+1', 'Poisoned Stab',
                                'Poisoned Stab+1', 'Pommel Strike', 'Pommel Strike+1', 'Power Through',
                                'Power Through+1', 'Pray', 'Pray+1', 'Predator', 'Predator+1', 'Prepared', 'Prepared+1',
                                'Pride', 'Prostrate', 'Prostrate+1', 'Protect', 'Protect+1', 'Pummel', 'Pummel+1',
                                'Purity', 'Purity+1', 'Quick Slash', 'Quick Slash+1', 'Rage', 'Rage+1', 'Ragnarok',
                                'Ragnarok+1', 'Rainbow', 'Rainbow+1', 'Rampage', 'Rampage+1', 'ReachHeaven',
                                'ReachHeaven+1', 'Reaper', 'Reaper+1', 'Reboot', 'Reboot+1', 'Rebound', 'Rebound+1',
                                'Reckless Charge', 'Reckless Charge+1', 'Recycle', 'Recycle+1', 'Redo', 'Redo+1',
                                'Reflex', 'Reflex+1', 'Regret', 'Reinforced Body', 'Reinforced Body+1', 'Reprogram',
                                'Reprogram+1', 'Riddle With Holes', 'Riddle With Holes+1', 'Rip and Tear',
                                'Rip and Tear+1', 'RitualDagger', 'RitualDagger+1', 'Rupture', 'Rupture+1',
                                'Sadistic Nature', 'Sadistic Nature+1', 'Safety', 'Safety+1', 'Sanctity', 'Sanctity+1',
                                'SandsOfTime', 'SandsOfTime+1', 'SashWhip', 'SashWhip+1', 'Scrape', 'Scrape+1',
                                'Scrawl', 'Scrawl+1', 'Searing Blow', 'Searing Blow+1', 'Searing Blow+2',
                                'Searing Blow+3', 'Searing Blow+4', 'Searing Blow+5', 'Searing Blow+6',
                                'Searing Blow+7', 'Searing Blow+8', 'Searing Blow+9', 'Searing Blow+10',
                                'Searing Blow+11', 'Searing Blow+12', 'Searing Blow+13', 'Searing Blow+14',
                                'Searing Blow+16', 'Searing Blow+17', 'Second Wind', 'Second Wind+1',
                                'Secret Technique', 'Secret Technique+1', 'Secret Weapon', 'Secret Weapon+1',
                                'Seeing Red', 'Seeing Red+1', 'Seek', 'Seek+1', 'Self Repair', 'Self Repair+1',
                                'Sentinel', 'Sentinel+1', 'Setup', 'Setup+1', 'Sever Soul', 'Sever Soul+1', 'Shame',
                                'Shiv', 'Shiv+1', 'Shockwave', 'Shockwave+1', 'Shrug It Off', 'Shrug It Off+1',
                                'SignatureMove', 'SignatureMove+1', 'Skewer', 'Skewer+1', 'Skim', 'Skim+1', 'Slice',
                                'Slice+1', 'Slimed', 'Slimed+1', 'Smite', 'Smite+1', 'SpiritShield', 'SpiritShield+1',
                                'Spot Weakness', 'Spot Weakness+1', 'Stack', 'Stack+1', 'Static Discharge',
                                'Static Discharge+1', 'Steam', 'Steam Power', 'Steam Power+1', 'Steam+1', 'Storm',
                                'Storm of Steel', 'Storm of Steel+1', 'Storm+1', 'Streamline', 'Streamline+1', 'Strike',
                                'Strike+1', 'Study', 'Study+1', 'Sucker Punch', 'Sucker Punch+1', 'Sunder', 'Sunder+1',
                                'Survivor', 'Survivor+1', 'Sweeping Beam', 'Sweeping Beam+1', 'Swift Strike',
                                'Swift Strike+1', 'Swivel', 'Swivel+1', 'Sword Boomerang', 'Sword Boomerang+1',
                                'Tactician', 'Tactician+1', 'TalkToTheHand', 'TalkToTheHand+1', 'Tantrum', 'Tantrum+1',
                                'Tempest', 'Tempest+1', 'Terror', 'Terror+1', 'The Bomb', 'The Bomb+1',
                                'Thinking Ahead', 'Thinking Ahead+1', 'ThirdEye', 'ThirdEye+1', 'ThroughViolence',
                                'ThroughViolence+1', 'Thunder Strike', 'Thunder Strike+1', 'Thunderclap',
                                'Thunderclap+1', 'Tools of the Trade', 'Tools of the Trade+1', 'Transmutation',
                                'Transmutation+1', 'Trip', 'Trip+1', 'True Grit', 'True Grit+1', 'Turbo', 'Turbo+1',
                                'Twin Strike', 'Twin Strike+1', 'Underhanded Strike', 'Underhanded Strike+1', 'Undo',
                                'Undo+1', 'Unload', 'Unload+1', 'Uppercut', 'Uppercut+1', 'Vault', 'Vault+1',
                                'Vengeance', 'Vengeance+1', 'Venomology', 'Venomology+1', 'Vigilance', 'Vigilance+1',
                                'Violence', 'Violence+1', 'Void', 'Void+1', 'Wallop', 'Wallop+1', 'Warcry', 'Warcry+1',
                                'WaveOfTheHand', 'WaveOfTheHand+1',
                                'Weave', 'Weave+1', 'Well Laid Plans', 'Well Laid Plans+1', 'WheelKick', 'WheelKick+1',
                                'Whirlwind', 'Whirlwind+1', 'White Noise', 'White Noise+1', 'Wild Strike',
                                'Wild Strike+1', 'WindmillStrike', 'WindmillStrike+1', 'Wireheading', 'Wireheading+1',
                                'Wish', 'Wish+1', 'Worship', 'Worship+1', 'Wound', 'Wound+1', 'Wraith Form v2',
                                'Wraith Form v2+1', 'WreathOfFlame', 'WreathOfFlame+1', 'Writhe', 'Zap', 'Zap+1',
                                'Strike_R', 'Strike_R+1', 'Strike_G', 'Strike_G+1', 'Strike_B', 'Strike_B+1',
                                'Strike_P', 'Strike_P+1', 'Defend_R', 'Defend_R+1', 'Defend_G', 'Defend_G+1',
                                'Defend_B', 'Defend_B+1', 'Defend_P', 'Defend_P+1'}


def process_runs(data_dir):
    file_not_opened = 0
    bad_file_count = 0
    total_file_count = 0
    file_not_processed_count = 0
    file_processed_count = 0
    file_master_not_match_count = 0
    fight_training_examples = list()

    count = 0
    tmp_dir = os.path.join('out', str(round(time.time())))
    os.mkdir(tmp_dir)
    for root, dirs, files in os.walk(data_dir):
        for fname in files:
            count += 1
            if len(fight_training_examples) > 40000:
                print('Saving batch')
                write_file_name = f'data_{round(time.time())}.json'
                write_file(fight_training_examples, os.path.join(tmp_dir, write_file_name))
                fight_training_examples.clear()
                print('Wrote batch to file')
                print('Garbage collecting')
                gc.collect()
                print('Finished garbage collecting')

            if count % 10000 == 0:
                gc.collect()

            if count % 200 == 0:
                print(
                    f'\n\n\nFiles not able to open: {file_not_opened} => {((file_not_opened / total_file_count) * 100):.1f} %')
                print(
                    f'Files filtered with pre-filter: {bad_file_count} => {((bad_file_count / total_file_count) * 100):.1f} %')
                print(
                    f'Files SUCCESSFULLY processed: {file_processed_count} => {((file_processed_count / total_file_count) * 100):.1f} %')
                print(
                    f'Files with master deck not matching created deck: {file_master_not_match_count} => {((file_master_not_match_count / total_file_count) * 100):.1f} %')
                print(
                    f'Files not processed: {file_not_processed_count} => {((file_not_processed_count / total_file_count) * 100):.1f} %')
                print(f'Total files: {total_file_count}')
                print(f'Number of Training Examples in batch: {len(fight_training_examples)}')
            path = os.path.join(root, fname)
            if path.endswith(".run.json"):
                total_file_count += 1
                try:
                    with open(path, 'r', encoding='utf8') as file:
                        data = json.load(file)
                        if is_bad_file(data):
                            bad_file_count += 1
                        else:
                            if 'ReplayTheSpireMod:Calculation Training+1' in data['master_deck']:
                                print('Modded file found')
                                print(data)
                                print(path)
                            processed_run = list()
                            try:
                                processed_run.clear()
                                processed_run.extend(process_run(data))
                                file_processed_count += 1
                                fight_training_examples.extend(processed_run)
                            except RuntimeError as e:
                                file_master_not_match_count += 1
                                # print(f'{path}\n')
                                pass
                            except Exception as e:
                                file_not_processed_count += 1
                                # print(path)
                except Exception as e:
                    file_not_opened += 1

    print(f'\n\n\nFiles not able to open: {file_not_opened} => {((file_not_opened / total_file_count) * 100):.1f} %')
    print(f'Files filtered with pre-filter: {bad_file_count} => {((bad_file_count / total_file_count) * 100):.1f} %')
    print(
        f'Files SUCCESSFULLY processed: {file_processed_count} => {((file_processed_count / total_file_count) * 100):.1f} %')
    print(
        f'Files with master deck not matching created deck: {file_master_not_match_count} => {((file_master_not_match_count / total_file_count) * 100):.1f} %')
    print(
        f'Files not processed: {file_not_processed_count} => {((file_not_processed_count / total_file_count) * 100):.1f} %')
    print(f'Total files: {total_file_count}')
    print(f'Number of Training Examples: {len(fight_training_examples)}')
    write_file_name = f'data_{round(time.time())}.json'
    write_file(fight_training_examples, os.path.join(tmp_dir, write_file_name))


def process_run(data):
    # We actually want to win or maximize our score, not just minimize damage
    # This will also help account for higher-skilled players that are on A20 and thus probably making better choices
    score = data.get('score', 0)
    path_per_floor = data.get('path_per_floor')
    damage_taken = data.get('damage_taken')
    act_bosses = get_act_bosses(path_per_floor, damage_taken)

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
    unknown_cards_by_floor = dict()
    unknowns = (
        unknown_removes_by_floor, unknown_upgrades_by_floor, unknown_transforms_by_floor, unknown_cards_by_floor)

    processed_fights = list()
    for floor in range(0, data['floor_reached']):
        if floor in battle_stats_by_floor and floor != 1:
            fight_data = process_battle(data, battle_stats_by_floor[floor], potion_use_by_floor, current_deck,
                                        current_relics, floor, score, act_bosses, path_per_floor)
            processed_fights.append(fight_data)

        if floor in relics_by_floor:
            process_relics(relics_by_floor[floor], current_relics, data['relics'], floor, unknowns)

        if floor in card_choices_by_floor:
            process_card_choice(card_choices_by_floor[floor], current_deck, current_relics)

        if floor in campfire_choices_by_floor:
            restart_needed, new_data = try_process_data(
                partial(process_campfire_choice, campfire_choices_by_floor[floor], current_deck))
            if restart_needed:
                return process_run(new_data)

        if floor in purchases_by_floor:
            try_process_data(
                partial(process_purchases, purchases_by_floor[floor], current_deck, current_relics, data['relics'],
                        floor, unknowns))

        if floor in purges_by_floor:
            try_process_data(partial(process_purges, purges_by_floor[floor], current_deck))

        if floor in events_by_floor:
            try_process_data(
                partial(process_events, events_by_floor[floor], current_deck, current_relics, data['relics'], floor,
                        unknowns))

        if floor == 0:
            process_neow(data['neow_bonus'], current_relics, data['relics'], unknowns)

    current_deck.sort()
    master_deck = sorted(data['master_deck'])
    current_relics.sort()
    master_relics = sorted(data['relics'])
    if current_deck != master_deck or current_relics != master_relics:
        success, new_data = resolve_missing_data(current_deck, master_deck=data['master_deck'], unknowns=unknowns,
                                                 master_data=data)
        if success:
            return process_run(new_data)
        raise RuntimeError('Final decks or relics did not match')
    else:
        return processed_fights


def get_act_bosses(path_per_floor, damage_taken):
    boss_floors = set([floor + 1 for floor, event in enumerate(path_per_floor) if event == 'B'])
    act_bosses = {}
    for encounter in damage_taken:
        if encounter['floor'] in boss_floors:
            act_bosses[encounter['floor']] = encounter['enemies']
    return act_bosses


def try_process_data(func):
    try:
        func()
        return False, None
    except Exception as e:
        raise e


def process_battle(master_data, battle_stat, potion_use_by_floor, current_deck, current_relics, floor, score,
                   act_bosses, path_per_floor):
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

    next_boss_floor, fight_data['next_boss'] = get_next_boss(floor, act_bosses)
    fight_data['score'] = score
    fight_data['remaining_events_before_boss'] = get_remaining_encounters(floor, next_boss_floor, path_per_floor,
                                                                          encounter_type='?')
    fight_data['remaining_campfires_before_boss'] = get_remaining_encounters(floor, next_boss_floor, path_per_floor,
                                                                             encounter_type='R')
    fight_data['remaining_monsters_before_boss'] = get_remaining_encounters(floor, next_boss_floor, path_per_floor,
                                                                           encounter_type='M')
    fight_data['remaining_elites_before_boss'] = get_remaining_encounters(floor, next_boss_floor, path_per_floor,
                                                                          encounter_type='E')
    return fight_data


def get_next_boss(floor, act_bosses):
    next_boss_floor = 999
    next_boss = None
    for boss_floor, boss in act_bosses.items():
        if boss_floor - floor > 0 and boss_floor < next_boss_floor:
            next_boss_floor = boss_floor
            next_boss = boss
    return next_boss_floor, next_boss


def get_remaining_encounters(current_floor, next_boss_floor, path_per_floor, encounter_type=None):
    """
    Used to get the remaining floors of a certain type before the Act Boss.
    encounter_type can be within the following:
        'M' - monster
        '$' - shop
        'E' - elite
        'R' - rest (AKA campfire)
        'BOSS' - act boss
        'T' - treasure
        '?' - event

    :param current_floor:
    :param next_boss_floor:
    :param path_per_floor:
    :param encounter_type:
    :return:
    """
    num_encounter_floors = len([floor + 1 for floor, event in enumerate(path_per_floor)
                                if event == encounter_type and current_floor < floor < next_boss_floor])
    return num_encounter_floors


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


def process_relics(relics, current_relics, master_relics, floor, unknowns):
    for r in relics:
        obtain_relic(r, current_relics, master_relics, floor, unknowns)


def process_campfire_choice(campfire_data, current_deck):
    choice = campfire_data['key']
    if choice == 'SMITH':
        upgrade_card(current_deck, campfire_data['data'])
    if choice == 'PURGE':
        current_deck.remove(campfire_data['data'])


def process_purchases(purchase_data, current_deck, current_relics, master_relics, floor, unknowns):
    purchased_cards = [x for x in purchase_data if x not in BASE_GAME_RELICS and x not in BASE_GAME_POTIONS]
    purchased_relics = [x for x in purchase_data if x not in purchased_cards and x not in BASE_GAME_POTIONS]
    current_deck.extend(purchased_cards)
    for r in purchased_relics:
        obtain_relic(r, current_relics, master_relics, floor, unknowns)


def process_purges(purge_data, current_deck):
    for card in purge_data:
        current_deck.remove(card)


def process_events(event_data, current_deck, current_relics, master_relics, floor, unknowns):
    if 'relics_obtained' in event_data:
        for r in event_data['relics_obtained']:
            obtain_relic(r, current_relics, master_relics, floor, unknowns)
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
    if 'event_name' in event_data and event_data['event_name'] == 'Vampires':
        current_deck[:] = [x for x in current_deck if not x.startswith('Strike')]


def process_neow(neow_bonus, current_relics, master_relics, unknowns):
    unknown_removes_by_floor, unknown_upgrades_by_floor, unknown_transforms_by_floor, unknown_cards_by_floor = unknowns
    if neow_bonus == 'ONE_RARE_RELIC' or neow_bonus == 'RANDOM_COMMON_RELIC':
        current_relics.append(master_relics[1])
    if neow_bonus == 'BOSS_RELIC':
        current_relics[0] = master_relics[0]
    if neow_bonus == 'THREE_ENEMY_KILL':
        current_relics.append('NeowsBlessing')
    if neow_bonus == 'UPGRADE_CARD':
        unknown_upgrades_by_floor[0] = [{'type': 'unknown'}]
    if neow_bonus == 'REMOVE_CARD':
        unknown_removes_by_floor[0] = 1
    if neow_bonus == 'REMOVE_TWO':
        unknown_removes_by_floor[0] = 2
    if neow_bonus == 'TRANSFORM_CARD':
        unknown_transforms_by_floor[0] = 1
    if neow_bonus == 'THREE_CARDS':
        unknown_cards_by_floor[0] = [{'type': 'unknown'}]
    if neow_bonus == 'THREE_RARE_CARDS' or neow_bonus == 'ONE_RANDOM_RARE_CARD':
        unknown_cards_by_floor[0] = [{'type': 'rare'}]


def upgrade_card(current_deck, card_to_upgrade):
    card_to_upgrade_index = current_deck.index(card_to_upgrade)
    # if 'earing' in card_to_upgrade:
    # print(f'Probably Searing Blow id: {card_to_upgrade}')
    current_deck[card_to_upgrade_index] += '+1'


def obtain_relic(relic_to_obtain, current_relics, master_relics, floor, unknowns):
    unknown_removes_by_floor, unknown_upgrades_by_floor, unknown_transforms_by_floor, unknown_cards_by_floor = unknowns
    if relic_to_obtain == 'Black Blood':
        current_relics[0] = 'Black Blood'
        return
    if relic_to_obtain == 'Ring of the Serpent':
        current_relics[0] = 'Ring of the Serpent'
        return
    if relic_to_obtain == 'FrozenCore':
        current_relics[0] = 'FrozenCore'
        return
    if relic_to_obtain == 'Calling Bell':
        current_relics.extend(master_relics[len(current_relics) + 1:len(current_relics) + 4])
    if relic_to_obtain == 'Empty Cage':
        unknown_removes_by_floor[floor] = 2
    if relic_to_obtain == 'Whetstone':
        unknown_upgrades_by_floor[floor] = [{'type': 'attack'}, {'type': 'attack'}]
    if relic_to_obtain == 'War Paint':
        unknown_upgrades_by_floor[floor] = [{'type': 'skill'}, {'type': 'skill'}]
    current_relics.append(relic_to_obtain)


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


def resolve_missing_data(current_deck, master_deck, unknowns, master_data):
    unknown_removes_by_floor, unknown_upgrades_by_floor, unknown_transforms_by_floor, unknown_cards_by_floor = unknowns
    if current_deck != master_deck:
        if len(current_deck) > len(master_deck) and len(unknown_removes_by_floor) == 1 and len(
                unknown_upgrades_by_floor) == 0 and len(unknown_transforms_by_floor) == 0 and len(
            unknown_cards_by_floor) == 0:
            differences = list((Counter(current_deck) - Counter(master_deck)).elements())
            for floor, number_of_removes in unknown_removes_by_floor.items():
                if len(differences) == number_of_removes:
                    master_data['items_purged'].extend(differences)
                    for i in range(number_of_removes):
                        items_purched_floors = master_data['items_purged_floors']
                        items_purched_floors.append(floor)
                    return True, master_data
        elif len(current_deck) == len(master_deck) and len(unknown_upgrades_by_floor) == 1 and len(
                unknown_removes_by_floor) == 0 and len(unknown_transforms_by_floor) == 0 and len(
            unknown_cards_by_floor) == 0:
            diff1 = list((Counter(current_deck) - Counter(master_deck)).elements())
            diff2 = list((Counter(master_deck) - Counter(current_deck)).elements())
            if len(diff1) == len(diff2):
                upgraded_names_of_unupgraded_cards = [x + "+1" for x in diff1]
                if upgraded_names_of_unupgraded_cards == diff2:
                    for floor, upgrade_types in unknown_upgrades_by_floor.items():
                        if len(diff1) == len(upgrade_types):
                            for unupgraded_card in diff1:
                                master_data['campfire_choices'].append(
                                    {"data": unupgraded_card, "floor": floor, "key": "SMITH"})
                            return True, master_data

    return False, None


BUILD_VERSION_REGEX = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}$')


def valid_build_number(string, character):
    pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    if pattern.match(string):
        m = re.search('(.+)-(.+)-(.+)', string)
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))

        date = datetime.date(year, month, day)
        if date >= datetime.date(2020, 1, 16):
            return True
        elif character in ['IRONCLAD', 'THE_SILENT', 'DEFECT'] and date >= datetime.date(2019, 1, 23):
            return True

    return False


def is_bad_file(data):
    # Corrupted files
    necessary_fields = ['damage_taken', 'event_choices', 'card_choices', 'relics_obtained', 'campfire_choices',
                        'items_purchased', 'item_purchase_floors', 'items_purged', 'items_purged_floors',
                        'character_chosen', 'boss_relics', 'floor_reached', 'master_deck', 'relics']
    for field in necessary_fields:
        if field not in data:
            # print(f'File missing field: {field}')
            return True

    # Modded games
    key = 'character_chosen'
    if key not in data or data[key] not in ['IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER']:
        # print(f'Modded character: {data[key]}')
        return True

    key = 'master_deck'
    if key not in data or set(data[key]).issubset(BASE_GAME_CARDS_AND_UPGRADES) is False:
        # deck = data[key]
        # print(f'Modded file. Cards: {deck - BASE_GAME_CARDS_AND_UPGRADES}')
        return True

    key = 'relics'
    if key not in data or set(data[key]).issubset(BASE_GAME_RELICS) is False:
        return True

    # Watcher files since full release of watcher (v2.0) and ironclad, silent, defect since v1.0
    key = 'build_version'
    if key not in data or valid_build_number(data[key], data['character_chosen']) is False:
        return True

    # Non standard runs
    key = 'is_trial'
    if key not in data or data[key] is True:
        return True

    key = 'is_daily'
    if key not in data or data[key] is True:
        return True

    key = 'daily_mods'
    if key in data:
        return True

    key = 'chose_seed'
    if key not in data or data[key] is True:
        return True

    # Endless mode
    key = 'is_endless'
    if key not in data or data[key] is True:
        return True

    key = 'circlet_count'
    if key not in data or data[key] > 0:
        return True

    key = 'floor_reached'
    if key not in data or data[key] > 60:
        return True

    # Really bad players or give ups
    key = 'floor_reached'
    if key not in data or data[key] < 4:
        return True

    key = 'score'
    if key not in data or data[key] < 10:
        return True

    key = 'player_experience'
    if key not in data or data[key] < 100:
        return True


def write_file(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def process_single_file(data_dir, filename):
    with open(f"{data_dir}/{filename}", 'r') as file:
        data = json.load(file)
        result = process_run(data)
        print(f'Result: {result}')


directory = 'SpireLogs Data'
process_runs(directory)
# process_single_file(directory, '1546376628.run')

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
