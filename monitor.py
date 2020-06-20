# -*- coding: utf-8 -*-
import sys
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware

def query_sealer(config, sealer_name):
    try:
        rpc_port = config[sealer_name]['rpc_port']
        rpc_url = 'http://localhost:%s' % rpc_port
        provider = Web3.HTTPProvider(rpc_url)
        w3 = Web3(provider)
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        block_number = w3.eth.blockNumber
        result = {'block_number': block_number, 'block_hashes':[]}
        for tmp_block_number in range(block_number - 12, block_number + 1):
            block_info = w3.eth.getBlock(tmp_block_number)
            block_hash = block_info['hash']
            result['block_hashes'].append(block_hash)
        result['block_hashes'] = list(reversed(result['block_hashes']))
        return result
    except:
        return {}

def start_monitor(config):
    while True:
        lines = '--------------------------------------------------------------------------------------------------------------------------\n'
        lines += 'sealer\tblock\t%s\n' % ''.join(['hash#%s\t'%i for i in range(13)])
        lines += '--------------------------------------------------------------------------------------------------------------------------\n'
        for k,v in config.items():
            sealer_info = query_sealer(config, k)
            if sealer_info:
                block_number = sealer_info['block_number']
                block_hashes = [item.hex()[:6] for item in sealer_info['block_hashes']] # only show the prefix 6 characters
                line = "{0}\t{1}\t{2}\n".format(k, block_number, '\t'.join(block_hashes))
                lines += line
        sys.stdout.write(lines)
        sys.stdout.flush()
        time.sleep(3)
