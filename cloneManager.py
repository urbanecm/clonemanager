#!/usr/bin/env python
#-*- coding: utf-8 -*-

from git import Repo
import requests
import click
from config import Config
import os
import pwd

__dir__ = os.path.dirname(__file__)
config = Config(defaults={'port': 29418, 'user': pwd.getpwuid(os.getuid()).pw_name})

@click.group()
@click.option('--host')
@click.option('--port')
@click.option('--user')
def cli(host, port, user):
    if host:
        config.override('host', host)
    if port:
        config.override('port', port)
    if user:
        config.override('user', user)

@cli.command()
@click.argument('variable', type=click.Choice(['host', 'port', 'user']))
@click.argument('value')
def set(variable, value):
    config[variable] = value
    config.save()

@cli.command()
def clone():
    assert config.can_gerrit
    click.echo('Getting the list of the projects...')
    projects = config.gerrit.get_projects()
    for project in projects:
        if "/" not in project:
            click.echo('Skipping %s' % project)
            continue
        git_url = "ssh://%s@%s:%s/%s.git" % (config.get('user'), config.get('host'), config.get('port'), project)
        hook_path = os.path.join(__dir__, '..', project, '.git', 'hooks', 'commit-msg')
        if not os.path.isdir(os.path.join(__dir__, '..', project)):
            click.echo("Clonning %s" % project)
            Repo.clone_from(git_url, os.path.join(__dir__, '..', project))
        else:
            click.echo("Skipping %s, it was already clone. If you want to update, use update command" % project)
        if not os.path.isfile(hook_path):
            click.echo('Installing missing hook for %s' % project)
            hook = open(hook_path, 'w')
            hook.write(requests.get(config.gerrit.hook_url).content.decode('utf-8'))
            hook.close()
            os.chmod(hook_path, 755)

@cli.command()
def update():
    print('I do not need gerrit')

if __name__ == "__main__":
    cli()