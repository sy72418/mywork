# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:43:04 2022

@author: user
"""

import pymysql

dbsetting = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'123456789',
    'db':'mjwebhw',
    'charset':'utf8'
    }

conn = pymysql.connect(**dbsetting)