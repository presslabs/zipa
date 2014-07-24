# -*- coding: utf-8 -*-
# vim: ft=python:sw=4:ts=4:sts=4:et:
from zipa import api_github_com as github

repos = github.orgs.django.repos

for repo in repos[{'sort': 'created', 'direction': 'desc'}]:
    print repo.name
