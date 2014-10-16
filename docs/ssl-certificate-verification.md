# SSL Certificate Verification

Enable verification (default)
```
from zipa import api_github_com as gh
gh.config.verify = True
```

Disable verification (bad idea)
```
from zipa import api_github_com as gh
gh.config.verify = False
```

Provide server certificate (ie. with self-signed certs or custom CA setups)
```
from zipa import api_github_com as gh
gh.config.verify = '/path/to/your/servercert.pem'
```
