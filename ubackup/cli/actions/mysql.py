import click
from ubackup.cli import validators
from ubackup.backup.mysql import MysqlBackup

option = click.option(
    '--databases',
    help='List of MySQL databases you want to backup/restore, "*" for all.',
    callback=validators.mysql_databases)


@click.command()
@click.pass_context
@option
def backup(ctx, databases):
    ctx.obj['manager'].push_backup(MysqlBackup(databases=databases))


@click.command()
@click.pass_context
@option
def restore(ctx, databases):
    ctx.obj['manager'].restore_backup(MysqlBackup(databases=databases))
