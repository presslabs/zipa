# Getting and manipulating data

__Getting data is as simple as calling a function.__

## Simple GET

For well written APIs the calls will have much sense. For example, for getting
all repos from `django` GitHub organization you just call:

```
from zipa import api_github_com as gh
gh.orgs.django.repos()
```

## Passing arguments

Function arguments are passed to the request.

```
gh.orgs.django.repos(page=2)
```

This would do a `GET /orgs/django/repos?page=2`

## Creating an object

Creating an object is as simple as calling a [magic function](/magic/#functions).

```
gist = gh.gists.create(description='Test gist', files={'empty.txt': {'content': 'a'}})
```

## Deleting an object
```
gh.gists[gist.id].delete()
```


