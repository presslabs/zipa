# Welcome to zipa

zipa ("apiz reversed") is a generic REST API client, which allows you to
easily access REST APIs that follow conventions being used around the web.

## The magic behind

```
pip install zipa
python
>>> from zipa import api_github_com as gh
>>> gh.orgs.django.repos()
```

Under the hood `zipa` transforms your imports into clients. It follows a simple
convention: `HOSTNAME__PREFIX`. For the hostname, single underscores are
translated into dots and for the prefix into slashes.

For example: `api_twitter_com__v1` becomes `https://api.twitter.com/v1`. The
prefix part is optional.
