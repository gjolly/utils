#!/usr/bin/env python3
import os
import click
from datetime import datetime
from github import Github


@click.command(help='Close all the PRs against a github repository that were not \
updated after the given date. REPO_NAME should be formated like `org/repo`, \
date should be %Y%m%d')
@click.argument('repo_name')
@click.argument('date')
def main(repo_name: str, date: str) -> None:
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        raise ValueError('GITHUB_TOKEN env var should be set')

    org_id, repo_id = repo_name.split('/')
    end_date = datetime.strptime(date, '%Y%m%d')

    g = Github(github_token)
    pr_to_close = list()
    repo = g.get_organization(org_id).get_repo(repo_id)

    click.echo('Will close the following PRs:')
    # Then play with your Github objects:
    for pr in repo.get_pulls():
        if pr.updated_at < end_date:
            pr_to_close.append(pr)
            click.echo(f'{pr.updated_at} - {pr.title} - {pr.state}')

    r = click.prompt('Apply[Y/n]')

    if r != 'Y':
        click.echo('User abort')
        return

    for pr in pr_to_close:
        pr.edit(status='closed')


if __name__ == '__main__':
    main()
