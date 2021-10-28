import logging
from funcy import log_durations
from proxy import Proxy

logger = logging.getLogger(__name__)


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
