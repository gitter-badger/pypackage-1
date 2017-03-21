"""Commandline interface for installing pypackage dodo script."""
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--author', '-a', type=str)
@click.option('--project', '-p', type=str)
@click.option('--github_repo', '-gh', default='', type=str)
def install():
    pass


if __name__ == '__main__':
    cli()
