import click
from pocket.core.create import create as pocket_create
from pocket.core.list import list_ as pocket_list
from pocket.core.rm import rm as pocket_rm, rm_all as pocket_rm_all
from pocket.utils import console


@click.group()
def cli():
    pass


@cli.command(help="create a new pocket")
@click.argument("config")
def create(config):
    pocket_create(config)


@cli.command(help="run a command in a pocket")
@click.argument("pid")
@click.argument("command")
def run():
    pass


@cli.command(help="remove a pocket")
@click.option("-a", "--all", 'all_', is_flag=True)
@click.option("--pid", type=str)
def rm(all_, pid):
    if all_:
        if pid:
            console.error('PID should not be specified with --all parameter')
        else:
            console.ok('%d pockets deleted' % pocket_rm_all())
    else:
        if pid:
            pocket_rm(pid)
        else:
            console.error('Specify a PID or use --all')


@cli.command(help="logs for a pocket")
@click.argument("pid")
def log():
    pass


@cli.command(help="list all pockets")
@click.option("-q", "--quiet", is_flag=True)
def ls(quiet):
    pocket_list(quiet)


if __name__ == '__main__':
    cli()
