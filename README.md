# Step 1: Set Up Environment

Install Required Python Packages:


```
pip install requests python-dotenv boto3
```
Directory Structure Example:


```
incident_tool/
│
├── incident_reporter.py         # Main script
├── config.env                   # Environment variables
├── logs/system.log              # Example log file
├── sop.md                       # Documentation
└── cronjob_setup.txt            # Crontab instructions
```
#Step 2: Create config.env

Store secrets here securely (don’t commit this to version control):


```
SERVICENOW_INSTANCE=https://yourinstance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
SERVICENOW_TABLE=incident
```
#Step 3: incident_reporter.py – Main Script

[Code](https://github.com/sexywebdev/AutoIncident-Bot/blob/main/incident_reporter.py)


#Step 4: Setup Cron Job on Linux
Edit Crontab:
```
crontab -e
```

Add this to run every 15 minutes:

```
*/15 * * * * /usr/bin/python3 /path/to/incident_tool/incident_reporter.py
```

You can redirect errors to a file too:

```
*/15 * * * * /usr/bin/python3 /path/to/incident_tool/incident_reporter.py >> /path/to/incident_tool/cron.log 2>&1
```
#Step 5: Sample sop.md Documentation
[sop.md](https://github.com/sexywebdev/AutoIncident-Bot/blob/main/sop.md)




