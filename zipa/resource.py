import json
import requests

from requests.exceptions import HTTPError

from .entity import Entity
from .utils import dict_merge


class Resource(dict):
    def __resource(self, url):
        if url == self._get_url():
            raise RuntimeError('Cannot call directly on root')

        base_url = self._get_url()
        if not url.startswith(base_url):
            raise RuntimeError("You can't change the base url. The new "
                               "resource needs to have the host %s" % base_url)

        return Resource(url[len(base_url):], url.split("/")[-1],
                        config=self.config)

    def __init__(self, url=None, name=None, params=None, config=None):
        self._url = url or ''
        self.name = name
        self.params = params or {}

        _config = config or {}
        _config_defaults = {
            'auth': None,
            'use_extensions': False,
            'secure': True,
            'prefix': '/',
            'serializer': 'json',
            'verify': True,
            'append_slash': False,
            'headers': {},
            'response_handler': self.default_response_handler
        }

        config = dict_merge(_config_defaults, _config)
        self.config = Entity(config)

        if name is None:
            self.resource = self.__resource

    def _get_url(self):
        scheme = 'https://' if self.config.secure else 'http://'

        url = scheme + self.config.host + self.config.prefix
        if not url.endswith('/'):
            url += '/'
        resource_url = self._url.replace('_/', '/').rstrip('/')
        if resource_url.startswith('/'):
            resource_url = resource_url[1:]
        url += resource_url

        if self.config.use_extensions:
            url += '.json'

        if self.config.append_slash and not url.endswith('/'):
            url += '/'

        return url

    def _expand_url(self, part):
        prefix = self._url
        if not self._url.endswith('/'):
            prefix += '/'
        return '%s%s' % (prefix, part)

    def _prepare_data(self, **kwargs):
        if self.config.serializer == 'json':
            return json.dumps(kwargs)
        else:
            return kwargs

    @staticmethod
    def default_response_handler(response):
        try:
            parsed_response = response.json()
        except ValueError:
            parsed_response = {}

        if 400 <= response.status_code < 500:
            http_error_msg = '%s Client Error: %s' % (response.status_code,
                                                      response.reason)
        elif 500 <= response.status_code < 600:
            http_error_msg = '%s Server Error: %s' % (response.status_code,
                                                      response.reason)
        else:
            http_error_msg = None

        if http_error_msg:
            raise HTTPError(http_error_msg, parsed_response, response=response)

        return parsed_response

    def _prepare_entity(self, response):
        response_handler = self.config.response_handler or (lambda r: r)

        parsed_response = response_handler(response) or {}

        if isinstance(parsed_response, list):
            return [Entity(entity) for entity in parsed_response]

        return Entity(parsed_response)

    def post(self, **kwargs):
        data = self._prepare_data(**kwargs)
        headers = dict_merge({'content-type': 'application/json'},
                             self.config['headers'])
        response = requests.post(self.url, data=data,
                                 auth=self.config['auth'],
                                 verify=self.config['verify'],
                                 headers=headers)

        entity = self._prepare_entity(response)
        return entity

    def put(self, **kwargs):
        data = self._prepare_data(**kwargs)
        headers = dict_merge({'content-type': 'application/json'},
                             self.config['headers'])
        response = requests.put(self.url, data=data,
                                auth=self.config['auth'],
                                verify=self.config['verify'],
                                headers=headers)

        entity = self._prepare_entity(response)
        return entity

    def delete(self, **kwargs):
        response = requests.delete(self.url, params=kwargs,
                                   auth=self.config['auth'],
                                   verify=self.config['verify'])
        entity = self._prepare_entity(response)
        return entity

    def patch(self, **kwargs):
        data = self._prepare_data(**kwargs)
        headers = dict_merge({'content-type': 'application/json'},
                             self.config['headers'])
        response = requests.patch(self.url, data=data,
                                  auth=self.config['auth'],
                                  verify=self.config['verify'],
                                  headers=headers)

        entity = self._prepare_entity(response)
        return entity

    def __getattr__(self, name):
        if name == 'url':
            return self._get_url()
        elif name in self.__dict__:
            return self.__dict__[name]

        # Handle special attributes used with ipdb/ipython tab completion.
        elif name in ['_getAttributeNames', 'trait_names']:
            return super(Resource, self).__getattribute__(name)

        return Resource(self._expand_url(name), name, config=self.config)

    def __getitem__(self, name):
        if isinstance(name, dict):
            params = name
            filtered = Resource(self._url, self.name, params, self.config)
            return filtered
        elif isinstance(name, slice):
            params = name.start or {}
            if name.stop:
                params['page'] = name.stop
            if slice.step:
                params['per_page'] = name.step

            filtered = Resource(self._url, self.name, params, self.config)
            return filtered
        else:
            return self.__getattr__(name)

    def __call__(self, **kwargs):
        if self.name is None:
            raise RuntimeError('Cannot call directly on root')

        response = requests.get(self.url, params=kwargs,
                                auth=self.config['auth'],
                                headers=self.config['headers'],
                                verify=self.config['verify'])
        entity = self._prepare_entity(response)
        return entity

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<Resource: %s>' % self.url

    def __iter__(self):
        r = requests.get(self.url, params=self.params,
                         auth=self.config['auth'],
                         verify=self.config['verify'])
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict):
            yield Entity(data)
        else:
            for x in data:
                yield Entity(x)
        while 'next' in r.links and r.links['next']['url']:
            r = requests.get(r.links['next']['url'],
                             auth=self.config['auth'],
                             verify=self.config['verify'])
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict):
                yield Entity(data)
            else:
                for x in data:
                    yield Entity(x)
