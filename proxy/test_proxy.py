import logging
from funcy import log_durations
from proxy import Proxy

logger = logging.getLogger(__name__)

## test 1
@log_durations(logging.info)
def test_property_method_get_random_ua():
    proxy=Proxy()
    print(proxy.user_agent)

## test 2 
@log_durations(logging.info)
def test_class_method_get_random_ua():
    print(Proxy.get_random_user_agent())

## test 3
@log_durations(logging.info)
def test_static_method_get_new_proxy_for_url():
    # # Test urls
    # # "https://www.mcallen.net/departments/bridge/mcallen-hidalgo"
    # # "https://www.mcallen.net/departments/bridge/anzalduas"
    # # "https://www.netrma.org/net-rma-policies/toll-rates/"
    # # "https://www.netrma.org/net-rma-policies/toll-rates/"
    print(Proxy.get_new_proxy_for_url(url="https://www.mcallen.net/departments/bridge/mcallen-hidalgo"))

## test 4
@log_durations(logging.info)
def test_getting_new_working_proxies_and_saving_to_file():
    proxy=Proxy()
    print(proxy.get_working_proxy_for_url(url="https://www.netrma.org/net-rma-policies/toll-rates/"))

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S', level=logging.INFO)

    # test 1
    test_property_method_get_random_ua()

    # test 2
    test_class_method_get_random_ua()

    # test 3
    test_static_method_get_new_proxy_for_url()

    # test 4
    test_getting_new_working_proxies_and_saving_to_file()