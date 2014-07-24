zipa
====
General purpose REST API client


```
>>> from zipa import api_github_com as gh
>>> for repo in gh.users['tpope'].repos:
...     print("{}: {}".format(repo.name, repo.url))

```
