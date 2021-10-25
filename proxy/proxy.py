import json
import logging
import random
import time
from collections import defaultdict
from pathlib import Path
import pandas as pd
import requests
from itertools import cycle
import functools
from funcy import log_durations
from pathlib import Path


class Proxy:
    ''' Class to store data related to proxies'''

    @functools.lru_cache
    def __init__(self):
        with open(Path(r"proxy\proxy.json"), 'r') as f:
            self.__proxy = json.load(f)
            logging.info(f"Loaded proxy {self.__proxy} from json file")
        with open(Path(r'proxy\user_agents.json'), 'r') as f:
            self.__user_agent_list = json.load(f).get("user_agents")
            logging.info(f"Loaded list of user agents from json file")
            logging.info(
                f"First and last are - {self.__user_agent_list[0]} and {self.__user_agent_list[-1]}")

    @property
    def user_agent(self) -> dict:
        """Provides a random user agent from list of user agents"""
        return {"User-Agent": random.choice(self.__user_agent_list)}

    @staticmethod
    def get_new_proxy_for_url(url: str, verify:bool=True,timeout:int=200,proxy_json_path:str="proxy.json") -> dict:
        """Getting new proxy for the given url"""

        proxy_website_url = 'https://www.us-proxy.org/'

        # getting page content of the proxy list page
        proxy_df = pd.read_html(requests.get(url, timeout=200).text)

        # checking if the url which needs proxy is secured or not
        # and filtering the proxy list based on that
        if "https" in url:
            proxy_df = proxy_df[0][proxy_df[0]['Https'] == 'yes']
            key = "https"
        else:
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

                    # GIL will happen at this place
                    with open(Path(r"proxy\proxy.json"), 'w') as write_file:
                        json.dump(proxy_dict, write_file)
                        time.sleep(2)
                        logging.info(f'Wrote new proxies')
                    return proxy_dict
            
            except Exception as e:
                logging.info(f"Proxy {proxy_dict} {count} failed because of {e}")
                continue
        raise Exception("No Proxy Found !")

    def get_working_proxy_for_url(self, url: str, method: list) -> dict:
        try:
            if requests.get(url, proxies=self.__proxy).ok:
                return self.__proxy
            else:
                pass
        except:
            pass
            return dict()

    @staticmethod
    def get_proxy_by_location(location: str) -> dict:
        # using default dict so that if someone passes wrong country code it will not through KeyError
        dict_of_proxies_by_location = defaultdict(lambda x: None)
        # use the following site for proxies
        # http://free-proxy.cz/en/proxylist/country/US/https/ping/all
        dict_of_proxies_by_location.update(dict(us={
            "http": "http://132.226.36.165:3128",
            "https": "https://104.129.196.54:8800",
            "ftp": "ftp://10.10.1.10:3128"
        }))
        # if correct, provides location proxy dict else None
        if location:
            return dict_of_proxies_by_location[location]
        # if location is None returns None
        return dict()

    @staticmethod
    def get_new_us_proxy(url_to_check: str, verify: bool = True) -> dict:
        url = 'https://www.us-proxy.org/'

        is_https = "https" in url_to_check

        dfs = pd.read_html(requests.get(url, timeout=200).text)

        if is_https:
            df = dfs[0][dfs[0]['Https'] == 'yes']
            key = "https"  # this is due to 'https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname'
            # test_url = "https://www.mcallen.net/departments/bridge/mcallen-hidalgo"
        else:
            df = dfs[0][dfs[0]['Https'] == 'no']
            key = "http"
            # test_url = "http://www.ritba.org/tolls-2/"

        proxy_json_path = Path(
            r'G:\Shared drives\a_03_Map_Python\tollguru_tollroads\common\proxy.json')

        with open(proxy_json_path, "r") as read_file:
            proxy_dict = json.load(read_file)
        # # Commenting next block for websites like http://www.bcbridges.org/toll-rates-e-zpass/
        # try:
        #     # check if proxy is even needed
        #     if requests.get(url_to_check).ok:
        #         print(f"Proxy is not needed")
        #         return None
        # except Exception as e:
        try:
            if requests.get(url_to_check, proxies=proxy_dict, verify=verify, timeout=200).ok:
                time.sleep(2)
                print(f"Using existing proxies {proxy_dict}")
                return proxy_dict
        except Exception as e:
            for count, proxy in enumerate(df.iterrows()):
                # proxy_dict[key] = f"{key}://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
                proxy_dict[key] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
                try:
                    if requests.get(url_to_check, proxies=proxy_dict, verify=verify, timeout=200).ok:
                        print(f"Using proxy {proxy_dict}")
                        with open(proxy_json_path, 'w') as write_file:
                            json.dump(proxy_dict, write_file)
                            time.sleep(2)
                            print(f'Wrote new proxies')
                        return proxy_dict
                except Exception as e:
                    print(f"Proxy {proxy_dict} {count} failed because of {e}")
                    continue
        raise Exception('NO_PROXIES_FOUND')

    @staticmethod
    def get_proxy_rotator() -> dict:
        proxy_url = 'https://free-proxy-list.net/'
        df = pd.read_html(requests.get(proxy_url, headers={
                          'User-Agent': Proxy.get_random_ua()}).text)[0]
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
    print(proxy.user_agent)


if __name__ == "__main__":
    # proxy = Proxy.get_new_us_proxy(url_to_check="https://www.netrma.org/net-rma-policies/toll-rates/")
    # print(requests.get(url="https://www.netrma.org/net-rma-policies/toll-rates/", proxies=proxy).ok)
    # print(Proxy.get_new_us_proxy(url_to_check="https://www.mcallen.net/departments/bridge/anzalduas"))
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    main()
