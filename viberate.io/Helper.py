import json
import random
import requests
import time
import codecs

WEI_TO_VIB = 1e-18

# load dictionary from JSON-file
def load_dictionary_from_json(filename):
    with open (filename) as data_file:
        return json.load(data_file)

def log(*args):
  print('-' * 40)
  print(time.ctime())
  print(args)

def load_list_from_file(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return lines

def print_dict(d):
    print json.dumps(d, indent=3)

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
    except StandardError as Ex:
        pass
    raise Exception('No result returned')


def get_transaction(tx_hash):
    receipt = send_request({
        'method': 'eth_getTransactionByHash',
        'params': [tx_hash]
    })  
    return receipt

def get_transaction_receipt(tx_hash):
    receipt = send_request({
        'method': 'eth_getTransactionReceipt',
        'params': [tx_hash]
    })  
    return receipt

def get_block_number(receipt):
    return int(receipt["blockNumber"],16)

def get_from(receipt):
    return receipt["from"]

def get_to(receipt):
    return receipt["to"]

def get_logs(receipt):
    if not receipt["logs"]:
        return None
    else: 
        return receipt["logs"]

def get_status(receipt):
    return receipt["status"]

def get_input(transaction):
    return transaction["input"]

def get_transaction_value(transaction):
    return int(transaction["value"],16)

def get_method(input):
    if (len(input) - 8 - 2) % 64 != 0:
        raise Exception('Data size misaligned with parse request')
    return input[:10]

def get_to_addr_from_input(input):
    #print input
    params = input[10:]
    return params[:64].strip('0')

def get_value_from_input(input):
    params = input[10:]
    value = params[64:]
    value = int(value, 16) * WEI_TO_VIB
    return value

# save dictionary to JSON-file
def save_dictionary_to_json(path, jsonDump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(jsonDump, indent=3))