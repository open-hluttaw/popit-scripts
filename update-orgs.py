#!/bin/python
# -*- coding: utf-8 -*-
import requests
import pandas

import utils

base_url = "http://api.openhluttaw.org"
lang = "my"

#store key in token.txt Don't commit this file
key = open('token.txt')
token = 'Token '+key.read().rstrip()

headers = {'Authorization': token }


#Update Multilingual Name

def update():

    df = pandas.DataFrame.from_csv('data/organizations.csv', header=0, index_col=False)
    df = df.where((pandas.notnull(df)), None)

    orgs = df.to_dict(orient='records')

    for org in orgs:
        
        if org['name_en']:
            
            popit_id = utils.org_name_to_popitid(org['name_en'],base_url)

            if not popit_id:
                print "Adding Organization: " + org['name_en']
                payload = {'name': org['name_en'] }
                r = requests.post('http://api.openhluttaw.org/en/organizations',
                              headers=headers, json=payload)
                r.content

            if popit_id:
                print "Updating translations for: " + org['name_en']
                payload = {'name': org['name_mm'] }
                print org['name_mm'].decode('utf-8')


update()
