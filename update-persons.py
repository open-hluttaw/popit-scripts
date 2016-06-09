#!/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import pandas

base_url = "http://api.openhluttaw.org"
lang = "mn"

#store key in token.txt Don't commit this file
key = open('token.txt')
token = 'Token '+key.read().rstrip()

headers = {'Authorization': token }

def hluttaw_to_popitid(identifier_hluttaw,base_url):
    # Get PopitID matching identifier_hluttaw column id for
    # representatives

    #using en due to bug https://github.com/Sinar/popit_ng/issues/171
    search_url = base_url + '/' + 'en' + '/search/persons?q="' + identifier_hluttaw +'"'
    search_req = requests.get(search_url)
    
    if search_req.json()['results']:
        return search_req.json()['results'][0]['id']
    else:
        return False


#Update Multilingual Name

df = pandas.DataFrame.from_csv('mp-mm.csv', header=1, index_col=False)

MPs = df.itertuples()

for mp in MPs:
    hluttaw_id = mp[1]

    popit_id = hluttaw_to_popitid(hluttaw_id, base_url)
    
    if popit_id:
        url = base_url + "/" + lang + "/persons/" + popit_id

        name = mp[4]
        gender = mp[15]

        payload = { 'name': name,
                    'gender': gender }

        r = requests.put(url, headers=headers, json=payload)
        print r.content
