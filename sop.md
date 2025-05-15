# Automated Incident Reporting System

## Overview
This tool monitors system logs and health metrics and automatically logs incidents to ServiceNow via REST API.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` file with ServiceNow credentials.
4. Configure cron job using `crontab -e`.

## Usage
Run manually:
```bash
python3 incident_reporter.py
