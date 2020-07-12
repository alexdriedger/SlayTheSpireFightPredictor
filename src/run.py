import json
import logging
from collections import Counter
from functools import partial

from main import BASE_GAME_ATTACKS, BASE_GAME_POTIONS, BASE_GAME_POWERS, BASE_GAME_RELICS, BASE_GAME_SKILLS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filemode='w+'
)
logger = logging.getLogger('run')


class Run:
    """
    Processes a single run.
    WIP. Currently reimplements all the methods that were used in main.py
    """

    def __init__(self, run_path):
        """

        :param run_path:
        """
        self.run_path = run_path
        self.run = self.load_run()
        self.stats_by_floor = self.get_by_floor()
        self.current_deck = self.get_starting_deck()
        self.current_relics = self.get_starting_relics()
        self.end_game_stats = self.get_end_game_stats()
        self.unknowns = {
            'unknown_removes_by_floor': {},
            'unknown_upgrades_by_floor': {},
            'unknown_transforms_by_floor': {},
            'unknown_cards_by_floor': {},
        }

    def load_run(self):
        with open(self.run_path, 'r', encoding='utf8') as file:
            data = json.load(file)
        return data

    def get_starting_relics(self):
        character = self.run.get('character_chosen')
        character_relics = {
            'IRONCLAD': ['Burning Blood'],
            'THE_SILENT': ['Ring of the Snake'],
            'DEFECT': ['Cracked Core'],
            'WATCHER': ['PureWater'],
        }
        return character_relics.get(character, logger.info(f'Unsupported character {character}'))

    def get_starting_deck(self):
        character = self.run.get('character_chosen')
        ascension = self.run.get('ascension_level')
        basic_deck = ['Strike', 'Strike', 'Strike', 'Strike', 'Defend', 'Defend', 'Defend', 'Defend']
        if character == 'IRONCLAD':
            basic_deck.extend(['Strike', 'Bash'])
            self.character_specific_basic_cards(basic_deck, '_R')
        elif character == 'THE_SILENT':
            basic_deck.extend(['Strike', 'Defend', 'Survivor', 'Neutralize'])
            self.character_specific_basic_cards(basic_deck, '_G')
        elif character == 'DEFECT':
            basic_deck.extend(['Zap', 'Dualcast'])
            self.character_specific_basic_cards(basic_deck, '_B')
        elif character == 'WATCHER':
            basic_deck.extend(['Eruption', 'Vigilance'])
            self.character_specific_basic_cards(basic_deck, '_P')
        else:
            logger.info(f'Unsupported character {character}')
        if ascension and ascension >= 10:
            basic_deck.append('AscendersBane')
        return basic_deck

    def character_specific_basic_cards(self, deck, suffix):
        for index, card in enumerate(deck):
            if card == 'Strike' or card == 'Defend':
                deck[index] = card + suffix

    def get_end_game_stats(self):
        end_game_stats = {
            'score': self.run.get('score', 0),
            'master_deck': self.run.get('master_deck'),
            'master_relics': self.run.get('relics'),
            'path_per_floor': self.run.get('path_per_floor'),
            'damage_taken': self.run.get('damage_taken'),
            'act_bosses': self.get_act_bosses(),
        }
        return end_game_stats

    def get_act_bosses(self):
        self.run.get('path_per_floor')
        boss_floors = set([floor + 1 for floor, event in enumerate(self.run.get('path_per_floor', [])) if event == 'B'])
        act_bosses = {}
        for encounter in self.run.get('damage_taken', []):
            if encounter['floor'] in boss_floors:
                act_bosses[encounter['floor']] = encounter['enemies']
        return act_bosses

    def get_by_floor(self):
        stats_by_floor = {
            'battle_stats_by_floor': {battle_stat['floor']: battle_stat for battle_stat in
                                      self.run['damage_taken']},
            'events_by_floor': {event_stat['floor']: event_stat for event_stat in
                                self.run['event_choices']},
            'card_choices_by_floor': {card_choice['floor']: card_choice for card_choice in
                                      self.run['card_choices']},
            'relics_by_floor': self.get_relics_by_floor(),
            'campfire_choices_by_floor': {campfire_choice['floor']: campfire_choice for campfire_choice in
                                          self.run['campfire_choices']},
            'purchases_by_floor': self.get_stat_with_separate_floor_list('items_purchased',
                                                                         'item_purchase_floors'),
            'purges_by_floor': self.get_stat_with_separate_floor_list('items_purged',
                                                                      'items_purged_floors'),
            'potion_use_by_floor': list(set(self.run['potions_floor_usage']))
        }
        return stats_by_floor

    def get_relics_by_floor(self):
        relics_by_floor = self.get_stats_by_floor_with_list('relics_obtained')
        boss_relics = self.run['boss_relics']
        num_boss_relics = len(boss_relics)
        if num_boss_relics >= 1:
            picked_relic = boss_relics[0]['picked']
            if picked_relic != 'SKIP':
                relics_by_floor[17] = [picked_relic]
        if num_boss_relics == 2:
            picked_relic = boss_relics[1]['picked']
            if picked_relic != 'SKIP':
                relics_by_floor[34] = [picked_relic]
        return relics_by_floor

    def get_stats_by_floor_with_list(self, data_key):
        stats_by_floor = dict()
        if data_key in self.run:
            for stat in self.run[data_key]:
                floor = stat['floor']
                if floor not in stats_by_floor:
                    stats_by_floor[floor] = list()
                stats_by_floor[floor].append(stat['key'])
        return stats_by_floor

    def get_stat_with_separate_floor_list(self, obtain_key, floor_key):
        stats_by_floor = dict()
        if obtain_key in self.run and floor_key in self.run and len(self.run[obtain_key]) == len(self.run[floor_key]):
            obtains = self.run[obtain_key]
            floors = self.run[floor_key]
            for index, obtain in enumerate(obtains):
                floor = floors[index]
                obtain = obtains[index]
                if floor not in stats_by_floor:
                    stats_by_floor[floor] = list()
                stats_by_floor[floor].append(obtain)
        return stats_by_floor

    def process_run(self):
        processed_fights = list()
        for floor in range(0, self.run['floor_reached']):
            if floor != 1:
                fight_data = self.process_battle(floor)
                processed_fights.append(fight_data)

            self.process_relics(floor)
            self.process_card_choice(floor)

            # TODO Better error handling here
            restart_needed = self.try_process_data(partial(self.process_campfire_choice))
            if restart_needed:
                return Run(self.run_path).process_run()

            self.try_process_data(partial(self.process_purchases, floor))
            self.try_process_data(partial(self.process_purges, floor))
            self.try_process_data(partial(self.process_events, floor))

            if floor == 0:
                self.process_neow()

        if self.current_deck != self.end_game_stats['master_deck'] or self.current_relics != self.end_game_stats[
            'master_relics']:
            success = self.resolve_missing_data()
            if success:
                return Run(self.run_path).process_run()
            raise RuntimeError('Final decks or relics did not match')
        else:
            return processed_fights

    def try_process_data(self, func):
        try:
            func()
            return False
        except Exception as e:
            raise e

    def process_battle(self, floor):
        fight_data = dict()
        battle_stat = self.stats_by_floor['battle_stats_by_floor'][floor]
        if battle_stat:
            fight_data['cards'] = list(self.current_deck)
            fight_data['relics'] = list(self.current_relics)
            fight_data['max_hp'] = self.run['max_hp_per_floor'][floor - 2]
            fight_data['entering_hp'] = self.run['current_hp_per_floor'][floor - 2]
            fight_data['character'] = self.run['character_chosen']
            fight_data['ascension'] = self.run['ascension_level']
            fight_data['enemies'] = battle_stat['enemies']
            fight_data['potion_used'] = floor in self.stats_by_floor['potion_use_by_floor']
            fight_data['floor'] = floor
            if self.run['current_hp_per_floor'] == 0:
                hp_change = battle_stat['damage']
            else:
                hp_change = self.run['current_hp_per_floor'][floor - 2] - self.run['current_hp_per_floor'][floor - 1]
            fight_data['damage_taken'] = hp_change

            next_boss_floor, fight_data['next_boss'] = self.get_next_boss(floor)
            fight_data['score'] = self.end_game_stats['score']
            fight_data['remaining_events_before_boss'] = self.get_remaining_encounters(floor, next_boss_floor,
                                                                                       encounter_type='?')
            fight_data['remaining_campfires_before_boss'] = self.get_remaining_encounters(floor, next_boss_floor,
                                                                                          encounter_type='R')
            fight_data['remaining_monsters_before_boss'] = self.get_remaining_encounters(floor, next_boss_floor,
                                                                                         encounter_type='M')
            fight_data['remaining_elites_before_boss'] = self.get_remaining_encounters(floor, next_boss_floor,
                                                                                       encounter_type='E')
            return fight_data

    def get_next_boss(self, floor):
        next_boss_floor = 999
        next_boss = None
        for boss_floor, boss in self.end_game_stats['act_bosses'].items():
            if boss_floor - floor > 0 and boss_floor < next_boss_floor:
                next_boss_floor = boss_floor
                next_boss = boss
        return next_boss_floor, next_boss

    def get_remaining_encounters(self, current_floor, next_boss_floor, encounter_type=None):
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
        path_per_floor = self.end_game_stats['path_per_floor']
        num_encounter_floors = len([floor + 1 for floor, event in enumerate(path_per_floor)
                                    if event == encounter_type and current_floor < floor < next_boss_floor])
        return num_encounter_floors

    def process_card_choice(self, floor):
        card_choice_data = self.stats_by_floor['card_choices_by_floor'].get(floor)
        if card_choice_data:
            picked_card = card_choice_data['picked']
            if picked_card != 'SKIP' and picked_card != 'Singing Bowl':
                if 'Molten Egg 2' in self.current_relics and picked_card in BASE_GAME_ATTACKS and picked_card[
                    -2] != '+1':
                    picked_card += '+1'
                if 'Toxic Egg 2' in self.current_relics and picked_card in BASE_GAME_SKILLS and picked_card[-2] != '+1':
                    picked_card += '+1'
                if 'Frozen Egg 2' in self.current_relics and picked_card in BASE_GAME_POWERS and picked_card[
                    -2] != '+1':
                    picked_card += '+1'
                self.current_deck.append(picked_card)

    def process_campfire_choice(self, floor):
        campfire_data = self.stats_by_floor['campfire_choices_by_floor'].get(floor)
        if campfire_data:
            choice = campfire_data['key']
            if choice == 'SMITH':
                self.upgrade_card(campfire_data['data'])
            if choice == 'PURGE':
                self.current_deck.remove(campfire_data['data'])

    def upgrade_card(self, card_to_upgrade):
        card_to_upgrade_index = self.current_deck.index(card_to_upgrade)
        # TODO Properly handle searing blow
        # if 'earing' in card_to_upgrade:
        # logger.info(f'Probably Searing Blow id: {card_to_upgrade}')
        self.current_deck[card_to_upgrade_index] += '+1'

    def process_purchases(self, floor):
        purchase_data = self.stats_by_floor['purchases_by_floor'].get(floor)
        if purchase_data:
            purchased_cards = [x for x in purchase_data if x not in BASE_GAME_RELICS and x not in BASE_GAME_POTIONS]
            purchased_relics = [x for x in purchase_data if x not in purchased_cards and x not in BASE_GAME_POTIONS]
            self.current_deck.extend(purchased_cards)
            for r in purchased_relics:
                self.obtain_relic(r, floor)

    def process_purges(self, floor):
        purge_data = self.stats_by_floor['purges_by_floor'].get(floor)
        if purge_data:
            for card in purge_data:
                self.current_deck.remove(card)

    def process_events(self, floor):
        event_data = self.stats_by_floor['events_by_floor'].get(floor)
        if event_data:
            if 'relics_obtained' in event_data:
                for r in event_data['relics_obtained']:
                    self.obtain_relic(r, floor)
            if 'relics_lost' in event_data:
                for relic in event_data['relics_lost']:
                    self.current_relics.remove(relic)
            if 'cards_obtained' in event_data:
                self.current_deck.extend(event_data['cards_obtained'])
            if 'cards_removed' in event_data:
                for card in event_data['cards_removed']:
                    self.current_deck.remove(card)
            if 'cards_upgraded' in event_data:
                for card in event_data['cards_upgraded']:
                    self.upgrade_card(card)
            if 'event_name' in event_data and event_data['event_name'] == 'Vampires':
                self.current_deck[:] = [x for x in self.current_deck if not x.startswith('Strike')]

    def process_neow(self):
        neow_bonus = self.run['neow_bonus']
        if neow_bonus == 'ONE_RARE_RELIC' or neow_bonus == 'RANDOM_COMMON_RELIC':
            self.current_relics.append(self.end_game_stats['master_relics'][1])
        elif neow_bonus == 'BOSS_RELIC':
            self.current_relics[0] = self.end_game_stats['master_relics'][0]
        elif neow_bonus == 'THREE_ENEMY_KILL':
            self.current_relics.append('NeowsBlessing')
        elif neow_bonus == 'UPGRADE_CARD':
            self.unknowns['unknown_upgrades_by_floor'][0] = [{'type': 'unknown'}]
        elif neow_bonus == 'REMOVE_CARD':
            self.unknowns['unknown_removes_by_floor'][0] = 1
        elif neow_bonus == 'REMOVE_TWO':
            self.unknowns['unknown_removes_by_floor'][0] = 2
        elif neow_bonus == 'TRANSFORM_CARD':
            self.unknowns['unknown_transforms_by_floor'][0] = 1
        elif neow_bonus == 'THREE_CARDS':
            self.unknowns['unknown_cards_by_floor'][0] = [{'type': 'unknown'}]
        elif neow_bonus == 'THREE_RARE_CARDS' or neow_bonus == 'ONE_RANDOM_RARE_CARD':
            self.unknowns['unknown_cards_by_floor'][0] = [{'type': 'rare'}]

    def resolve_missing_data(self):
        master_deck = self.end_game_stats['master_deck']
        if self.current_deck != master_deck:
            if len(self.current_deck) > len(master_deck) and len(
                    self.unknowns['unknown_removes_by_floor']) == 1 and len(
                self.unknowns['unknown_upgrades_by_floor']) == 0 and len(
                self.unknowns['unknown_transforms_by_floor']) == 0 and len(
                self.unknowns['unknown_cards_by_floor']) == 0:
                differences = list((Counter(self.current_deck) - Counter(master_deck)).elements())
                for floor, number_of_removes in self.unknowns['unknown_removes_by_floor'].items():
                    if len(differences) == number_of_removes:
                        self.run['items_purged'].extend(differences)
                        for i in range(number_of_removes):
                            items_purched_floors = self.run['items_purged_floors']
                            items_purched_floors.append(floor)
                        return True, self.run
            elif len(self.current_deck) == len(master_deck) and len(
                    self.unknowns['unknown_upgrades_by_floor']) == 1 and len(
                self.unknowns['unknown_removes_by_floor']) == 0 and len(
                self.unknowns['unknown_transforms_by_floor']) == 0 and len(
                self.unknowns['unknown_cards_by_floor']) == 0:
                diff1 = list((Counter(self.current_deck) - Counter(master_deck)).elements())
                diff2 = list((Counter(master_deck) - Counter(self.current_deck)).elements())
                if len(diff1) == len(diff2):
                    upgraded_names_of_unupgraded_cards = [x + "+1" for x in diff1]
                    if upgraded_names_of_unupgraded_cards == diff2:
                        for floor, upgrade_types in self.unknowns['unknown_upgrades_by_floor'].items():
                            if len(diff1) == len(upgrade_types):
                                for unupgraded_card in diff1:
                                    self.run['campfire_choices'].append(
                                        {"data": unupgraded_card, "floor": floor, "key": "SMITH"})
                                return True

        return False, None

    def process_relics(self, floor):
        relics = self.stats_by_floor['relics_by_floor'].get(floor)
        if relics:
            for relic in relics:
                self.obtain_relic(relic, floor)

    def obtain_relic(self, relic, floor):
        if relic == 'Black Blood':
            self.current_relics[0] = 'Black Blood'
            return
        elif relic == 'Ring of the Serpent':
            self.current_relics[0] = 'Ring of the Serpent'
            return
        elif relic == 'FrozenCore':
            self.current_relics[0] = 'FrozenCore'
            return
        elif relic == 'Calling Bell':
            self.current_relics.extend(
                self.end_game_stats['master_relics'][len(self.current_relics) + 1:len(self.current_relics) + 4])
        elif relic == 'Empty Cage':
            self.unknowns['unknown_removes_by_floor'][floor] = 2
        elif relic == 'Whetstone':
            self.unknowns['unknown_upgrades_by_floor'][floor] = [{'type': 'attack'}, {'type': 'attack'}]
        elif relic == 'War Paint':
            self.unknowns['unknown_upgrades_by_floor'][floor] = [{'type': 'skill'}, {'type': 'skill'}]
        self.current_relics.append(relic)
