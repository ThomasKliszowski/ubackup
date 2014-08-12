from ubackup import settings, utils, log
from ubackup.remote import REMOTES
from ubackup.manager import Manager
import click

import logging
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(settings.VERSION)
@click.pass_context
@click.option(
    '--settings-path',
    help='Path to your settings which will be merged with the app settings.')
@click.option(
    '--remote',
    help='The remote you want to use.',
    type=click.Choice(REMOTES.keys()),
    required=True)
@click.option(
    '--log-level',
    help='The log level you want to capture.',
    type=click.Choice(log.level_names()),
    default='INFO')
def cli(ctx, settings_path, remote, log_level):
    # Merge settings and init logging
    utils.merge_settings(settings_path)
    log.set_config(settings.LOGGING)
    log.set_level(log_level)

    ctx.obj['manager'] = Manager(
        REMOTES[remote](token=settings.DROPBOX_TOKEN))


# -----

# Import all sub commands
from ubackup.cli.backup import *

# -----


def main():
    try:
        cli(obj={})
    except Exception as e:
        logger.error(e, exc_info=True)
