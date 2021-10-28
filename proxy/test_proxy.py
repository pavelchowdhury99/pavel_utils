import logging
import random
import time
import os
import requests
import pytest

from .proxy import Proxy

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def proxy_obj() -> Proxy:
    """Returns a proxy object"""
    return Proxy()


@pytest.fixture(scope="class")
def url_to_test() -> str:
    """Returns a url string"""
    url_list = [
        "https://www.mcallen.net/departments/bridge/mcallen-hidalgo",
        "https://www.mcallen.net/departments/bridge/anzalduas",
        "https://www.netrma.org/net-rma-policies/toll-rates/",
    ]
    random_url = random.choice(url_list)
    logger.debug(f"Using {random_url} as test url")
    return random_url


@pytest.fixture(scope="class")
def proxy_rotator():
    """Return a cycle object of proxy dict"""
    return Proxy.get_proxy_rotator()


@pytest.mark.usefixtures("proxy_obj", "url_to_test", "proxy_rotator")
class TestProxy:
    """Tests Class to test Proxy class from proxy.py"""

    def test_init(self, proxy_obj):
        """test to check object creation"""
        assert isinstance(proxy_obj, Proxy)

    def test_user_agent_property(self, proxy_obj):
        """test to check user_agent property method"""
        assert isinstance(proxy_obj.user_agent, dict)

    def test_get_random_user_agent(self):
        """test the class method to get random user agent"""
        assert isinstance(Proxy.get_random_user_agent(), dict)

    def test_get_new_proxy_for_url(self, url_to_test):
        """test to check get_new_proxy_for_url static method"""
        new_proxy = Proxy.get_new_proxy_for_url(url_to_test, verify=False)
        assert isinstance(new_proxy, dict)
        assert any([new_proxy.get("https") is not None,
                    new_proxy.get("http") is not None]) == True

    def test_get_working_proxy_for_url(self, proxy_obj, url_to_test):
        """test to check test_get_working_proxy_for_url"""
        new_proxy = proxy_obj.get_new_proxy_for_url(url_to_test,
                                                    verify=False)
        time.sleep(2)
        assert requests.get(url_to_test,
                            proxies=new_proxy,
                            verify=False).ok

        assert isinstance(new_proxy, dict)
        assert any([new_proxy.get("https") is not None,
                    new_proxy.get("http") is not None]) == True

    def test_get_proxy_rotator(self, proxy_rotator):
        """test to check get_proxy_rotator"""
        for idx, new_proxy in enumerate(proxy_rotator):
            if idx == 4:
                break
            assert isinstance(new_proxy, dict)
            assert new_proxy.get("https") is not None
            assert new_proxy.get("http") is not None


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    pytest.main(["-v", f'{os.path.realpath(__file__)}:test_get_proxy_rotator'])
