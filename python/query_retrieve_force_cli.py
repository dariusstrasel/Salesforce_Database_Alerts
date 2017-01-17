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
    8. Run test queries for the accounts imported from file.
    9. Save queries to output file
    ########### START EMAILING RESULTS ###############
    10. Send email for each failed row in results.

    Module Structure (12/31/2016):
        Classes:
            Utility (Static methods for rest fo module):
                -is_path()
                -return_now_as_datetime()
                -date_delta()
                -path_exist()
                -user_input_is_valid()
                -generate_rule_name()
            Email (Simple class to facilitate email):
                send_email()
                catch_failed_test() (OBSOLETE)
            SFDCSession (Represents session with Salesforce API):
                -__init__()
                -execute()
                -login()
                -parse_query_result()
                -run_query() (OBSOLETE)
                -output_query_results_to_file()
                -output_query_results_database()
            FileStore (Represents CSV filestores and logs; handles IO)
                -__init__(filename, headers)
                -get_file_location()
                -init_csv()
                -write_csv()
                -read_queries_from_file()
            TestRunner (Represents active test session; parent of all functionality.):
                -__init__(account_file, query_file, database_connection)
                -execute_queries_on_accounts()
                -catch_error() (OBSOLETE)
                -rule_set_is_valid()
                -query_rule_match()
                -query_passes_tests()
                -calculate_variance()
                -calculate_stdev()
            Database (Represents database IO, handles cursor sessions, and CRUD operations.):
                -__init__(name, location)
                -init_database()
                -open_cursor()
                -execute_cursor()
                -select_data() (OBSOLETE)
                -insert_query_result()
                -select_query_history()
                -insert_rule_set()
                -select_query_results() (OBSOLETE)
                -select_rule_sets()

Notes 1/4/17 Meeting:
        proportion: percentage of change
        difference: value of change

      Scalar, 0 Target Record Count
        SELECT COUNT(SFDCID__C) IsActive_Status_Not_Active FROM Contact where (mxw__Is_Active__c = true and Status__c != 'Active') OR (mxw__Is_Active__c = false and Status__c = 'Active')
      Vector, Daily, Threshold: 5%, Proportion
        SELECT COUNT(SFDCID__C) Active FROM Contact where mxw__Is_Active__c = true

