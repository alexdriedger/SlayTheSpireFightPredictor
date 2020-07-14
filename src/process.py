import datetime
import json
import logging
import os
import re
import time

from .common import InvalidRunError, StSGlobals
from .run import Run

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('main')


class Process:
    """

    """

    def __init__(self, run_directory, num_processed):
        """
        Go through a directory of runs and process them all in batches
        """
        self.run_directory = run_directory

    def process_runs(self):
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
        for root, dirs, files in os.walk(self.run_directory):
            for fname in files:
                count += 1
                if len(fight_training_examples) > 40000:
                    logger.info('Saving batch')
                    write_file_name = f'data_{round(time.time())}.json'
                    self.write_file(fight_training_examples, os.path.join(tmp_dir, write_file_name))
                    fight_training_examples.clear()
                    logger.info('Wrote batch to file')

                if count % 200 == 0:
                    logger.info(
                        f'\n\n\nFiles not able to open: {file_not_opened} => {((file_not_opened / total_file_count) * 100):.1f} %')
                    logger.info(
                        f'Files filtered with pre-filter: {bad_file_count} => {((bad_file_count / total_file_count) * 100):.1f} %')
                    logger.info(
                        f'Files SUCCESSFULLY processed: {file_processed_count} => {((file_processed_count / total_file_count) * 100):.1f} %')
                    logger.info(
                        f'Files with master deck not matching created deck: {file_master_not_match_count} => {((file_master_not_match_count / total_file_count) * 100):.1f} %')
                    logger.info(
                        f'Files not processed: {file_not_processed_count} => {((file_not_processed_count / total_file_count) * 100):.1f} %')
                    logger.info(f'Total files: {total_file_count}')
                    logger.info(f'Number of Training Examples in batch: {len(fight_training_examples)}')
                run_path = os.path.join(root, fname)
                # if run_path.endswith(".run.json"):
                total_file_count += 1
                run = self.load_run(run_path)
                if self.is_bad_file(run):
                    bad_file_count += 1
                else:
                    processed_run = list()
                    try:
                        processed_run.clear()
                        processed_run.extend(Run(run).process_run())
                        file_processed_count += 1
                        fight_training_examples.extend(processed_run)
                    # Just pass all the exceptions we know about
                    except InvalidRunError:
                        pass
                    except RuntimeError as e:
                        file_master_not_match_count += 1
                        logger.debug(f'{run_path}\n')
                        pass

        logger.info(
            f'\n\n\nFiles not able to open: {file_not_opened} => {((file_not_opened / total_file_count) * 100):.1f} %')
        logger.info(
            f'Files filtered with pre-filter: {bad_file_count} => {((bad_file_count / total_file_count) * 100):.1f} %')
        logger.info(
            f'Files SUCCESSFULLY processed: {file_processed_count} => {((file_processed_count / total_file_count) * 100):.1f} %')
        logger.info(
            f'Files with master deck not matching created deck: {file_master_not_match_count} => {((file_master_not_match_count / total_file_count) * 100):.1f} %')
        logger.info(
            f'Files not processed: {file_not_processed_count} => {((file_not_processed_count / total_file_count) * 100):.1f} %')
        logger.info(f'Total files: {total_file_count}')
        logger.info(f'Number of Training Examples: {len(fight_training_examples)}')
        write_file_name = f'data_{round(time.time())}.json'
        self.write_file(fight_training_examples, os.path.join(tmp_dir, write_file_name))

    def process_single_file(self, run_directory, run_path):
        with open(f"{run_directory}/{run_path}", 'r') as file:
            data = json.load(file)
        result = Run(data).process_run()
        logger.info(f'Result: {result}')

    def write_file(self, data, name):
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def load_run(self, run_path):
        with open(run_path, 'r', encoding='utf8') as file:
            data = json.load(file)
        return data

    def is_bad_file(self, run):
        # Corrupted files
        necessary_fields = {'damage_taken', 'event_choices', 'card_choices', 'relics_obtained', 'campfire_choices',
                            'items_purchased', 'item_purchase_floors', 'items_purged', 'items_purged_floors',
                            'character_chosen', 'boss_relics', 'floor_reached', 'master_deck', 'relics'}
        present_fields = set(run.keys())
        has_necessary_fields = necessary_fields.issubset(present_fields)
        if not has_necessary_fields:
            logger.debug('Does not have necessary fields')
            return True

        # Modded games
        key = 'character_chosen'
        if run.get(key) not in StSGlobals.BASE_GAME_CHARACTERS:
            logger.debug('Does not have base game character')
            return True

        key = 'master_deck'
        if set(run.get(key, {'Empty Set'})).issubset(StSGlobals.BASE_GAME_CARDS_AND_UPGRADES) is False:
            logger.debug('Does not use base game deck')
            return True

        key = 'relics'
        if set(run.get(key, {'Empty Set'})).issubset(StSGlobals.BASE_GAME_RELICS) is False:
            logger.debug('Does not have base game relics')
            return True

        key = 'ReplayTheSpireMod:Calculation Training+1'
        if key in run['master_deck']:
            logger.debug('Uses ReplayTheSpireMod')
            return True

        # Watcher files since full release of watcher (v2.0) and ironclad, silent, defect since v1.0
        key = 'build_version'
        if key not in run or self.valid_build_number(run[key], run['character_chosen']) is False:
            logger.debug('Invalid build number')
            return True

        # Non standard runs
        key = 'is_trial'
        if run.get(key, True):
            logger.debug('Trial run')
            return True

        key = 'is_daily'
        if run.get(key, True):
            logger.debug('Daily run')
            return True

        key = 'daily_mods'
        if key in run:
            logger.debug('Daily run')
            return True

        key = 'chose_seed'
        if run.get(key, True):
            logger.debug('Chose seed')
            return True

        # Endless mode
        key = 'is_endless'
        if run.get(key, True):
            logger.debug('Endless mode')
            return True

        key = 'circlet_count'
        if run.get(key, 1) > 0:
            return True

        key = 'floor_reached'
        if run.get(key, 61) > 60:
            logger.debug('More floors than possible')
            return True

        # Really bad players or give ups
        key = 'floor_reached'
        if run.get(key, 1) < 4:
            logger.debug('Player stinks')
            return True

        key = 'score'
        if run.get(key, 1) < 10:
            logger.debug('Player stinks')
            return True

        key = 'player_experience'
        if run.get(key, 1) < 10:
            logger.debug('Player stinks')
            return True

    def valid_build_number(self, string, character):
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
