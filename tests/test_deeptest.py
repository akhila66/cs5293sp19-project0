# importing required modules 
import PyPDF2 
import project0
import pytest
from project0 import main
#from urllib.request import urlretrieve

#urlretrieve('http://normanpd.normanok.gov/filebrowser_download/657/2019-02-15%20Daily%20Arrest%20Summary.pdf','example.pdf')
# creating a pdf file object 
pdfFileObj = open('example.pdf', 'rb') 
  
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
print(pdfReader.numPages) 
  
# creating a page object 
pageObj = pdfReader.getPage(0) 
  
# extracting text from page 
page1data =(pageObj.extractText()) 
  
# closing the pdf file object 
pdfFileObj.close()
database = "pythonsqlite.db"
def test_extractincidents():
    df = main.extractincidents(page1data)
    assert df is not None
    assert df.iloc[1][3] == "DRIVING WITH LIC. CANCELED/SUSPENDED/REVOKE D - DUS"
    assert df.shape == (10,9) # rows and cols
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
    dfdata = main.extractincidents(page1data)
    con = main.create_connection(database)
    main.create_table(con)
    main.insert_table(con , dfdata)
    com_len_rows = "SELECT COUNT(*) FROM arrests"
    cur = con.cursor()
    assert cur.execute(com_len_rows).fetchall()[0][0] == 10
    com = "PRAGMA table_info(arrests);"
    c = con.cursor()
    assert len(c.execute(com).fetchall()) == 9
def test_get_Random_Value():
    print("test get_Random_Value")
    conn = main.create_connection(database)
    assert type(main.get_Random_Value(conn)) == str
    assert len(main.get_Random_Value(conn)) >= 1

