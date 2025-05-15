import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import logging
import datetime
from typing import List, Optional

# Load config
load_dotenv()

# Logging Setup
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'system.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# ServiceNow Config
SN_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
SN_USER = os.getenv("SERVICENOW_USERNAME")
SN_PASS = os.getenv("SERVICENOW_PASSWORD")
SN_TABLE = os.getenv("SERVICENOW_TABLE")

# Validate environment
required_env = [SN_INSTANCE, SN_USER, SN_PASS, SN_TABLE]
if not all(required_env):
    missing = [var for var, val in zip(
        ["SERVICENOW_INSTANCE", "SERVICENOW_USERNAME", "SERVICENOW_PASSWORD", "SERVICENOW_TABLE"], required_env) if not val]
    logging.critical(f"Missing required environment variables: {', '.join(missing)}")
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

def check_system_health() -> List[str]:
    """Perform basic system health checks."""
    health_issues = []
    try:
        cpu_load = os.getloadavg()[0]
        if cpu_load > 2.0:
            health_issues.append(f"High CPU Load: {cpu_load:.2f}")
    except (AttributeError, OSError):
        # os.getloadavg may not be available on all platforms
        pass

    try:
        disk_usage = os.popen("df -h /").read()
        if "100%" in disk_usage:
            health_issues.append("Disk usage critical.")
    except Exception as e:
        logging.error(f"Disk usage check failed: {e}")

    return health_issues

def create_servicenow_ticket(
    short_desc: str,
    description: str,
    urgency: str = "2",
    category: str = "inquiry"
) -> Optional[dict]:
    """Create an incident ticket in ServiceNow."""
    url = f"{SN_INSTANCE}/api/now/table/{SN_TABLE}"
    headers = {"Content-Type": "application/json"}
    auth = (SN_USER, SN_PASS)
    data = {
        "short_description": short_desc,
        "description": description,
        "urgency": urgency,
        "category": category
    }
    try:
        response = requests.post(url, auth=auth, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        if response.status_code == 201:
            logging.info("Ticket created successfully.")
            return response.json()
        else:
            logging.error(f"Ticket creation failed: {response.text}")
    except requests.RequestException as e:
        logging.error(f"ServiceNow request failed: {e}")
    return None

def parse_logs(log_path: Path) -> List[str]:
    """Parse a log file for ERROR or CRITICAL entries."""
    issues_found = []
    try:
        with log_path.open('r') as f:
            for line in f:
                if "ERROR" in line or "CRITICAL" in line:
                    issues_found.append(line.strip())
    except Exception as e:
        logging.error(f"Failed to read log {log_path}: {e}")
    return issues_found

def main():
    errors = parse_logs(LOG_FILE)
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
        logging.error(f"Script failure: {e}")
