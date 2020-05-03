from abc import ABC, abstractmethod
import typing as t

from requests import Session

JSONType = t.Union[str, int, float, bool,
                   None, t.Dict[str, t.Any], t.List[t.Any]]
PARAMSType = t.Dict[str, t.Union[str, int]]


class CollectAPI(ABC):
    """Abstract Collect class that we be inhereted by all endpoints
    """

    def __init__(self, endpoint: str, apikey: str) -> None:
        """At class initiation endpoint and apikey are required

        Arguments:
            endpoint {str} -- endpoint of the service e.g. '/stateUsaPrice'
            apikey {str} -- the apikey code in apikey "apikey [THIS_API_CODE]"
        """

        self.endpoint = endpoint
        self.BASE_URL = 'https://api.collectapi.com'

        headers = {
            'content-type': 'application/json',
            'authorization': f'apikey {apikey}'
        }

        session = Session()
        session.headers.update(headers)
        self.session = session

    def __repr__(self):
        return f'{self.__class__.__name__}(API={repr(self.BASE_URL)})'

    @abstractmethod
    def get(self, *args, **kwargs) -> JSONType:
        pass


class GasPrice(CollectAPI):
    """gasPrice endpoint

    Arguments:
            endpoint {str} -- endpoint of the service e.g. '/stateUsaPrice'
            apikey {str} -- the apikey code in apikey "apikey [THIS_API_CODE]"
    
    Returns:
            self -- a class with base url, session ready for parameters

    Usage:
        ```python
        import os
        from collectapi import GasPrice

        apikey=os.environ['COLLECTAPIKEY']
        gas = GasPrice('/stateUsaPrice', apikey=apikey)
        print(gas.get({'state':'WA'}))
        ``` 
    """

    def get(self, params: PARAMSType = None) -> JSONType:

        """get function that returns a json response

        Arguments:
            params {dict} -- dictonary of parameters e.g. {'district': 'kadikoy', 
                                                            'city': 'istanbul'}
        Returns:
            json -- json response
        """

        middle_endpoint = 'gasPrice'

        # check endpoint data start with /
        if not self.endpoint.startswith('/'):
            self.endpoint = f'/{self.endpoint}'

        self.GAS_BASE_URL = f'{self.BASE_URL}/{middle_endpoint}{self.endpoint}'
        req = self.session.get(url=self.GAS_BASE_URL, params=params)

        assert req.status_code == 200, 'Connection Issue'
        return req.json()
