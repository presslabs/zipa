zipa [![Build Status](https://travis-ci.org/vtemian/zipa.svg?branch=master)](https://travis-ci.org/vtemian/zipa)
====
General purpose REST API client ([docs](http://vtemian.github.io/zipa/)).


```
>>> from zipa import api_github_com as gh
>>> for repo in gh.users['tpope'].repos:
...     print repo.name

```

Under the hood `zipa` transforms your imports into clients. It follows a simple
convention: `HOSTNAME__PREFIX`. For the hostname, single underscores are
translated into dots and for the prefix into slashes.

For example: `api_twitter_com__v1` becomes `https://api.twitter.com/v1`. The
prefix part is optional.
