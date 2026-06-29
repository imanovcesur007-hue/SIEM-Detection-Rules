import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_HOST = os.getenv("SPLUNK_HOST")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")
TELEGRAM_TOKEN = "8875580959:AAEOvW7ZPzygkQwxc2vfsJT-FZt3P5jwCDc"
TELEGRAM_CHAT = "-1004353279755"

HEADERS = {"Authorization": f"Bearer {SPLUNK_TOKEN}"}
webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT}&text=SOC+ALERT:+Hücum+aşkarlandı!"

def deploy_rule(rule_name, spl_query):
    endpoint = f"{SPLUNK_HOST}/services/saved/searches"
    data = {
        "name": rule_name,
        "search": spl_query,
        "cron_schedule": "*/1 * * * *",
        "is_scheduled": "1",
        "dispatch.earliest_time": "-1m",
        "dispatch.latest_time": "now",
        "action.webhook": "1",
        "action.webhook.param.url": webhook_url
    }
    
    response = requests.post(endpoint, headers=HEADERS, data=data, verify=False)
    if response.status_code in [200, 201]:
        print(f"[+] Uğurla əlavə edildi: {rule_name}")
    else:
        print(f"[-] Xəta baş verdi {rule_name}: {response.text}")

with open('rules/owasp_rules.json', 'r') as f:
    rules = json.load(f)
    for rule in rules:
        deploy_rule(rule['name'], rule['search'])
