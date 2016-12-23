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

    TODO:
    -Rewrite log CSVwriter
    -Add try statement to check if force-cli is installed
    -Refactor query runner (ensure single responsibility principal)
    -Add sys.argv to allow CLI level script execution
    -Add CLI input validators (check for 2 parameters, both are paths.)


'''

import os
import time
import csv
import subprocess
from sys import argv
import re
import datetime


class Utility:

    def is_path(input):
        regex = r"(.+)/([^/]+)$"
        if len(re.findall(regex, input)) == 0:
            return False
        return True

    def file_exist(file_path):
        return os.path.exists(file_path)

    def user_input_is_valid(arg_cls):
        if len(arg_cls) < 3:
            print("Not enough parameters passed. Need %s more" % (3 - len(argv)))
            return False
        if file_exist(arg_cls[1]):
            if file_exist(arg_cls[2]):
                print(True)
                return True
        print("'%s' and '%s' are not files/do not exist." % (arg_cls[1], arg_cls[2]))
        return False


# def import_queries(file_path):
#     # Parses each line of the ./inputs/queries.csv file and executes them in OS shell using force-cli
#     print("def import_queries(%s)" % file_path)
#     query_file_path = file_path
#     query_list = {}
#     with open(query_file_path, 'r') as file:
#         query_list = csv.DictReader(file, delimiter=',')
#         return [Command.run_query(sql_statement['query']) for sql_statement in query_list]


# def run_tests(account_input_file, query_input_file):
#     # Parses each line of .inputs/accounts.csv, logs into using force-cli and executes each test case
#     print("def run_tests(%s, %s)" % (account_input_file, query_input_file))
#     with open(account_input_file, 'r') as file:
#         account_list = csv.DictReader(file, delimiter=',')
#         for account in account_list:
#             Command.login(account['username'], account['pw'])
#             FileStore.read_queries(query_input_file, account['username'])
#             # break  # Stops the loop from processing every account; just for testing

class Email:

    @staticmethod
    def send_email(self, user, pwd, recipient, subject, body):
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

    @staticmethod
    def send_failed_test_email(self, user, pwd, recipient, subject, account, rule_name, record_count):
        body = "{account} has failed rule '{rule_name}' with a record count of '{record_count}'."
        send_email(user, pwd, recipient, subject, body)

class Command:
    """This class file serves as a force-cli wrapper library for Python. This will execute each Command using the
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
        return Command.execute("force login -u=%s -p=%s" % (username, password))


    def parse_query_result(query):
        regex = r"\s([0-9]\d*)"
        try:
            return re.findall(regex, query)[0]
        except Exception:
            return query


    def run_query(sql_statement, account):
        """Will execute a single SOQL statement."""
        python_output_query_file = FileStore('../outputs/python_output_query_file.csv', ["Account", "Rule_Name", "Record_Count"])
        query_result = Command.execute("force query " + sql_statement)
        dict_list = [{'Account': account, 'Rule_Name': sql_statement, 'Record_Count': Command.parse_query_result(query_result)}]
        python_output_query_file.write_csv(dict_list)
        return Command.execute("force query " + sql_statement)





class FileStore:


    def __init__(self, filename, fields):
        """This uses a passed in 'filename' argument to create a FileStore file with the same name."""
        self.filename = filename
        self.headers = fields
        if os.path.isfile(self.filename) == False:
            self.init_csv(fields)

    def get_file_location(self):
        return self.filename

    def init_csv(self, fields):
        print("Creating '%s', using %s as headers." % (self.filename, fields))
        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',', quoting=csv.QUOTE_ALL,
                                    lineterminator='\n')
            return writer.writeheader()


    def write(self, text):
        "Writes a single line to specified filename. Can refer to preexisting FileStore files."
        with open(self.filename, 'w', newline=' ') as csvfile:
            log_file = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            log_file.writerow(text)


    def write_csv(self, fields):
        """Will write to a csv file """
        print("def write_csv(%s)" % fields)
        with open(self.filename, 'a') as csvfile:
            fieldnames = self.headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
            return writer.writerow(fields)

    def read_queries(self, file_path, account):
        """Will execute n amount of SOQL statements based on parsed query file."""
        query_log = FileStore(file_path, ["query"])
        query_list = {}
        with open(query_log.filename, 'r') as file:
            query_list = csv.DictReader(file, delimiter=',')
            return [Command.run_query(query['query'], account) for query in query_list]


class TestRunner:

    def __init__(self, account_input_file, query_input_file):
        self.account_input_file = account_input_file
        self.query_input_file = query_input_file
        self.account_file = FileStore(account_input_file[0], account_input_file[1])
        self.query_file = FileStore(query_input_file[0], query_input_file[1])
        self.start_time = time.time()

    def execute_queries_on_accounts(self):
        with open(self.account_input_file, 'r') as accounts_file:
            account_list = csv.DictReader(accounts_file, delimiter=',')
            for account in account_list:
                Command.login(account['username'], account['pw'])
                FileStore.read_queries(self.query_input_file, account['username'])


def main():
    #print(run_tests("../outputs/accounts.csv", "../inputs/queries.csv"))
    account_file = "../outputs/accounts.csv", ["username", "pw"]
    query_file = "../inputs/queries.csv", ["query"]
    active_tests = TestRunner(account_file, query_file)
    print(active_tests.account_file.get_file_location())
    return active_tests.execute_queries_on_accounts

    # if user_input_is_valid(argv):
    #     start_time = time.time()
    #     print(True)
    #     #main()
        #print("--- %s seconds elapsed ---" % (time.time() - start_time))


    # send_email(read_credentials('gmail', 'username'), 'eumlwmfbrbnqveea','dstrasel@preventure.com','Test Email','Test Body')
    #send_failed_test_email()
    # Command.run_query("SELECT COUNT(SFDCID__C) Active FROM Contact", "test_account")
    # print(Command.parse_query_result(" Active -------- 20     (1 records)"))

    # If no args are specified, print "Nothing specified" and return pass
    # If args specified, pass them into "run_tests", arg[0] should be account path and arg[1] should be test path,
    # while arg[2] can flag whether emails should be sent. Default False, unless explicitly passed.

if __name__ == "__main__":
    main()