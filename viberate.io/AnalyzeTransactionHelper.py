from Helper import print_dict, get_logs, load_dictionary_from_json, log, send_request, get_block_number, get_from, get_input, get_method, get_status, get_to, get_to_addr_from_input, get_transaction, get_transaction_receipt, get_transaction_value, get_value_from_input

WEI_TO_VIB = 1e-18
WEI_TO_ETH = 1e-18

def crowdsale(tx):
    tmp = basic(tx)
    tmp["type"] = "crowdsale"
    
    ret_receipt = get_transaction_receipt(tx["hash"])
    logs = get_logs(ret_receipt)
    if logs:
        # overwrite values from basic()
        tmp["erc20_to"] = ret_receipt["from"]
    return tmp

def angel(tx):
    tmp = basic(tx)
    tmp["type"] = "angel"
    return tmp

def transfer(tx):
    tmp = basic(tx)
    tmp["type"] = "transfer"
    return tmp

def team_tokens(tx):
    tmp = basic(tx)
    tmp["type"] = "team_tokens"
    return tmp

def transaction_succeess(fin):
    byzantium = 4370000
    if fin["blockNumber"] >= byzantium:
        if fin["status"]:
            return True
        else:
            return False
    return (fin["gas_used"] < fin["gas_limit"])
    

def basic(tx):
    tmp = {}
    tmp["blockNumber"] = int(tx["blockNumber"],16)
    tmp["tx_from"] = tx["from"]
    tmp["hash"] = tx["hash"]
    tmp["tx_to"] = tx["to"]
    tmp["type"] = "crowdsale"
    tmp["erc20_to"] = "0x"+get_to_addr_from_input(tx["input"])

    eth_value = tx["value"]
    if eth_value == "0x0":
        tmp["eth_value"] = 0
    else:
        tmp["eth_value"] = int(eth_value,16) * WEI_TO_ETH # change it back to ,16?

    ret_receipt = get_transaction_receipt(tx["hash"])
    tmp["gas_used"] = int(ret_receipt["gasUsed"],16)
    tmp["gas_limit"] = int(tx["gas"],16)


    if "status" in ret_receipt.keys():
        tmp["status"] = int(ret_receipt["status"],16)
    
    logs = get_logs(ret_receipt)
    if logs:
        tmp["erc20_value"] = int(logs[0]["data"],16) * WEI_TO_VIB

    tmp["success"] = transaction_succeess(tmp)
    return tmp

