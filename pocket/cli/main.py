import click


@click.group()
def cli():
    pass


@cli.command(help="create a new pocket")
@click.argument("config")
def create():
    pass


@cli.command(help="run a command in a pocket")
@click.argument("pid")
@click.argument("command")
def run():
    pass


@cli.command(help="remove a pocket")
@click.argument("pid")
def rm():
    pass


@cli.command(help="logs for a pocket")
@click.argument("pid")
def log():
    pass


@cli.command(help="list all pockets")
def ls():
    pass


if __name__ == '__main__':
    cli()
