import argparse
import logging
import multiprocessing as mp

from src.process import Process

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('main')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run-directory', default='2019SpireRuns', help='File path to directory of runs')
    parser.add_argument('--num-processes', default=None,
                        help='Number of processes to spawn, defaults to number of CPU cores')
    args = parser.parse_args()

    # Where Slay the Spire runs are stored, as '.run' files
    run_directory = args.run_directory

    # How many processes to start
    if args.num_processes and int(args.num_processes) <= mp.cpu_count():
        num_processes = int(args.num_processes)
    else:
        num_processes = mp.cpu_count()
    run_processor = Process(run_directory, num_processes)
    run_processor.process_runs()


if __name__ == "__main__":
    main()