'''

import os
import time
import csv
import subprocess
import sys
import re
import colorama
import sqlite3
import datetime
import dateutil.parser
import statistics


class Utility:

    @staticmethod
    def is_path(input_string):
        """Returns whether an input string has a pattern match in the regex expression. This particular pattern looks
        to see if a string matches a typical file-system path."""
        regex = r"(.+)/([^/]+)$"
        if len(re.findall(regex, input_string)) == 0:
            return False
        return True

    @staticmethod
    def return_now_as_datetime():
        """Returns a SQLITE compatible datetime object for the present time at invocation."""
        return datetime.datetime.today().strftime('%Y-%m-%d %I:%M:%S')

    @staticmethod
    def date_delta(datetime_string, duration_string):
        duration_mapping = {'daily': "1", 'weekly': '7', 'monthly': '30'}
        datetime_string_as_object = dateutil.parser.parse(datetime_string)

        delta_date = datetime_string_as_object - datetime.timedelta(days=int(duration_mapping[duration_string]))
        return delta_date

    @staticmethod
    def path_exist(file_path):
        """Returns whether a filepath on the local filesystem actually exists. Can accept a file in addition to path."""
        return os.path.exists(file_path)

    @staticmethod
    def user_input_is_valid(arg_cls):
        if len(arg_cls) < 3:
            print("Not enough parameters passed. Need %s more" % (3 - len(sys.argv)))
            return False
        print([Utility.path_exist(argument) for argument in sys.argv[1:]])

        print("'%s' and '%s' are not files/do not exist." % (arg_cls[1], arg_cls[2]))
        return False

    @staticmethod
    def generate_rule_name(string_input):
        result = ""
        for item in string_input.split(" "):
            formatted_item = item[0].upper()
            if item[0] == "(":
                result += formatted_item + ")"
            if item[0] == ")":
                result += formatted_item + "("
            else:
                result += formatted_item
        return result


class Email:

    @staticmethod
    def send_email(self, user, pwd, recipient, subject, body):
        # Sends an email using passed in arguments, catches errors in try/except
        print("send_email(%s, %s, %s, %,s %s)" % (user, pwd, recipient, subject, body))
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
    def catch_failed_test(record_count, account, rule_name):
        print("def catch_failed_test(%s, %s, %s)" % (record_count, account, rule_name))
        # user = ""
        # pwd = ""
        # recipient = account
        # subject = ""
        body = "%s has failed rule '%s' with a record count of '%s'." % (account, rule_name, record_count)

        if int(record_count) == 0:
            print()
            print('\033[31m' + body)
            print(colorama.Style.RESET_ALL)
            # Email.send_email(user, pwd, recipient, subject, body)


class SFDCSession:
    """This class file serves as a force-cli wrapper library for Python. This will execute each SFDCSession using the
    subprocess Python module."""
    def __init__(self):
        pass

    @staticmethod
    def execute(command):
        """This method will execute the string statement passed in."""
        print("execute(%s)" % command)
        output = None
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output.decode()

    @staticmethod
    def login(username, password):
        """Used to pass a login to force-cli using username, password arguments."""
        return SFDCSession.execute("force login -u=%s -p=%s" % (username, password))

    @staticmethod
    def parse_query_result(query):
        regex = r"\s([0-9]\d*)"
        try:
            return re.findall(regex, query)[0]
        except Exception:
            return query

    @staticmethod
    def run_query(sql_statement, account):
        """Will execute a single SOQL statement."""
        query_date = datetime.datetime.today().strftime('%Y-%m-%d %I:%M:%S')
        query_result = SFDCSession.execute("force query " + sql_statement)
        query_result_as_str = str(query_result)
        query_result_parsed = SFDCSession.parse_query_result(query_result_as_str)
        rule_name = Utility.generate_rule_name(sql_statement)
        # Doesn't reflect new database method
        # Email.catch_failed_test(query_result_parsed, account, rule_name)
        dict_list = {'Account': account, 'Rule_Name': rule_name, 'Record_Count': query_result_parsed}
        query_data = [(sql_statement, str(query_date), query_result_parsed, account)]
        SFDCSession.output_query_results_database(query_data)
        SFDCSession.output_query_results_to_file(dict_list)

    @staticmethod
    def output_query_results_to_file(input):
        output_location = '../outputs/python_output_query_file.csv'
        output_headers = ["Account", "Rule_Name", "Record_Count"]
        python_output_query_file = FileStore(output_location, output_headers)
        return python_output_query_file.write_csv(input)

    @staticmethod
    def output_query_results_database(input):
        database_connection = Database("queries_database", "../db/")
        return database_connection.insert_query_result(input)


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

    def write_csv(self, fields):
        """Will write to a csv file """
        print("def write_csv(%s)" % fields)
        with open(self.filename, 'a') as csvfile:
            fieldnames = self.headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL,
                                    lineterminator='\n')
            return writer.writerow(fields)

    def read_queries_from_file(self, account) -> list:
        """Will execute n amount of SOQL statements based on parsed query file."""
        with open(self.filename, 'r') as file:
            query_list = csv.DictReader(file, delimiter=',')
            return [SFDCSession.run_query(query['query'], account) for query in query_list]

    def read_rulesets_from_file(self) -> list:
        """Loads the lines from rule_set.csv into an associated database."""
        """
            What does this function do?
            This will take the rule_sets.csv file and load it into the rule_set table of the database. What are the steps
            involved?
            1. Open .csv
            2. Read each line into a dictionary, reading header:value pairs
            3. Insert each line into the database table for rule_sets
        """
        with open(self.filename, 'r') as file:
            rule_list = csv.DictReader(file, delimiter=',')
            return [rule for rule in rule_list]

class TestRunner:

    def __init__(self, account_input_file, query_input_file, database_name, database_location):
        self.rule_set_file = FileStore(account_input_file[0], account_input_file[1])
        self.account_file = FileStore(account_input_file[0], account_input_file[1])
        self.query_file = FileStore(query_input_file[0], query_input_file[1])
        self.database_connection = Database(database_name, database_location)
        self.start_time = time.time()

    def execute_queries_on_accounts(self):
        with open(self.account_file.get_file_location(), 'r') as file_lock:
            account_list = csv.DictReader(file_lock, delimiter=',')
            for account in account_list:
                SFDCSession.login(account['username'], account['pw'])
                self.query_file.read_queries_from_file(account['username'])

    def catch_error(self):
        """Directs query results to rule processor."""
        pass

    @staticmethod
    def execute_rule_suite(query):
        # Select all rule_sets
        # Execute test_session.query_passes_tests(query, rule_set)
        # If any rules fail, send an email.
        pass

    @staticmethod
    def rule_set_is_valid(rule_set):
        """Returns whether a rule_set has a legal schema. True/False"""
        # TODO: Add rule to ensure query has a record count?
        rule_definitions = {
            'valid_types': ['scalar', 'vector']
            ,'valid_data_structure_length': '6'
            ,'sql_statement_is_required': 'True'
            ,'valid_duration': ['daily', 'weekly', 'monthly']
        }
        total_rules = len(rule_definitions)
        rules_passed = 0
        if rule_set['rule_set_type'] in rule_definitions['valid_types']:
            rules_passed += 1
        else:
            print("%s not in %s" % (rule_set['rule_set_type'], rule_definitions['valid_types']))
        if len(rule_set) == int(rule_definitions['valid_data_structure_length']):
            rules_passed += 1
        else:
            print("rule_set did not have legal parameter count.")
        if rule_set['sql_statement'] is not None or rule_set['sql_statement'] is not "":
            rules_passed += 1
        else:
            print("rule_set_type is null or empty")
        if rule_set['duration'] in rule_definitions['valid_duration']:
            rules_passed += 1
        else:
            print("Duration value is not legal.")
        if total_rules == rules_passed:
            return True
        print("Rule Set is not valid. Passed %s of %s tests." % (rules_passed, total_rules))
        return False

    @staticmethod
    def query_rule_match(query, rule_set) -> bool:
        """Returns true or false if a rule applies to a query result. """
        if TestRunner.rule_set_is_valid(rule_set):
            if rule_set['sql_statement'] == query['sql_statement'] and rule_set['account'] == query['account']:
                return True
            if rule_set['sql_statement'] == query['sql_statement']:
                return True
            print("SQL Statements do not match.")
            return False
        print("Rule is not legal.")
        return False

    def query_passes_tests(self, query, rule_set) -> bool:
        """This will compare each query result to rule_sets."""
        print("query: " + str(query))
        print("rule_set: " + str(rule_set))
        if TestRunner.query_rule_match(query, rule_set):
            if rule_set['rule_set_type'] == 'scalar':
                if rule_set['target_record_count'] == query['record_count']:
                    print("Is Scalar Rule")
                    return True
                print("Target record count does not match.")
                return False
            elif rule_set['rule_set_type'] == 'vector':
                if rule_set['sql_statement'] == query['sql_statement']:
                    query_history_results = self.database_connection.select_query_history(query['sql_statement'], query['execution_date'], query['record_count'], query['account'], rule_set['duration'])
                    print(query_history_results)
                    query_history = [item[2] for item in query_history_results]
                    print(query_history)
                    query_history_stdev = self.calculate_proportion(query_history)
                    print(query_history_stdev)
                    if query_history_stdev <= int(rule_set['threshold']):
                        return True
                    return False
                print("Ruleset does not match query")
        print("No matching rule found for query.")
        return False

    @staticmethod
    def type_is_int(data) -> bool:
        try:
            [int(data) for data in data]
            return True
        except TypeError:
            return False

    @staticmethod
    def calculate_proportion(data1, data2) -> int:
        """Returns the variance of a population as input."""
        if TestRunner.type_is_int([data1, data2]):
            proportion = 100 * (data2 - data1) / data1
            return proportion
    # 1 2
    # 1/100 = 2/
    @staticmethod
    def calculate_difference(data1, data2) -> int:
        """Returns the variance of a population as input."""
        if TestRunner.type_is_int([data1, data2]):
            difference = data1 - data2
            return difference

    @staticmethod
    def calculate_variance(data):
        """Returns the variance of a population as input."""
        if TestRunner.type_is_int(data):
            return statistics.variance(data)

    @staticmethod
    def calculate_stdev(data):
        """Returns the variance of a population as input."""
        if TestRunner.type_is_int(data):
            return statistics.stdev(data)


class Database:
    # TODO: Ensure data processing is ensuring NONE is passed as NULL into database and not empty string

    def __init__(self, name, location):
        self.location = location
        self.filename = name + '.db'
        self.database_path = self.location + self.filename
        if os.path.isfile(self.database_path) == False:
            print("Database '%s' does not exist. Creating at: '%s'" % (self.filename, self.database_path))
            self.database_connection = sqlite3.connect(self.database_path)
            self.init_database()
        else:
            self.database_connection = sqlite3.connect(self.database_path)

    def init_database(self):
        print("Initialising database with default schema.")
        query_table_sql_statement = """CREATE TABLE queries (query_id INTEGER PRIMARY KEY,sql_statement TEXT, datetime TEXT, record_count INTEGER, account TEXT)"""
        self.execute_cursor(query_table_sql_statement)
        rule_set_table_sql_statement = """CREATE TABLE rule_sets (rule_set_id INTEGER PRIMARY KEY, rule_type TEXT, sql_statement TEXT, target_record_count INTEGER, duration TEXT, variance REAL, math_type TEXT, account TEXT, UNIQUE (rule_type, sql_statement, target_record_count, duration, variance, math_type, account) ON CONFLICT IGNORE)"""
        self.execute_cursor(rule_set_table_sql_statement)

    def open_cursor(self, sql_statement):
        """Fetches all the results from input SQL statement, without committing."""
        cursor = self.database_connection.cursor()
        cursor.execute(sql_statement)
        return cursor.fetchall()

    def execute_cursor(self, sql_statement):
        cursor = self.database_connection.cursor()
        try:
            cursor.execute(sql_statement)
            return self.database_connection.commit()
        except Exception:
            self.database_connection.rollback()
            e = sys.exc_info()[0]
            print("--------------------------------")
            print("\nException found; rolling back commit.")
            print("SQL Statement: '%s'" % (sql_statement))
            print("\nException: " + str(sys.exc_info()))
            print("--------------------------------")
            raise Exception
            #return self.database_connection.close()

    def insert_query_result(self, sql_statement, execution_date, record_count, account):
        """Executes a cursor commit to the query database by inserting a single record based on input parameters."""
        # OperationalError = Insert doesn't match table schema
        # OperationalError = Database may be locked
        # query_data = [("SELECT * FROM FAKETABLE", "12-27-2016", "0", "Test Account")]
        query_data = [(sql_statement, execution_date, record_count, account)]
        for record in query_data:
            format_str = """INSERT INTO 'queries' (sql_statement, datetime, record_count, account) VALUES ("{sql_statement}", "{datetime}", "{record_count}", "{account}");"""
            sql_command = format_str.format(sql_statement=record[0], datetime=record[1], record_count=record[2],account=record[3])

            try:
                self.execute_cursor(sql_command)
                print("Executing: %s" % (sql_command))
            except sqlite3.OperationalError:
                self.database_connection.rollback()
                print("Database is locked or insert does not match table schema.")
                exit()

    def insert_rule_set(self, rule_type, sql_statement, target_record_count, duration, variance, math_type):
        # OperationalError = Insert doesn't match table schema
        # OperationalError = Database may be locked
        # query_data = [("SELECT * FROM FAKETABLE", "12-27-2016", "0", "Test Account")]
        rule_data = [(rule_type, sql_statement, target_record_count, duration, variance, math_type)]
        for record in rule_data:
            format_str = """INSERT INTO rule_sets (rule_type, sql_statement, target_record_count, duration, variance, math_type)
                    VALUES ("{rule_type}", "{sql_statement}", "{target_record_count}", "{duration}", "{variance}", "{math_type}");"""

            sql_command = format_str.format(rule_type=record[0].lower(), sql_statement=record[1], target_record_count=record[2],
                                            duration=record[3].lower(), variance=record[4], math_type=record[5].lower())
            try:
                self.execute_cursor(sql_command)
                print("Executing: %s" % (sql_command))
            except sqlite3.OperationalError:
                self.database_connection.rollback()
                print("Database is locked or insert does not match table schema.")
                exit()

    def upsert_rulesets_to_database(self, file_store):
        print([item for item in file_store.read_rulesets_from_file()])
        return [self.insert_rule_set(item["rule_type"], item["sql_statement"], item["target_record_count"], item["duration"], item["variance"], item["math_type"]) for item in file_store.read_rulesets_from_file()]

    def select_query_history(self, sql_statement, execution_date, record_count, account, rule_set_duration):
        """Selects all query history where a specified (input) duration is removed from an input datetime."""
        # query_data = [("SELECT * FROM FAKETABLE", "12-27-2016", "0", "Test Account")]
        duration_mapping = {'daily':"1", 'weekly':'7', 'monthly':'30'}
        start_date = Utility.date_delta(execution_date, rule_set_duration)
        query_data = [(sql_statement, execution_date, record_count, account)]
        for record in query_data:
            format_str = """SELECT sql_statement, datetime, record_count, account FROM 'queries' WHERE datetime
                            BETWEEN "{start_date}" AND "{datetime}" """
            sql_command = format_str.format(start_date=start_date, datetime=record[1], record_count=record[2],
                                            account=record[3])
            try:
                print("Executing: %s" % (sql_command))
                return self.open_cursor(sql_command)

            except sqlite3.OperationalError:
                self.database_connection.rollback()
                print("Database is locked or insert does not match table schema.")

    def select_rule_sets(self, table, fields):
        table = "rule_sets"
        fields = ["type", "sql_statement", "target_record_count", "duration", "threshold_of_variance"]
        return self.select_data(table, fields)
        pass

def main():
    if True: #Eventually will check for user input.
        start_time = time.time()
        account_file_config = ("../outputs/accounts.csv", ["username", "pw"])
        query_file_config = ("../inputs/queries.csv", ["query"])
        rule_set_config = ("../inputs/rule_sets.csv", ["rule_type", "sql_statement", "target_record_count", "duration", "variance", "math_type"])
        rule_set_object = FileStore(rule_set_config[0], rule_set_config[1])

        database_store = ("queries_database", "../db/")

        query_dummy_data = {'sql_statement': "SELECT * FROM CONTACTS", 'record_count': "0", 'execution_date':'2016-12-29 00:00:00',
                 'account': 'Test Account'}
        rule_set_dummy_data = {'rule_set_type':'vector', 'sql_statement': "SELECT * FROM CONTACTS", 'target_record_count':"0",
                    'duration':'weekly', "threshold":"0", 'account':''}
        #test_session.query_rule_match(query, rule_set)

        test_session = TestRunner(account_file_config, query_file_config, database_store[0], database_store[1])

        #print(rule_set_object.read_rulesets_from_file())
        test_session.database_connection.upsert_rulesets_to_database(rule_set_object)
        #print(TestRunner.calculate_proportion(1000, 1050))
        # print(active_tests.execute_queries_on_accounts())
        # print(test_session.query_passes_tests(query_dummy_data, rule_set_dummy_data))
        #print(queries_database.select_query_history("SELECT * FROM CONTACTS", "2016-12-28 23:50:04", "1000",
        # "Test Account", "weekly"))
        print("--- %s seconds elapsed ---" % (time.time() - start_time))
    exit()

if __name__ == "__main__":
    main()
