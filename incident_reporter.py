import requests
import os
from dotenv import load_dotenv
import datetime
import logging

# Load config
load_dotenv()

# Logging Setup
logging.basicConfig(filename='logs/system.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# ServiceNow Config
SN_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
SN_USER = os.getenv("SERVICENOW_USERNAME")
SN_PASS = os.getenv("SERVICENOW_PASSWORD")
SN_TABLE = os.getenv("SERVICENOW_TABLE")

def check_system_health():
    health_issues = []
    
    # Example checks (expand as needed)
    cpu_load = os.getloadavg()[0]
    if cpu_load > 2.0:
        health_issues.append(f"High CPU Load: {cpu_load}")
    
    disk_usage = os.popen("df -h /").read()
    if "100%" in disk_usage:
        health_issues.append("Disk usage critical.")

    return health_issues

def create_servicenow_ticket(short_desc, description, urgency="2", category="inquiry"):
    url = f"{SN_INSTANCE}/api/now/table/{SN_TABLE}"
    headers = {"Content-Type": "application/json"}
    auth = (SN_USER, SN_PASS)
    
    data = {
        "short_description": short_desc,
        "description": description,
        "urgency": urgency,
        "category": category
    }

    response = requests.post(url, auth=auth, headers=headers, json=data)
    
    if response.status_code == 201:
        logging.info("Ticket created successfully.")
        return response.json()
    else:
        logging.error(f"Ticket creation failed: {response.text}")
        return None

def parse_logs(log_path):
    issues_found = []
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "ERROR" in line or "CRITICAL" in line:
                    issues_found.append(line.strip())
    except Exception as e:
        logging.error(f"Failed to read log: {e}")
    
    return issues_found

def main():
    # Parse logs
    errors = parse_logs("logs/system.log")

    # System health
    health = check_system_health()

    issues = errors + health

    if issues:
        description = "\n".join(issues)
        create_servicenow_ticket("Automated Incident Detected", description)
    else:
        logging.info("No incidents to report.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Script failure: {str(e)}")
