zipa [![Build Status](https://api.travis-ci.org/PressLabs/zipa.svg)](https://travis-ci.org/PressLabs/zipa)
====

# Welcome to zipa

zipa is a magic pythonic REST client. For more information read the [docs](http://zipa.readthedocs.org/).

zipa was developed by the awesome engineering team at [Presslabs](https://www.presslabs.com/), 
a Managed WordPress Hosting provider.

For more open-source projects, check [Presslabs Code](https://www.presslabs.org/). 

### Instalation
``` pip install zipa ```

### Examples

```
>>> from zipa import api_github_com as gh
>>> for repo in gh.users['tpope'].repos:
...     print(repo.name)

```

Under the hood `zipa` transforms your imports into clients. It follows a simple
convention: `HOSTNAME__PREFIX`. For the hostname, single underscores are
translated into dots and for the prefix into slashes.

For example: `api_twitter_com__v1` becomes `https://api.twitter.com/v1`. The
prefix part is optional.
