import requests
import os
import json
import logging
import argparse
from dotenv import load_dotenv

# Load Enviroment Variables
load_dotenv()

# Logging Configuration
logging.basicConfig(filename="./cloudflare-public-ip.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s",datefmt='%m-%d-%y %H:%M:%S', level=logging.INFO)

def main():
    public_ip = get_public_ip()
    dns_record = get_dns_record(record="impulse.gorobei.net")["result"][0]    
    if public_ip != dns_record["content"]:
        logging.info("The public ip was change.")
        update_dns_record(record="impluse.gorobei.net", content=public_ip)
        logging.info("The DNS record was updated.")
    else:
        logging.info("Everthing it's ok, nothing changes.")

def get_public_ip():
    req = requests.get('http://api.ipify.org?format=json')
    public_ip = req.json()["ip"]
    if req.status_code == 200:
        return public_ip
    else:
        logging.error("Erro on get public ip, status code: {}".format(req.status_code))

def update_dns_record(record, content):
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Key":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_KEY")),
        "X-Auth-Email":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_EMAIL"))
    }
    data = {
        "type":"A",
        "name":record,
        "content":content,
        "ttl":120
    }
    req = requests.put("{}{}".format(os.getenv("CLOUDFLARE_ENDPOINT"),"/dns_records/ac0474a0daaa527043a211583966ef5f"), headers=headers, data=json.dumps(data))
    if req.status_code == 200:
        return req.json
    else:
        logging.error("{}".format(req.json()))

def create_dns_record(record, content):
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Key":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_KEY")),
        "X-Auth-Email":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_EMAIL"))
    }
    data = {
        "type":"A",
        "name":record,
        "content":content,
        "ttl":120,
        "priority":10,
        "proxied": False
    }
    req = requests.post("{}{}".format(os.getenv("CLOUDFLARE_ENDPOINT"),"/dns_records"), headers=headers, data=json.dumps(data))
    response = req.json()
    errors = response["errors"][0]
    if errors["code"] == 81057:
        logging.warning("{}".format(req.json()))
        update_dns_record(record=record)
    if req.status_code == 200:
        return req.json()
    else:
        logging.error("{}".format(req.json()))

def get_dns_record(record):
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Key":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_KEY")),
        "X-Auth-Email":"{}".format(os.getenv("CLOUDFLARE_X_AUTH_EMAIL"))
    }
    params = {
        "name":record,
        "type":"A"
    }
    req = requests.get("{}{}".format(os.getenv("CLOUDFLARE_ENDPOINT"),"/dns_records"), headers=headers, params=params)
    if req.status_code == 200:
        return req.json()
    else:
        logging.error("{}".format(req.json()))       

if __name__ == "__main__":
    main()

