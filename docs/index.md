# Welcome to zipa

zipa is apiz reversed.

It a general purpose API client. It enables you to use REST api without
depending on an existing client. Also if you are writing an REST api, you can
quickly test it without the need of implementing your own client.

The client aims to follow convetions about the rest APIs around the web.

## The magic behind

```
pip install zipa
python
>>> from zipa import api_github_com as gh
>>> gh.orgs.django.repos()
```

Under the hood `zipa` transforms your imports into clients. If follows a simple
convetion: `HOSTNAME__PREFIX`. For the hostname, single undersocres are
translated into dots and for prefix into slashes.

For example: `api_twitter_com__v1` becomes `https://api.twitter.com/v1`. The
prefix part is optional.

