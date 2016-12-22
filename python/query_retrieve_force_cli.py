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
import re


def import_queries(file_path):
    # Parses each line of the ./inputs/queries.csv file and executes them in OS shell using force-cli
    print("def import_queries(%s)" % file_path)
    query_file_path = file_path
    query_list = {}
    with open(query_file_path, 'r') as file:
        query_list = csv.DictReader(file, delimiter=',')
        return [command.run_query(sql_statement['query']) for sql_statement in query_list]


def run_tests(accounts_path, tests_path):
    # Parses each line of .inputs/accounts.csv, logs into using force-cli and executes each test case
    # print(">>>read_credentials: " + accounts_path)
    #print("def run_tests(%s, %s)" % accounts_path, tests_path)
    print("test: " + str(__name__))
    tests_file_path = accounts_path
    account_list = {}
    with open(tests_file_path, 'r') as file:
        account_list = csv.DictReader(file, delimiter=',')
        for account in account_list:
            command.login(account['username'], account['pw'])
            command.run_queries(tests_path, account['username'])
            # break  # Stops the loop from processing every account; just for testing


def send_email(user, pwd, recipient, subject, body):
    # Sends an email using passed in arguments, catches errors in try/except
    print("send_email(%s, %s, %s, %,s %s)" % user, pwd, recipient, subject, body)
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

def send_failed_test_email(user, pwd, recipient, subject, account, rule_name, record_count):
    body = "{account} has failed rule '{rule_name}' with a record count of 'record_count)'."
    send_email(user, pwd, recipient, subject, body)

class command:
    """This class file serves as a force-cli wrapper library for Python. This will execute each command using the
    subprocess Python module."""
    def __init__(self):
        pass

    def execute(command):
        """This method will execute the string statement passed in."""
        print("execute(%s)" % command)
        output = None
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output.decode()

    def login(username, password):
        """Used to pass a login to force-cli using username, password arguments."""
        return command.execute("force login -u=%s -p=%s" % (username, password))

    def parse_query_result(query):
        regex = r"\s([0-9]\d*)"
        try:
            return re.findall(regex, query)[0]
        except Exception:
            return query

    def run_query(sql_statement, account):
        """Will execute a single SOQL statement."""
        python_output_query_file = log('../outputs/python_output_query_file.csv')
        query_result = command.execute("force query " + sql_statement)
        dict_list = [{'Account': account, 'Rule_Name': sql_statement, 'Record_Count': command.parse_query_result(query_result)}]
        python_output_query_file.write_csv(dict_list)

        command.execute("force query " + sql_statement)

        return command.execute("force query " + sql_statement)

    def run_queries(file_path, account):
        """Will execute n amount of SOQL statements based on parsed query file."""
        query_filename = file_path
        query_list = {}
        with open(query_filename, 'r') as file:
            query_list = csv.DictReader(file, delimiter=',')
            return [command.run_query(query['query'], account) for query in query_list]


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
        print("def write_csv(%s)" % fields)
        with open(self.filename, 'a') as csvfile:
            fieldnames = list(fields[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
            writer.writeheader()
            return [writer.writerow(item) for item in fields]




def main():
    start_time = time.time()
    print(run_tests("../outputs/accounts.csv", "../inputs/queries.csv"))
    print("--- %s seconds elapsed ---" % (time.time() - start_time))
    # send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')
    send_failed_test_email()
    # command.run_query("SELECT COUNT(SFDCID__C) Active FROM Contact", "test_account")
    # print(command.parse_query_result(" Active -------- 20     (1 records)"))

    # If no args are specified, print "Nothing specified" and return pass
    # If args specified, pass them into "run_tests", arg[0] should be account path and arg[1] should be test path,
    # while arg[2] can flag whether emails should be sent. Default False, unless explicitly passed.

if __name__ == "__main__":
    main()