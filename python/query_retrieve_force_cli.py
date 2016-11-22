import time
import os
import json

from simple_salesforce import Salesforce


def read_credentials(file_store_name, key):
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


#send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')


def execute_soql_query(sql_statement):
    """Will execute inputted SOQL statement to authenticated Salesforce org."""
    sfdc_token = read_credentials('salesforce', 'sfdc_token')
    sfdc_username = read_credentials('salesforce', 'sfdc_username')
    sfdc_password = read_credentials('salesforce', 'sfdc_password')

    sf = Salesforce(username=sfdc_username, password=sfdc_password, security_token=sfdc_token)
    enviornment_hub_results = sf.query(sql_statement)
    return enviornment_hub_results

test_query = "SELECT  SFDCID__C IsActive_Status_Not_Active FROM Contact"
test_query2 = "Select ID from Contact"
#print(execute_soql_query(test_query))

import subprocess
import shutil
import pprint
#subprocess.run(["force"], shell=True)

def execute_command(command):
    output = None
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output.decode()

print(execute_command(["force", "logins"]))r