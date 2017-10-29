import urllib
import sys
import json
import codecs
import re
import cfscrape
from bs4 import BeautifulSoup

#get HTML from link
def get_html(url):
    try:
        return urllib.urlopen(url).read()
    except StandardError as e:
        print "Error getting HTML: " + str(e)

def get_html_cloud(url):
    try:
        scraper = cfscrape.create_scraper()
        return scraper.get(url).content
    except StandardError as e:
        print "Error getting HTML: " + str(e)

def save_list_to_file(path, thelist):
    thefile = open(path, 'w')
    for item in thelist:
        thefile.write("%s\n" % item)

def load_dictionary_from_json(file):
    with open (file) as data_file:
        return json.load(data_file)

def save_dictionary_to_json(path, jsonDump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(jsonDump, indent=3))

def strip_refs(single):
    return re.sub(r"\?[ref|fref]+=[a-zA-Z.-]+","", single)

def strip_numbers(single):
    return re.sub(r"\/[0-9]+","",single)

def strip_btctalk_noise(single):
    return re.sub(r"(;all|\.[0-9|msg|new]+((;prev_next=prev#new)|(;prev_next=next#new))?[#msg[0-9]*]?)", "",single)

def strip_domain(domain, single):
    output = re.sub(domain,"",single)
    return output.strip("/")

#print strip_domain(r"(http(s)?:\/\/)?(www\.)?facebook\.com\/","https://facebook.com/groups/darcrus")
#print strip_domain(r"(http(s)?:\/\/)?(www\.)?twitter\.com\/", "https://twitter.com/darcrus")
#print strip_domain(r"(http(s)?:\/\/)?(www\.)?github\.com\/","https://github.com/sigwotechnologies" )

#print strip_refs("https://www.facebook.com/groups/evergreencoincurrency/?ref=evergreencoin.org")
#print strip_refs("https://www.facebook.com/reggiemiddletonfintech/?fref=ts")

#print strip_numbers("https://www.facebook.com/pages/hobonickels-hbn-crypto-currency/672818916094322")
#print strip_numbers("https://www.facebook.com/groups/148397155706069/")

#print strip_btctalk_noise("index.php?topic=1764573.60")