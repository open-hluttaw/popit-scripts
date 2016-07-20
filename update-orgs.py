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

            if org['popit_id']:
                popit_id = org['popit_id']
            else:
                popit_id = utils.org_name_to_popitid(org['name_en'],base_url)

            #Add new entries
            if not popit_id:
                print "Adding Organization: " + org['name_en']
                payload = {'name': org['name_en'] }
                r = requests.post('http://api.openhluttaw.org/en/organizations',
                              headers=headers, json=payload)
                r.content

            #Updates
            if popit_id:

                payload = {}

                #update fields
                print "Updating fields: \n"
                print org['name_en']

                if org['classification_en'] == 'Committee':

                    payload = { 'classification': org['classification_en'] }

                    print payload

                    url = base_url + '/en/organizations/' + popit_id
                    r = requests.put(url,headers=headers,json=payload)
                    print r.content

                    #translations
                    print "Updating translations for: " + org['name_en']
                    print org['name_mm'].decode('utf-8')
                    
                    payload = {'name': org['name_mm'],
                               'classification': org['classification_mm']}
                    
                    url = base_url + '/my/organizations/' + popit_id
                    r = requests.put(url,headers=headers,json=payload)
                    print r.content

update()
