import os
import sqlite3 as sl
import pandas as pd


def initialize():
    con = sl.connect('stock_name.db')
    c = con.cursor()
    data_file = pd.read_csv('dataset.csv')
    data_file.to_sql('data', con, if_exists='replace', index=False)


def search(name):
    con = sl.connect('stock_name.db')
    c = con.cursor()
    dict = {}
    name = "'%" + str(name) + "%'"
    for name, ticker in c.execute('SELECT Name, Ticker FROM data where Name like' + name):
        if name in dict.keys():
            dict[name + "*"] = ticker
        else:
            dict[name] = ticker

    con.close()
    if len(dict) == 0:
        return None
    else:
        return dict






