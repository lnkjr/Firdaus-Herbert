import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def fetch():

    """Downloads the skill_test_data file """

    options = Options()
    options.add_experimental_option('prefs', {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })

    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)

    driver.get('https://jobs.homesteadstudio.co/data-engineer/assessment/download/')
    time.sleep(3)
    dl_button = driver.find_element(By.CLASS_NAME, "wp-block-button__link.wp-element-button")
    dl_button.click()
    time.sleep(3)
    driver.close()
  


def pivot_table():

    """Transforms the data and returns a Data Frame"""

    excel_file = pd.read_excel('skill_test_data.xlsx',sheet_name='data')

    excel_file.to_csv('skill_test.csv',header = True, index = None)

    df = pd.DataFrame(pd.read_csv('skill_test.csv'))

    pd.options.display.float_format = '{:,.2f}'.format


    table = pd.pivot_table(df,values=['Spend','Attributed Rev (1d)','Imprs','Visits','New Visits','Transactions (1d)','Email Signups (1d)'],index='Platform (Northbeam)',aggfunc='sum')

    table = table.rename(columns = {'Spend':'Sum of Spend','Attributed Rev (1d)':'Sum of Attributed Rev (1d)','Imprs':'Sum of Imprs','Visits':'Sum of Visits','New Visits':'Sum of New Visits','Transactions (1d)':'Sum of Transaction (1d)','Email Signups (1d)':'Sum of Email Signups (1d)'}).sort_values('Sum of Attributed Rev (1d)',ascending=False)

    table = table[['Sum of Spend','Sum of Attributed Rev (1d)','Sum of Imprs','Sum of Visits','Sum of New Visits','Sum of Transaction (1d)','Sum of Email Signups (1d)']]

    table = pd.concat([table,pd.DataFrame(table.sum(axis=0),columns = ['Grand Total']).T])

    table = table.reset_index()

    table = table.rename(columns={'index': 'Row Labels'})

    return table



def query(table):

    """Establishes the connection with sqlite"""

    con = sqlite3.connect('mydatabase.db')

    table.to_sql('mytable', con, if_exists='replace', index=False)

    #Displays the content of the table
    query = "SELECT * FROM mytable"
    result = pd.read_sql(query, con)

    print(result)

    con.close()


def main():
    fetch()
    table = pivot_table()
    query(table)


if __name__ =='__main__':
    main()
