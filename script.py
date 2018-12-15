import sys
from os.path import dirname, realpath
from itertools import product

from clusterun import create_jobs_from_parameters, run_cli
from main import run_training


PARAMETERS = list(product(
    ['mozart', 'jazzz', 'mozart_sonatas'],
    ['20', '100'],
))


def create_jobs():
    job_name = 'testing'
    commands = [
        'cd ' + dirname(realpath(__file__)),
        ' '.join([
            '/home/trane/.venv/theano/bin/python3',
            realpath(__file__) + ' "$index"',
        ]),
    ]
    create_jobs_from_parameters(PARAMETERS, job_name, commands)


def do_job(parameters):
    run_training(parameters[0], parameters[1])
    print(parameters)


def run_job(index):
    for params in PARAMETERS:
        do_job(params)


def main():
    if len(sys.argv) == 1:
        create_jobs()
    elif len(sys.argv) == 2:
        run_job(int(sys.argv[1]))
    else:
        print('usage: ' + sys.argv[0] + ' [index]')
        exit(1)


if __name__ == '__main__':
    main()
