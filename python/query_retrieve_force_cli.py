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
import csv
import subprocess

def import_queries(file_path):
    secrets_filename = file_path
    query_list = {}
    with open(secrets_filename, 'r') as file:
        query_list = csv.DictReader(file, delimiter=',')
        return [command.run_query(query['query']) for query in query_list]

def run_tests(accounts_path, tests_path):
    print(">>>read_credentials: " + accounts_path)
    secrets_filename = accounts_path
    account_list = {}
    with open(secrets_filename, 'r') as file:
        account_list = csv.DictReader(file, delimiter=',')
        for account in account_list:
            command.login(account['username'], account['pw'])
            command.run_queries(tests_path)
            break


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


class command:

    def __init__(self):
        """Do stuff which will login and create an active session with Salesforce?"""
        pass

    def execute(command):
        """Static method."""
        output = None
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            output = e.output
        print(output.decode())
        return output.decode()

    def login(username, password):
        return command.execute("force login -u=%s -p=%s" % (username, password))

    def run_query(sql_statement):
        return command.execute("force query " + sql_statement)

    def run_queries(file_path):
        query_filename = file_path
        query_list = {}
        with open(query_filename, 'r') as file:
            query_list = csv.DictReader(file, delimiter=',')
            return [command.run_query(query['query']) for query in query_list]


        """
        $Results = Import-CSV -delimiter ',' .\output_query_file.csv | where RecordCount -gt 0

        foreach($row in $results)
        {
            $message += $row.Account + ' has failed rule ' + $row.RuleName + ' by ' + $row.RecordCount + ' records'+ "`n"
        }
        """


class log:


    def __init__(self, filename):
        self.filename = filename

    def write(self, text):
        with open(self.filename, 'w', newline=' ') as csvfile:
            log_file = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            log_file.writerow(text)

    def write_log(self, fields):
        with open(self.filename, 'w') as csvfile:
            fieldnames = list(fields[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
            writer.writeheader()
            return [writer.writerow(item) for item in fields]




#send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')

#print(run_tests("../outputs/accounts.csv", "../inputs/queries.csv"))
python_output_query_file = log('../outputs/python_output_query_file.csv')

dict_list = [{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}, {'first_name': 'Wonderful', 'last_name': 'Spam'}]
python_output_query_file.write_log(dict_list)
