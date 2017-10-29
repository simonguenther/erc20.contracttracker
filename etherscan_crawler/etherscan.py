import json, re
from Helper import get_html_cloud, save_dictionary_to_json, save_list_to_file
from bs4 import BeautifulSoup
from time import gmtime, strftime

baseURL = "https://etherscan.io/token/generic-tokentxns2?contractAddress=0x2C974B2d0BA1716E644c1FC59982a89DDD2fF724&mode=&p="

all_regex = r"A\sTotal\sof\s[0-9]*\sevents\sfound"

all_hashes = []

def get_total_number_of_transactions(url):
    html = get_html_cloud(baseURL+"1")
    #print html
    results = re.findall(all_regex, html, 0)
    results = results[0].split(' ')
    return results[3]

def get_tx_hashes_from_page(html):
    soup = BeautifulSoup(html, "lxml")
    hashes = []
    for results in soup.findAll("span", { "class": "address-tag"}):
        if len(results.text) == 66:
            hashes.append(results.text)
    return hashes

total_txs = get_total_number_of_transactions(baseURL)
pages = int(total_txs)/50
print str(strftime("%H:%M:%S", gmtime()))+ ": Total number of transactions: %s (%s pages)" % (total_txs, pages+1)

for i in range (1, pages+2):
    print str(strftime("%H:%M:%S", gmtime())) + ": Processing page %s / %s" % (i, pages+1)
    url = baseURL + str(i)
    html = get_html_cloud(url)
    page_hashes = get_tx_hashes_from_page(html)
    all_hashes.extend(page_hashes)

print "Transaction hashes collected: %s " % str(len(all_hashes))
save_list_to_file("all_viberate_transaction_hashes.txt", all_hashes)