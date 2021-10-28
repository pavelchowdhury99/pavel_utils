import logging
import random
import time

import requests

import pytest
from funcy import log_durations
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
        assert new_proxy.get("https") is not None
        assert new_proxy.get("http") is not None

    def test_get_working_proxy_for_url(self, proxy_obj, url_to_test):
        """test to check test_get_working_proxy_for_url"""
        new_proxy = proxy_obj.get_new_proxy_for_url(url_to_test,
                                                    verify=False)
        time.sleep(2)
        assert requests.get(url_to_test,
                            proxies=new_proxy,
                            verify=False).ok

        assert isinstance(new_proxy, dict)
        assert new_proxy.get("https") is not None
        assert new_proxy.get("http") is not None

    def test_get_proxy_rotator(self, proxy_rotator):
        """test to check get_proxy_rotator"""
        for idx,new_proxy in enumerate(proxy_rotator):
            if idx==4:
                break
            assert isinstance(new_proxy, dict)
            assert new_proxy.get("https") is not None
            assert new_proxy.get("http") is not None

# test 1
# test loading class attribute __user_agent
# ,__init__ and loading from proxy.json
@log_durations(logging.info)
def test_property_method_get_random_ua():
    proxy = Proxy()
    print(proxy.user_agent)


# test 2
# test get_random_user_agent class method
# prints a dict
@log_durations(logging.info)
def test_class_method_get_random_ua():
    print(Proxy.get_random_user_agent())


# test 3
# test static get_new_proxy_for_url
# and prints a dict
@log_durations(logging.info)
def test_static_method_get_new_proxy_for_url():
    # # Test urls
    # # "https://www.mcallen.net/departments/bridge/mcallen-hidalgo"
    # # "https://www.mcallen.net/departments/bridge/anzalduas"
    # # "https://www.netrma.org/net-rma-policies/toll-rates/"
    # # "https://www.netrma.org/net-rma-policies/toll-rates/"
    print(Proxy.get_new_proxy_for_url(url="https://www.mcallen.net/departments/bridge/mcallen-hidalgo"))


# test 4
# test method get_working_proxy_for_url
# and prints a dict and updates the proxy.json
@log_durations(logging.info)
def test_getting_new_working_proxies_and_saving_to_file():
    proxy = Proxy()
    print(proxy.get_working_proxy_for_url(url="https://www.netrma.org/net-rma-policies/toll-rates/"))


# test 5
# check get_proxy_rotator static method
def test_check_get_proxy_rotator():
    for idx, proxy in enumerate(Proxy.get_proxy_rotator()):
        if idx == 4:
            break
        assert type(proxy) == dict
        assert proxy.get('https') is not None
    logger.debug("Done checking get_proxy_rotator")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)

    # test 1
    test_property_method_get_random_ua()

    # test 2
    test_class_method_get_random_ua()

    # test 3
    test_static_method_get_new_proxy_for_url()

    # test 4
    test_getting_new_working_proxies_and_saving_to_file()

    # test 5
    test_check_get_proxy_rotator()
