# Script Cloudflare Public IP #


After clone the repositoriy and install the dependences `(pip3 install -r requirements.txt)`, it's necessary create a .env file with the cloudflare tokens

`CLOUDFLARE_ENDPOINT = "" `
`CLOUDFLARE_X_AUTH_KEY = ""`
`CLOUDFLARE_X_AUTH_EMAIL = ""`
`CLOUDFLARE_AUTHORIZATION = ""`

## Usage ##

~$ python cloudflare-public-ip.py -h

usage: cloudflare-public-ip.py [-h] [-dns --dns-record]

Script Cloudflare Public IP

optional arguments:
  -h, --help         show this help message and exit
  -dns --dns-record  DNS record to update.