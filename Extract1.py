#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 12:48:08 2020

@author: kris
"""

import csv,os
import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd
from Plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016


def met_data(month, year):
    
    file = open('Data/Html_Data/%i/%i.html' % (year, month), 'rb')
    plain_text = file.read()

    oneD = []
    twoD = []

    soup = BeautifulSoup(plain_text, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                oneD.append(a)

    rows = len(oneD) / 15

    for times in range(rows):
        newoneD = []
        for i in range(15):
            newoneD.append(oneD[0])
            oneD.pop(0)
        twoD.append(newoneD)

    length = len(twoD)

    twoD.pop(length - 1)
    twoD.pop(0)

    for a in range(len(twoD)):
        twoD[a].pop(6)
        twoD[a].pop(13)
        twoD[a].pop(12)
        twoD[a].pop(11)
        twoD[a].pop(10)
        twoD[a].pop(9)
        twoD[a].pop(0)

    return twoD


def data_combine(year, cs):
    for a in pd.read_csv('Data/Real_Data/met_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
    if not os.path.exists("Data/Real_Data"):
        os.makedirs("Data/Real_Data")
    for year in range(2013, 2017):
        final = []
        with open('Data/Real_Data/met_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):
            if year == 2016:
                if month < 5:
                    a = met_data(month, year)
                    final = final + a
                else:
                    break
            else:
                a = met_data(month, year)
                final = final + a

        pm = getattr(sys.modules[__name__], 'data_%s' % year)()

        if len(pm) == 364:
            pm.insert(364, '-')

        for i in range(len(final)):
            # final[i].insert(0, i + 1)
            final[i].insert(8, pm[i])

        with open('Data/Real_Data/met_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final:
                flag = 0
                for elem in row:
                    if elem == 0 or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)

    a = data_combine(2013, 600)
    b = data_combine(2014, 600)
    c = data_combine(2015, 600)
    d = data_combine(2016, 600)

    total = a + b + c + d

    with open('Data/Real_Data/Original_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)