# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 16:04:28 2021

@author: pavelchandra99@gmail.com
"""

import logging
  
logger = logging.getLogger(__name__)

def main():
  pass

if __name__ == "__main__":

  logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler('tollwiki_regular_backup.log', mode='a'),
                                  logging.StreamHandler()])

  main()
