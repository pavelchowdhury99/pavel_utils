import json
import os
import logging
import random
import functools
import time
from collections import defaultdict
import pandas as pd
import requests
from itertools import cycle
from funcy import log_durations
from pathlib import Path

logger = logging.getLogger(__name__)


class Proxy:
    ''' Class to store data related to proxies'''

    # Class variable defined here
    with open(Path(os.path.join(os.path.dirname(__file__), 'user_agents.json')), 'r') as f:
        __user_agent_list = json.load(f).get("user_agents")
        logger.debug(f"Loaded list of user agents from json file")
        logger.debug(f"First and last are - {__user_agent_list[0]} and {__user_agent_list[-1]}")

    @functools.lru_cache
    def __init__(self):
        with open(Path(os.path.join(os.path.dirname(__file__), 'proxy.json')), 'r') as f:
            self.__proxy = json.load(f)
            logger.debug(f"Loaded proxy {self.__proxy} from json file")

    @property
    def user_agent(self) -> dict:
        """Provides a random user agent from list of user agents"""
        logger.debug("Fetching a random user agent...")
        return {"User-Agent": random.choice(self.__user_agent_list)}

    @classmethod
    def get_random_user_agent(cls):
        """Provides a random user agent from list of user agents"""
        logger.debug("Fetching a random user agent...")
        return {"User-Agent": random.choice(cls.__user_agent_list)}

    @staticmethod
    def get_new_proxy_for_url(url: str, verify: bool = True, timeout: int = 200) -> dict:
        """Getting new proxy for the given url"""

        proxy_website_url = 'https://www.us-proxy.org/'

        # getting page content of the proxy list page
        proxy_df = pd.read_html(requests.get(
            proxy_website_url, timeout=200).text)

        # checking if the url which needs proxy is secured or not
        # and filtering the proxy list based on that
        if "https" in url:
            logger.debug("Fetching new proxy for https type url..")
            proxy_df = proxy_df[0][proxy_df[0]['Https'] == 'yes']
            key = "https"
        else:
            logger.debug("Fetching new proxy for http type url..")
            proxy_df = proxy_df[0][proxy_df[0]['Https'] == 'no']
            key = "https"

        # trying each proxy from the proxy list
        proxy_dict = dict()
        for count, proxy in enumerate(proxy_df.iterrows()):
            # proxy_dict[key] = f"{key}://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
            proxy_dict[key] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
            try:
                if requests.get(url, proxies=proxy_dict, verify=verify, timeout=timeout).ok:
                    logging.info(f"Using proxy {proxy_dict}")
                    return proxy_dict
            except Exception as e:
                logging.debug(
                    f"Proxy {proxy_dict} {count} failed because of {e}")
                continue
        raise Exception("No Proxy Found!")

    def get_working_proxy_for_url(self, url: str, verify: bool = True, timeout: int = 200,
                                  proxy_json_path: str = os.path.join(os.path.dirname(__file__),
                                                                      'proxy.json')) -> dict:
        try:
            if requests.get(url, proxies=self.__proxy).ok:
                logger.info(f"Using existing proxies {self.__proxy}")
                return self.__proxy
            else:
                new_proxy_dict = Proxy.get_new_proxy_for_url(url=url,
                                                             verify=verify,
                                                             timeout=timeout)
                self.__proxy.update(new_proxy_dict)
                return self.__proxy
        except requests.exceptions.ProxyError:
            new_proxy_dict = Proxy.get_new_proxy_for_url(url=url,
                                                         verify=True)
            self.__proxy.update(new_proxy_dict)
            return self.__proxy
        except Exception as e:
            logger.error(f"Could not find proxy due to {e}")
        finally:
            with open(proxy_json_path, 'w') as f:
                json.dump(self.__proxy, f)
                logger.info(f"Wrote new proxy {self.__proxy} to {proxy_json_path}")

    # @staticmethod
    # def get_proxy_by_location(location: str) -> dict:
    #     # using default dict so that if someone passes wrong country code it will not through KeyError
    #     dict_of_proxies_by_location = defaultdict(lambda x: None)
    #     # use the following site for proxies
    #     # http://free-proxy.cz/en/proxylist/country/US/https/ping/all
    #     dict_of_proxies_by_location.update(dict(us={
    #         "http": "http://132.226.36.165:3128",
    #         "https": "https://104.129.196.54:8800",
    #         "ftp": "ftp://10.10.1.10:3128"
    #     }))
    #     # if correct, provides location proxy dict else None
    #     if location:
    #         return dict_of_proxies_by_location[location]
    #     # if location is None returns None
    #     return dict()

    @staticmethod
    def get_proxy_rotator() -> cycle:
        proxy_url = 'https://free-proxy-list.net/'
        df = pd.read_html(requests.get(proxy_url,
                                       headers=Proxy.get_random_user_agent()).text)[0]
        df = df[df['Https'] == 'yes']
        df['http'] = df[['IP Address', 'Port']].apply(
            lambda x: f'http://{x[0]}:{x[1]}', axis=1)
        df['https'] = df[['IP Address', 'Port']].apply(
            lambda x: f'https://{x[0]}:{x[1]}', axis=1)
        proxy_rotator = cycle(df[['http', 'https']].to_dict('records'))
        return proxy_rotator


@log_durations(logging.info)
def main():
    proxy = Proxy()
    logger.info(proxy.user_agent)
    x = proxy.get_working_proxy_for_url(url="https://www.netrma.org/net-rma-policies/toll-rates/", verify=False)
    logger.info("sleeping for 2 secs...")
    time.sleep(2)
    logger.info("Just woke up!")
    requests.get("https://www.netrma.org/net-rma-policies/toll-rates/", proxies=x, verify=False)
    logger.info("Done!!!!")

# Test urls
# "https://www.mcallen.net/departments/bridge/mcallen-hidalgo"
# "https://www.mcallen.net/departments/bridge/anzalduas"
# "https://www.netrma.org/net-rma-policies/toll-rates/"

# References
# https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    main()
