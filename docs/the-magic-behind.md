# The magic behind

Here are the rules zipa is following when doing its magic:

#### If you access a resource by object noation `.name` or dict notation `[name]` it makes no difference.
```
gh.users                            # /users
gh.orgs.django                      # /orgs/django
gh.orgs['django']                   # /orgs/django
gh.orgs['django'].repos['django']   # /orgs/django/repos/django
```

#### Calls to the remote are only made when you actually make a call from python

The following statements do not make a remote call
```
repos = gh.orgs['django'].repos
print(gh.orgs.django)
```
While these ones do:
```
repos = gh.orgs['django'].repos
# this calls GET /orgs/django/repos
repos()

# This calls GET /orgs/django
print(gh.orgs.django())

# This one calls GET /orgs/django/repos and subsequently calls the next url
# from the Link header
for repo in gh.orgs.django.repos:
    print(repo.name)
```

#### Filtering

You can add filters to iterators by using the slice notation like this:
```
# This one calls GET /orgs/django/repos?sort=created&direction=desc
for repo in gh.orgs.django.repos[{'sort': 'created', 'direction': 'desc'}]:
    print(repo.name)
```
