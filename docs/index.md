# Welcome to zipa

zipa is apiz reversed.

It is a general purpose API client. It enables you to use REST APIs without
depending on an existing client. Also if you are writing an REST API, you can
quickly test it without the need of implementing your own client.

The client aims to follow conventions about the rest APIs around the web.

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
