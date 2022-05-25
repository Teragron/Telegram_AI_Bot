# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 01:46:37 2022

@author: ahmet
"""

symbols = [["bitcoin","BTC"],
             ["ethereum","ETH"],
             ["tether","USDT"],
             ["cardano","ADA"],
             ["ripple","XRP"],
             ["solana","SOL"],
             ["polkadot","DOT"],
             ["dogecoin","DOGE"],
             ["dai","DAI"],
             ["monero","XMR"],
             ["litecoin","LTC"],
             ["algorand","ALGO"],
             ["tezos","XTZ"],
             ["iota","MIOTA"],
             ["eos","EOS"],
             ["zcash","ZEC"],
             ["nano","XNO"],
             ]

import requests
def get_current_data(from_sym='BTC', to_sym='USD', exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()
    return data











