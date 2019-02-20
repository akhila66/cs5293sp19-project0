Tried almost all the pdf extraction techniquies 

- pdftotest
- tika
- camelot-py
- tabula-py
- ghostscript

and few others which will help to fetch the table data from pdfs 

But tall these work work with the pdf that we are going to work because the 
data not structured and may actuall table row has inline rows which making this difficult

So pypdf2 which suggested my Dr grant works as it extracts the text words from the pdf. but in semi structured and with few hidden clues to make it structured

├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── docs
├── example.pdf
├── project0
│   ├── __init__.py
│   └── main.py
├── pythonsqlite.db
├── setup.cfg
├── setup.py
├── temp
└── tests
    ├── example.pdf
    ├── test_deeptest.py
    └── test_fetchpdf.py

Step 1 : Extracted the test from the given url by pypdf2
Step 2 : to clean the data I applied few assumptions and data stratagies and make it structured with rows and cols 
         splited given str data from pdpdf2 with ";" which helps to get data by row wise 
         before that I removed the header and then after splited the data removed the last row which actually has the headers of pdf
         now we get actual data in rows,
         to split these rows into cols used " \n" "\n" "-\n" after going through how data works in this pdf 
         it uses (space and \n) and ( - and \n )if it has continues values in next line
         after alignment of row data splitted with \n where we given final cols 
         to make addres combinded used assumptions that - the data is only missing for city zicode and state - only combined the address , city , zipcode and state with out bothering about the missing data. used the col index for combinding
step 3 : the list of list cleaned and structured data converted to dataframe using pandas
step 4 : created sqlite connection
step 5 : created table in it with 9 cols as mention in the docs
        CREATE TABLE arrests (
    arrest_time TEXT,
    case_number TEXT,
    arrest_location TEXT,
    offense TEXT,
    arrestee_name TEXT,
    arrestee_birthday TEXT,
    arrestee_address TEXT,
    status TEXT,
    officer TEXT
);
step 6 : inserted the dataframe into sqlite by excluding the index 

step 7 : returned the random row from sqllite table

Assumptions:
value data in more lines with is taken " \n" and "-\n"
assuming that data for offense will has 3 rows data - after doing " \n" we still left with 1 more for which there is no space. manually doing this considering the col index
assuming the headers are 1st 13 rows and removing it
assuming that last row data from spliting with ";" as header of pdf and removing it 

Disadvantage of ReGx:
Tried but we always cannot predict data in which format it will come. cannot get the cleaned data from regx for which the data is not in purticular format 

Test files:
    test_fetchpdf.py:
    this is genralised tests for all the pdf - fetching all the arrests url from main url and testing one random pdfurl
    checking for data fecthing , database connection , data into table , and length of rows and cols , if returing random values or not 
    test_deeptest.py:
    testing on seleted downloaded file example.pdf 
    checking if the data is fetched exactly as in the pdf by some selected values
    and count of rows and cols as well.



