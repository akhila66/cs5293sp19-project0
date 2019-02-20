import pytest
import project0
from project0 import main
import urllib
import pandas as pd
import re
import random
url = "http://normanpd.normanok.gov/content/daily-activity"
# data = urllib.request.urlopen(url).read() # normal method
# print (data['Name'])
tables =pd.read_html(url) # Returns list of all tables on page
ReqDataFrame = tables[0] # Select table of interest
FileNameList = ReqDataFrame['Name']
regex = re.compile(r'.*Arrest.*')
selected_files = list(filter(regex.search, FileNameList))
secure_random = random.SystemRandom()
linkname = secure_random.choice(selected_files)
fileurl = "http://normanpd.normanok.gov/filebrowser_download/657/"+linkname+".pdf"
fileurl = fileurl.replace(" ", "%20")
#print(fileurl)
database = "pythonsqlite.db"
def test_fetchincidents():
    assert main.fetchincidents(fileurl) is not None
def test_extractincidents():
    page1data = main.fetchincidents(fileurl)
    assert main.extractincidents(page1data) is not None
def test_create_connection():
    print("test_create_connection")
    con = main.create_connection(database)
    assert con is not None
def test_create_table():
    print("test_create_table")
    con = main.create_connection(database)
    main.create_table(con)
    # created table called arrests
    command = "SELECT name FROM sqlite_master WHERE type='table' AND name='arrests';"
    cur = con.cursor()
    assert cur.execute(command).fetchall()[0][0] == 'arrests'
def test_insert_table():
    print("test_insert_table")
    page1data = main.fetchincidents(fileurl)
    dfdata = main.extractincidents(page1data)
    con = main.create_connection(database)
    main.create_table(con)
    main.insert_table(con , dfdata)
    com_len_rows = "SELECT COUNT(*) FROM arrests"
    cur = con.cursor()
    assert cur.execute(com_len_rows).fetchall()[0][0] >= 1
    com = "PRAGMA table_info(arrests);"
    c = con.cursor()
    assert len(c.execute(com).fetchall()) == 9
def test_get_Random_Value():
    print("test get_Random_Value")
    conn = main.create_connection(database)
    assert type(main.get_Random_Value(conn)) == str
    assert len(main.get_Random_Value(conn)) >= 1
