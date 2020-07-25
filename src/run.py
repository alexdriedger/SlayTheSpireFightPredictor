import logging
from collections import Counter

from .common import InvalidRunError, StSGlobals

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('run')


class Run:
    """
    Processes a single run.
    WIP. Currently reimplements all the methods that were used in main.py
    """

    def __init__(self, run):
        """

        :param run_path:
        """
        self.run = run
        self.end_game_stats = self.get_end_game_stats()
        self.stats_by_floor = self.get_by_floor()
        self.current_deck = self.get_starting_deck()
        self.current_relics = self.get_starting_relics()
        self.processed_fights = []
        self.unknowns = {'unknown_removes_by_floor': {}, 'unknown_upgrades_by_floor': {},
                         'unknown_transforms_by_floor': {}, 'unknown_cards_by_floor': {}, }

    def get_starting_relics(self):
        character = self.run.get('character_chosen')
        character_relics = {'IRONCLAD': ['Burning Blood'], 'THE_SILENT': ['Ring of the Snake'],
                            'DEFECT': ['Cracked Core'], 'WATCHER': ['PureWater'], }

        return character_relics.get(character)

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
        end_game_stats = {'score': self.run.get('score', 0), 'master_deck': self.run.get('master_deck'),
                          'master_relics': self.run.get('relics'), 'path_taken': self.run.get('path_taken'),
                          'damage_taken': self.run.get('damage_taken'), 'act_bosses': self.get_act_bosses(), }
        return end_game_stats

    def get_act_bosses(self):
        self.run.get('path_per_floor')
        boss_floors = set([floor + 1 for floor, event in enumerate(self.run.get('path_per_floor', [])) if event == 'B'])
        act_bosses = {}
        for encounter in self.run.get('damage_taken', []):
            if encounter['floor'] in boss_floors:
                act_bosses[int(encounter['floor'])] = encounter['enemies']
        return act_bosses

    def get_by_floor(self):
        stats_by_floor = {
            'battle_stats_by_floor': {battle_stat['floor']: battle_stat for battle_stat in self.run['damage_taken']},
            'events_by_floor': {event_stat['floor']: event_stat for event_stat in self.run['event_choices']},
            'card_choices_by_floor': {card_choice['floor']: card_choice for card_choice in self.run['card_choices']},
            'relics_by_floor': self.get_relics_by_floor(),
            'campfire_choices_by_floor': {campfire_choice['floor']: campfire_choice for campfire_choice in
                                          self.run['campfire_choices']},
            # TODO: I don't think that the items purchased are in an ordered list! (See
            #  Feel No Pain upgrade in '2019SpireRuns/1555291174.run')
            'purchases_by_floor': self.get_stat_with_separate_floor_list('items_purchased', 'item_purchase_floors'),
            'purges_by_floor': self.get_stat_with_separate_floor_list('items_purged', 'items_purged_floors'),
            'potion_use_by_floor': list(set(self.run['potions_floor_usage'])),
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
        logger.debug(f'Deck at floor 0: {self.current_deck}')
        self.process_neow()
        for floor in range(1, self.run['floor_reached']):
            logger.debug(f'Deck at floor {floor}: {self.current_deck}')
            # TODO: Use the relics and cards on floor 1 to determine Neow's blessing
            self.process_battle(floor)
            self.process_relics(floor)
            self.process_card_choice(floor)
            self.process_campfire_choice(floor)
            self.process_purchases(floor)
            self.process_purges(floor)
            self.process_events(floor)

        master_deck = self.end_game_stats['master_deck']
        master_relics = self.end_game_stats['master_relics']
        if set(self.current_deck) != set(master_deck) or set(self.current_relics) != set(master_relics):
            success = self.resolve_missing_data()
            if success:
                return Run(self.run).process_run()
            raise RuntimeError('Final decks or relics did not match')
        else:
            return self.processed_fights

    def process_battle(self, floor):
        battle_stat = self.stats_by_floor['battle_stats_by_floor'].get(floor)
        if battle_stat:
            fight_data = dict()
            fight_data['cards'] = list(self.current_deck)
            fight_data['relics'] = list(self.current_relics)
            fight_data['max_hp'] = self.run['max_hp_per_floor'][floor - 2]
            fight_data['entering_hp'] = self.run['current_hp_per_floor'][floor - 2]
            fight_data['character'] = self.run['character_chosen']
            fight_data['ascension'] = self.run['ascension_level']
            fight_data['enemies'] = battle_stat['enemies']
            fight_data['potion_used'] = floor in self.stats_by_floor['potion_use_by_floor']
            fight_data['floor'] = floor
            fight_data['damage_taken'] = self.get_hp_change(battle_stat, floor)
            next_boss_floor, fight_data['next_boss'] = self.get_next_boss(floor)
            fight_data['score'] = self.end_game_stats['score']
            fight_data['remaining_encounters'] = self.get_remaining_encounters(floor, next_boss_floor)
            self.processed_fights.append(fight_data)

    def get_hp_change(self, battle_stat, floor):
        if self.run['current_hp_per_floor'] == 0:
            hp_change = battle_stat['damage']
        else:
            hp_change = self.run['current_hp_per_floor'][floor - 2] - self.run['current_hp_per_floor'][floor - 1]
        return hp_change

    def get_remaining_encounters(self, floor, next_boss_floor):
        """
        Used to get the remaining floors of certain encounter types before the Act Boss.
        encounter types are defined as follows: can be within the following:
            'M' - monster
            '$' - shop
            'E' - elite
            'R' - rest (AKA campfire)
            'BOSS' - act boss
            'T' - treasure
            '?' - event
        """
        encounter_types = ['M', '$', 'E', 'R', 'T', '?']
        remaining_path = self.end_game_stats['path_taken'][floor - 1: next_boss_floor]

        # Get encounter indices
        remaining_encounters = {
            encounter_type: len([i for i in remaining_path if i == encounter_type])
            for encounter_type in encounter_types
        }

        return remaining_encounters

    def get_next_boss(self, floor):
        next_boss_floor = 999
        next_boss = None
        for boss_floor, boss in self.end_game_stats['act_bosses'].items():
            if floor < boss_floor < next_boss_floor:
                next_boss_floor = boss_floor
                next_boss = boss
        return int(next_boss_floor), next_boss

    def process_card_choice(self, floor):
        card_choice_data = self.stats_by_floor['card_choices_by_floor'].get(floor)
        if card_choice_data:
            picked_card = card_choice_data['picked']
            if picked_card != 'SKIP' and picked_card != 'Singing Bowl':
                if 'Molten Egg 2' in self.current_relics and picked_card in StSGlobals.BASE_GAME_ATTACKS and \
                        picked_card[-2] != '+1':
                    picked_card += '+1'
                if 'Toxic Egg 2' in self.current_relics and picked_card in StSGlobals.BASE_GAME_SKILLS and picked_card[
                    -2] != '+1':
                    picked_card += '+1'
                if 'Frozen Egg 2' in self.current_relics and picked_card in StSGlobals.BASE_GAME_POWERS and picked_card[
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
        # TODO: Handle cards that were obtained via alternative methods
        if card_to_upgrade not in self.current_deck:
            logger.debug(f'{card_to_upgrade} not in current deck, did not get as battle card reward')
            raise InvalidRunError(f'{card_to_upgrade} not in current deck, did not get as battle card reward')
        card_to_upgrade_index = self.current_deck.index(card_to_upgrade)

        has_multiple_upgrades = len(self.current_deck[card_to_upgrade_index].split('+')) == 2
        if has_multiple_upgrades:
            logger.debug('Searing blow upgraded past +1')
            card_name, upgrades = self.current_deck[card_to_upgrade_index].split('+')
            self.current_deck[card_to_upgrade_index] = f'{card_name}+{str(int(upgrades[1:]) + 1)}'
            str(int(upgrades[1:]) + 1)
        self.current_deck[card_to_upgrade_index] += '+1'

    def process_purchases(self, floor):
        purchase_data = self.stats_by_floor['purchases_by_floor'].get(floor)
        if purchase_data:
            purchased_cards = [x for x in purchase_data if
                               x not in StSGlobals.BASE_GAME_RELICS and x not in StSGlobals.BASE_GAME_POTIONS]
            purchased_relics = [x for x in purchase_data if
                                x not in purchased_cards and x not in StSGlobals.BASE_GAME_POTIONS]
            self.current_deck.extend(purchased_cards)
            for r in purchased_relics:
                self.obtain_relic(r, floor)

    def process_purges(self, floor):
        purge_data = self.stats_by_floor['purges_by_floor'].get(floor)
        if purge_data:
            for card in purge_data:
                try:
                    self.current_deck.remove(card)
                except ValueError:
                    logger.debug(f'{card} not present in deck')
                    raise InvalidRunError(f'{card} not present in deck')

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
                    self.remove_card(card)
            if 'cards_upgraded' in event_data:
                for card in event_data['cards_upgraded']:
                    self.upgrade_card(card)
            if 'event_name' in event_data and event_data['event_name'] == 'Vampires':
                self.current_deck[:] = [x for x in self.current_deck if not x.startswith('Strike')]

    def remove_card(self, cards_to_remove):
        current_deck = set(self.current_deck)
        for card in cards_to_remove:
            if card in current_deck:
                self.current_deck.remove(card)
            elif f'{card}+1' in current_deck:
                self.current_deck.remove(f'{card}+1')
            else:
                # I assume no one will throw away their Searing Blow +n
                raise InvalidRunError(f'Trying to remove {card} in event where it does not exist')

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
        if relic in StSGlobals.BASE_GAME_STARTING_RELICS:
            self.current_relics[0] = relic
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
