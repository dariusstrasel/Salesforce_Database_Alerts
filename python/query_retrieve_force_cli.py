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
import sys


def import_queries(file_path):
    # Parses each line of the ./inputs/queries.csv file and executes them in OS shell using force-cli
    query_file_path = file_path
    query_list = {}
    with open(query_file_path, 'r') as file:
        query_list = csv.DictReader(file, delimiter=',')
        return [command.run_query(sql_statement['query']) for sql_statement in query_list]


def run_tests(accounts_path, tests_path):
    # Parses each line of .inputs/accounts.csv, logs into using force-cli and executes each test case
    # print(">>>read_credentials: " + accounts_path)
    tests_file_path = accounts_path
    account_list = {}
    with open(tests_file_path, 'r') as file:
        account_list = csv.DictReader(file, delimiter=',')
        for account in account_list:
            command.login(account['username'], account['pw'])
            command.run_queries(tests_path)
            break  # Stops the loop from processing every account; just for testing


def send_email(user, pwd, recipient, subject, body):
    # Sends an email using passed in arguments, catches errors in try/except
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
    """This class file serves as a force-cli wrapper library for Python. This will execute each command using the
    subprocess Python module."""
    def __init__(self):

        """Do stuff which will login and create an active session with Salesforce?"""
        pass

    def execute(command):
        """This method will execute the string statement passed in."""
        output = None
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output.decode()

    def login(username, password):
        """Used to pass a login to force-cli using username, password arguments."""
        return command.execute("force login -u=%s -p=%s" % (username, password))

    def run_query(sql_statement):
        """Will execute a single SOQL statement."""
        return command.execute("force query " + sql_statement)

    def run_queries(file_path):
        """Will execute n amount of SOQL statements based on parsed query file."""
        query_filename = file_path
        query_list = {}
        with open(query_filename, 'r') as file:
            query_list = csv.DictReader(file, delimiter=',')
            return [command.run_query(query['query']) for query in query_list]

    def output_command(self, command):
        pass


        """
        $Results = Import-CSV -delimiter ',' .\output_query_file.csv | where RecordCount -gt 0

        foreach($row in $results)
        {
            $message += $row.Account + ' has failed rule ' + $row.RuleName + ' by ' + $row.RecordCount + ' records'+ "`n"
        }
        """


class log:


    def __init__(self, filename):
        """This uses a passed in 'filename' argument to create a log file with the same name."""
        self.filename = filename

    def open_file(self, filename):
        """TODO: write 'with open' code, to reduce redundant open calls in following methods"""
        pass

    def write(self, text):
        "Writes a single line to specified filename. Can refer to preexisting log files."
        with open(self.filename, 'w', newline=' ') as csvfile:
            log_file = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            log_file.writerow(text)

    def write_csv(self, fields):
        """Will write to a csv file """
        with open(self.filename, 'w') as csvfile:
            fieldnames = list(fields[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
            writer.writeheader()
            return [writer.writerow(item) for item in fields]




#send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')

#print(run_tests("../outputs/accounts.csv", "../inputs/queries.csv"))
python_output_query_file = log('../outputs/python_output_query_file.csv')

dict_list = [{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}, {'first_name': 'Wonderful', 'last_name': 'Spam'}]
# python_output_query_file.write_log(dict_list)

print(command.login("mxw_cmx@preventure.com","cmxforc3"))
print(command.run_query("SELECT COUNT(SFDCID__C) Active FROM Contact where mxw__Is_Active__c = true"))

def main():
    pass
    # If no args are specified, print "Nothing specified" and return pass
    # If args specified, pass them into "run_tests", arg[0] should be account path and arg[1] should be test path,
    # while arg[2] can flag whether emails should be sent. Default False, unless explicitly passed.

if __name__ == "__main__":
    main()