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


class Proxy:
    ''' Class to store data related to proxies'''

    @functools.lru_cache
    def __init__(self):
        with open('proxy.json', 'r') as f:
            self.__proxy = json.load(f)
            logging.info(f"Loaded proxy {self.__proxy} from json file")
        with open('user_agents.json', 'r') as f:
            self.__user_agent_list = json.load(f).get("user_agents")
            logging.info(f"Loaded list of user agents from json file")
            logging.info(f"First and last are - {self.__user_agent_list[0]} and {self.__user_agent_list[-1]}")

    @property
    def user_agent(self) -> dict:
        """Provides a random user agent from list of user agents"""
        return {"User-Agent": random.choice(self.__user_agent_list)}

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
    def get_random_ua() -> str:
        user_agents = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
            "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
            "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
            "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
            "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5",
            "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
            "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
            "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
            "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
            "Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
            "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
            "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
            "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0"
        ]

        return user_agents[random.randint(0, len(user_agents) - 1)]

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

        proxy_json_path = Path(r'G:\Shared drives\a_03_Map_Python\tollguru_tollroads\common\proxy.json')

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
        df = pd.read_html(requests.get(proxy_url, headers={'User-Agent': Proxy.get_random_ua()}).text)[0]
        df = df[df['Https'] == 'yes']
        df['http'] = df[['IP Address', 'Port']].apply(lambda x: f'http://{x[0]}:{x[1]}', axis=1)
        df['https'] = df[['IP Address', 'Port']].apply(lambda x: f'https://{x[0]}:{x[1]}', axis=1)
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
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
    main()
