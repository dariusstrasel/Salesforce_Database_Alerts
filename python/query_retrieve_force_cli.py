'''Title: Maxwell Alerts
    Author: Darius Strasel
    Objective:
    Run test cases on accounts within Maxwell and email specified people if they fail.
    Workflow:
    1. Import './test_output.txt'
    2. Create table for holding Account, RuleName, and the RecordCount as result of the test
    3. Use test import to populate table with test information from .CSV
    4. Export resulting table to 'output_query_file.csv'
    ############## BEGIN RUNNING QUERIES ################
    5. Create output file for test results
    6. Import './accounts.csv' # Used to login using the account's admin user
    7. Create test list
    8. Run test equeries for the accounts imported from file.
    9. Save queries to output file
    ########### START EMAILING RESULTS ###############
    10. Send email for each failed row in results.
'''

import time
import os
import json
import csv
import subprocess

def read_credential(file_store_name, key):
    print(">>>read_credentials: " + file_store_name)
    secrets_filename = file_store_name
    api_keys = {}
    try:
        with open(secrets_filename, 'r') as f:
            try:
                api_keys = json.loads(f.read())
                print(">>>: " + key)
                return api_keys[key]
            except json.JSONDecodeError:
                print("'" + key + "'" + " key is missing from secrets file.")
    except FileNotFoundError:
        print("No secrets file detected. Creating new one...")
        new_file = open(secrets_filename, 'w')
        # new_file.write('{"sfdc_token": "token","sfdc_username": "token","sfdc_password": "token"}')

def send_email(user, pwd, recipient, subject, body):
    print(">>>send_email: " + "To: " + recipient + " From: " + user)
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('Successfully sent the mail')
    except:
        print("Failed to send mail")

class session:

    token = read_credential('salesforce', 'sfdc_token')
    username = read_credential('salesforce', 'sfdc_username')
    password = read_credential('salesforce', 'sfdc_password')

    is_logged_in = False

    def login_state(self):
        pass

    def create_login_session(self):
        command.execute(["force", "login", "-u ", session.username, "-p ", session.password])

class command:

    def __init__(self):
        """Do stuff which will login and create an active session with Salesforce?"""
        print(session.is_logged_in)
        pass

    def execute(command):
        """Static method."""
        output = None
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output.decode()

def csv_read(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['first_name'], row['last_name'])

def csv_write(file, file_rows):
    with open(file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(file_rows)

class testrunner:

    queries = ["SELECT COUNT(SFDCID__C) IsActive_Status_Not_Active FROM Contact where (mxw__Is_Active__c = true and Status__c != ''Active'') OR (mxw__Is_Active__c = false and Status__c = ''Active'')","SELECT COUNT(SFDCID__C) Active FROM Contact where mxw__Is_Active__c = true", "SELECT COUNT(SFDCID__C) Inactive FROM Contact where mxw__Is_Active__c = false"  ]

    def email_results(self):
        """
        $Results = Import-CSV -delimiter ',' .\output_query_file.csv | where RecordCount -gt 0

        foreach($row in $results)
        {
            $message += $row.Account + ' has failed rule ' + $row.RuleName + ' by ' + $row.RecordCount + ' records'+ "`n"
        }
        """
    def __init__(self):
        pass

class log:
    """Create log file and log results into file"""



#send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')
