import json
import requests
import random
import codecs
import time

BANCOR_SMART_CONTRACT = '0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c'
ENIGMA_SMART_CONTRACT = '0xf0Ee6b27b759C9893Ce4f094b49ad28fd15A23e4'
                         
VIBERATE_SMART_CONTRACT = '0x57D02550f47dd932d2fB84E0aA883C9D8d53C313'

WEI_TO_ETH = 1e-18
BNT_TO_ETH = 1e-2
BLOCK_START =   4358024
BLOCK_END = 4393704

def log(*args):
  print('-' * 40)
  print(time.ctime())
  print(args)

def get_transaction(tx_hash):
    url = 'http://localhost:8545'
    headers = {'content-type': 'application/json'}
    request = {
        'jsonrpc': '2.0', 'id': 1,
        'method': 'eth_getTransactionByHash',
        'params': [tx_hash]
    }
    answer = requests.post(url, data=json.dumps(request), headers=headers).json()
    return answer

def print_dict(d):
    print json.dumps(d, indent=3)

def save_dictionary_to_json(path, jsonDump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(jsonDump, indent=3))

def wei_to_eth(amount):
    return str(int(amount,16) * WEI_TO_ETH)

def send_request(request):
    url = 'http://localhost:8545'
    headers = {'content-type': 'application/json'}
    payload = {'jsonrpc': '2.0', 'id': random.randint(0, int(1e9))}
    payload.update(request)
    response = None
    while not response:
        try:
            raw_block =requests.post(url, data=json.dumps(payload), headers=headers).json() 
            #print raw_block
            response = raw_block
        except requests.exceptions.ConnectionError as e:
            pass
    if response[u'id'] != payload['id']:
        raise Exception('Returned mismatching id')
    try:
        return response[u'result']
    except KeyError:
        log('No result found!', response)
    raise Exception('No result returned')

def save_list_to_file(liste):
    thefile = open('test.txt', 'w')
    for item in liste:
        thefile.write("%s\n" % item)

def get_block(block_height):
    bh = block_height
    block = send_request({
            'method': 'eth_getBlockByNumber',
            'params' : [hex(int(bh)), True]
        })
    return block
    #save_dictionary_to_json('test.json', block)

def to_from_is_enigma_transaction(raw_tx):
    if raw_tx["to"] is None:
        to = '0xc738af467fe2614fccc3ad1b2b8eb14e60436123'
    else:
        to = raw_tx["to"].lower()
    if raw_tx["from"] is None:
        from_ = '0xc738af467fe2614fccc3ad1b2b8eb14e60436123'
    else:
        from_ = raw_tx["from"].lower()
    
    if ENIGMA_SMART_CONTRACT.lower() in [to, from_]:
        return True
    return False

def monitor():
    tx_set = []
    count = 0
    one_percent = (BLOCK_END - BLOCK_START) // 100
    for block_number in range(BLOCK_START,BLOCK_END):
        if (block_number - BLOCK_START) % one_percent == 0:
            print('{0}% done'.format((block_number - BLOCK_START) // one_percent))
        block = send_request({
            'method': 'eth_getBlockByNumber',
            'params' : [hex(block_number), True]
        })
        
        #print "Number of transactions: " + str(len(block["transactions"]))
        count +=1
        for tx in block["transactions"]:
            try:
            
                if to_from_is_enigma_transaction(tx):
                    tx_set.append(tx)
                
                
            except StandardError as ex:
                print ex
    save_list_to_file(tx_set)

monitor()
