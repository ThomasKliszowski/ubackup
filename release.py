#!/usr/bin/env python
import click
import os
import re
from subprocess import Popen, PIPE, CalledProcessError

CURRENT_DIR = os.path.dirname(__file__)
VERSION_PATH = os.path.join(CURRENT_DIR, 'ubackup', 'VERSION.txt')


def c(cmd):
    p = Popen(cmd, stdout=PIPE, shell=True)
    p.wait()
    if p.returncode:
        raise CalledProcessError(p.returncode, cmd)
    return p.stdout.read()


@click.command(help='Auto release tool using Git & Pypi upload.')
def cli():
    with open(VERSION_PATH, 'r') as fp:
        version = fp.read().strip()

    click.echo('Current release: %s' % click.style(version))

    new_version = click.prompt('Enter your new release')
    release_message = click.prompt('Enter your release message')

    current_branch = c('git rev-parse --abbrev-ref HEAD').strip()
    c('git checkout develop')
    with open(VERSION_PATH, 'w') as fp:
        fp.write(new_version)
    c('git add %s' % VERSION_PATH)
    c('git commit -m "update VERSION from %s to %s"' % (version, new_version))
    c('git push')

    c('git checkout master')
    c('git merge develop --commit')
    c('git tag %s -m "%s"' % (new_version, re.sub(r'[\"]', '\\\"', release_message)))
    c('git push')
    c('git push --tags')
    c('python setup.py sdist register upload')

    c('git checkout %s' % current_branch)


if __name__ == "__main__":
    cli()
