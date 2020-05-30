import os
import json
import pprint


def process_run(data):
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
    for filename in os.listdir(data_dir):
        if filename.endswith(".run"):
            with open(f"{data_dir}/{filename}", 'r') as file:
                data = json.load(file)
                # Ascension 20 Heart win or loss
                if data['ascension_level'] == 20 and \
                        ((data['floor_reached'] == 56 and data['victory'] is False and data['killed_by'] == 'The Heart') or
                            (data['floor_reached'] == 57 and data['victory'] is True)):
                    runs.append(process_run(data))
    return runs


def write_file(data):
    with open('out/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


directory = '2019SpireRuns'
processed_runs = process_runs(directory)
# pprint.pprint(processed_runs[0])
write_file(processed_runs)

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