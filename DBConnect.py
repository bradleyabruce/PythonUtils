import pyodbc
import pandas as pd
import Password
import requests
import urllib3

# ---------------------- Database Call ----------------------------------

try:
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=174.101.154.93;'
                      'Database=PasswordManager;'
                      'uid=bruceba;'
                      'pwd=password')

    # Store return value of a database query in a Panda Data Frame
    value = pd.read_sql_query('select * from tEntries', conn)
    print(value.count())

    # Foreach row value, create a Password Class and store it in a list of Password Classes
    DatabasePasswords = [
        (Password.Password(row.EntryID, row.UserID, row.WebsiteDomainID, row.WebsitePasswordID, row.CategoryID))
        for index, row in value.iterrows()]

    # Foreach Password Class in list of Passwords, print out the EntryID an int
    for x in DatabasePasswords:
        print(int(x.EntryID))

    # print out the length of the array not the count in this instance
    print('Count of Database Passwords: ' + str(len(DatabasePasswords)))

except Exception:
    print('Database Error!!!')

# ------------------------ API Post Call ---------------------------------------

# Suppress unverified https request from self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = 'https://174.101.154.93:1337/api/entryRetrieval'
PARAMS = {'userid': '9', 'categoryid': '0'}

try:
    r = requests.post(url=URL, data=PARAMS, verify=False)
    data = r.json()

    APIPasswords = []

    for i in range(len(data)):
        entryid = data[i]['EntryID']
        userid = '9'
        websitedomainid = data[i]['WebsiteDomain']
        websitepasswordid = data[i]['WebsitePassword']
        categoryid = data[i]['CategoryID']
        password = Password.Password(entryid, userid, websitedomainid, websitepasswordid, categoryid)
        APIPasswords.append(password)

    print('Count of API Passwords: ' + str(len(APIPasswords)))

except Exception:
    print('API Error!!!')

