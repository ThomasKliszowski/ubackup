import click
from ubackup.cli import validators
from ubackup.backup.path import PathBackup

option = click.option(
    '--path',
    help='Absolute path of the backup you want to create/restore.',
    callback=validators.directory,
    required=True)


@click.command()
@click.pass_context
@option
def backup(ctx, path):
    ctx.obj['manager'].push_backup(PathBackup(path=path))


@click.command()
@click.pass_context
@option
def restore(ctx, path):
    ctx.obj['manager'].restore_backup(PathBackup(path=path))
