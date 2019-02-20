import urllib
import pandas as pd
import re
import tempfile
from PyPDF2 import PdfFileReader
import sqlite3
from sqlite3 import Error
import argparse

col_names = ('Arrest_DateTime','Case_Number','Arrest_Location','Offense','Arrestee','Arrestee_Birthday','Arrestee_Address','Status','Officer')
def fetchincidents(fileurl):
    data = urllib.request.urlopen(fileurl)
    fp = tempfile.TemporaryFile()
    # Write the pdf data to a temp file
    fp.write(data.read())
    # Set the curser of the file back to the begining
    fp.seek(0)
    # Read the PDF
    pdfReader = PdfFileReader(fp)
    # Get the first page
    page1 = pdfReader.getPage(0).extractText()
    return page1

def extractincidents(page1):
    page1 = page1.split("\n")[13:]
    page1 = '\n'.join(page1)
    page1 = page1.replace(" \n"," ")
    page1 = page1.replace("-\n"," ")
    page1 = page1.split(";\n")[:-1]
    dl = []
    for i,val in enumerate(page1):
        # print(re.findall(re.escape(val),val))
        if(val.count("\n") == 11):
            val = val.split("\n")
            val[6:10] = [' '.join(val[6:10])]
            dl.append(val)
            # print(val)
        elif(val.count("\n") > 11):
            temp = val.split("\n")
            if(val.count("\n") == 12):
                temp[3:5] = [' '.join(temp[3:5])]
                temp[6:10] = [' '.join(temp[6:10])]
                dl.append(temp)
                # print(temp)
            else:
                print("greater than expected cols please check")
        else:
            # print("lets do somthing")
            temp = val.split("\n")
            for c in range(0,(11 - val.count("\n"))):
                temp.append('')
            if(val.count("\n") == 10):
                temp[10],temp[11] = temp[9],temp[10]
                temp[9] = ''
                
            if(val.count("\n") == 9):
                temp[10],temp[11] = temp[8],temp[9]
                temp[9] = ''
                temp[8] = ''
                
            if(val.count("\n") == 8):
                temp[10],temp[11] = temp[7],temp[8]
                temp[9] = ''
                temp[8] = ''
                temp[7] = ''
            temp[6:10] = [' '.join(temp[6:10])]
            dl.append(temp)
    # print(dl)
    df = pd.DataFrame(dl,columns=col_names)  
    # print(df.iloc[0:,6:12])
    # print(finalalldata.iloc[0:,0:])
    # print(finalalldata.iloc[0:,5:])
    #df.set_index('Arrest_DateTime', inplace=True)
    return df

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS arrests (
                                        Arrest_DateTime text,
                                        Case_Number text,
                                        Arrest_Location text,
                                        Offense text,
                                        Arrestee text,
                                        Arrestee_Birthday text,
                                        Arrestee_Address text,
                                        Status text,
                                        Officer text
                                    ); """
    try:
        c = conn.cursor()
        c.executescript('drop table if exists arrests;')
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_table(conn , dataToTable):  
    dataToTable.to_sql("arrests", conn, if_exists="replace",index=False)    
    conn.commit()

def get_Random_Value(conn):
    # write a code later
    randomstate = "SELECT * FROM arrests ORDER BY RANDOM() LIMIT 1"
    try:
        c = conn.cursor()
        c.execute(randomstate)
        r = c.fetchall()[0]
        # print(r)
        r = list(r)
        # print(r)
        r = 'þ'.join(r)
        return r
    except Error as e:
        return e
        print(e)

def main(url):
    page1data = fetchincidents(url)
    # print(page1data)
    dataToTable = extractincidents(page1data)
    database = "pythonsqlite.db"
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn)
        insert_table(conn , dataToTable)
        print(get_Random_Value(conn))
        # cur1 = conn.cursor()
        # cur1.execute("SELECT * FROM arrests")
        # rows = cur1.fetchall()
        # for row in rows:
        #     print(row)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrests", type=str, required=True, help="The arrest summary url.")
    args = parser.parse_args()
    if args.arrests:
        print(args.arrests)
        main(args.arrests)                         

