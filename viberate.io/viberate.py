from Helper import load_list_from_file, save_dictionary_to_json, print_dict, get_logs, load_dictionary_from_json, log, send_request, get_block_number, get_from, get_input, get_method, get_status, get_to, get_to_addr_from_input, get_transaction, get_transaction_receipt, get_transaction_value, get_value_from_input
from AnalyzeTransactionHelper import crowdsale, transfer, angel, team_tokens
import json
import random
import requests
import time
from time import gmtime, strftime

block_file = 'viberate_test.json'
output = 'process_etherscan_crawl_4853tx.json'
VIB_SMART_CONTRACT = "0x2C974B2d0BA1716E644c1FC59982a89DDD2fF724"
VIB_CROWDSALE = "0x91c94bee75786fbbfdcfefba1102b68f48a002f4"
HASH = "0x437d35ccddd4dd12a347fd0329f992a9be7abf40a63828f4e90fda2be7062aa0"

TRANSFER_METHOD = '0xa9059cbb'
PUSH_ANGEL_METHOD = '0xf28afb1e'
CLAIM_TEAM_TOKENS_METHOD = '0x826776fa'
WEI_TO_VIB = 1e-18
WEI_TO_ETH = 1e-18

other_txs = {}

def log_other_transaction_type(method, tx_hash):
    if method in other_txs.keys():
        other_txs[method].append(tx_hash)
    else:
        other_txs[method] = [tx_hash]

def analyze(tx):
    fin = {}
    #print tx["hash"]
    """ Values from Transaction """
    
    input = tx["input"]

    if input == "0x":   # probably crowdsale
        fin = crowdsale(tx)
        
    else:
        method = get_method(input)

        if method == PUSH_ANGEL_METHOD: # Angel Investment Distribution
            fin = angel(tx)

        elif method == TRANSFER_METHOD: # Regular Transfer
           fin = transfer(tx)
        
        elif method == CLAIM_TEAM_TOKENS_METHOD:
            fin = team_tokens(tx)

        else:
            print "Unknown method: " + method + " @ " + tx["hash"]
            log_other_transaction_type(method, tx["hash"])

    #print_dict(fin)
    return fin

def process_tx_from_blocks(): #block monitoring
    cnt_sale = 0
    cnt_team = 0
    cnt_transfer = 0
    cnt_other = 0
    cnt_angel = 0
    ana = {}

    # Read Transactions from JSON
    logs = load_dictionary_from_json(block_file)
    print "%s transactions will be processed" % str(len(logs))
    for tx_hash in logs:
        transaction = logs[tx_hash]
        tmp = analyze(transaction)
        if tmp != {}:
            typ = tmp["type"]

            if typ == "crowdsale":
                cnt_sale += 1
            elif typ == "angel":
                cnt_angel += 1
            elif typ == "transfer":
                cnt_transfer += 1
            elif typ == "team_tokens":
                cnt_team += 1
            ana[tx_hash] = tmp
        else:
            cnt_other += 1

    print "Crowdsale:\t %s \nAngel:\t\t %s \nTransfer:\t %s \nTeam:\t\t %s \nOther:\t\t %s " % (str(cnt_sale), str(cnt_angel), str(cnt_transfer), str(cnt_team), str(cnt_other))
    return ana

def process_tx_from_list(): #etherscan.io crawl
    cnt_sale = 0
    cnt_team = 0
    cnt_transfer = 0
    cnt_other = 0
    cnt_angel = 0
    ana = {}

    liste = load_list_from_file('all_viberate_transaction_hashes.txt')

    print str(strftime("%H:%M:%S", gmtime()))+ ": Total number of transactions found: %s" % (str(len(liste)))

    onepercent = len(liste)/100
    counter = 0
    for tx_hash in liste:
        transaction = get_transaction(tx_hash)
        tmp = analyze(transaction)
        if tmp != {}:
            typ = tmp["type"]

            if typ == "crowdsale":
                cnt_sale += 1
            elif typ == "angel":
                cnt_angel += 1
            elif typ == "transfer":
                cnt_transfer += 1
            elif typ == "team_tokens":
                cnt_team += 1
            ana[tx_hash] = tmp
        else:
            cnt_other += 1

        counter += 1
        if counter >= 100:
            break
        print(str(strftime("%H:%M:%S", gmtime())) + ": Processing %s / %s" % (counter, len(liste)))

    print str(strftime("%H:%M:%S", gmtime()))+ ": Finished"
    print "Crowdsale:\t %s \nAngel:\t\t %s \nTransfer:\t %s \nTeam:\t\t %s \nOther:\t\t %s " % (str(cnt_sale), str(cnt_angel), str(cnt_transfer), str(cnt_team), str(cnt_other))
    return ana
    
    
complete = process_tx_from_list()

save_dictionary_to_json(output, complete)
save_dictionary_to_json("other_transactions.json", other_txs)

