#!/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import pandas
import utils

base_url = "http://api.openhluttaw.org"
lang = "en"

#store key in token.txt Don't commit this file
key = open('token.txt')
token = 'Token '+key.read().rstrip()

headers = {'Authorization': token }

#Add Parliamentary Membership

df = pandas.DataFrame.from_csv('data/mp-en.csv', header=1, index_col=False)

MPs = df.itertuples()

for mp in MPs:
   
    if isinstance(mp[4], basestring):
        payload = {} 
        
        hluttaw_id = mp[1]
        person_id = utils.hluttaw_to_popitid(hluttaw_id, base_url)
        
        payload['role'] = 'MP'
        payload['person_id'] = person_id
        post_label = mp[7]
       
        if post_label == 'Bago':
            post = utils.post('414db6b73e8c40f7836d346c829c9f10',base_url)
        elif post_label == 'Magway':
            post = utils.post('bca454c041e9469aab2d91bd7dc7fb93',base_url)
        else:
            post = utils.search_post(post_label, base_url)
        
        post_id = post['id']
        organization_id = post['organization_id']

        payload['organization'] = organization_id

        party = mp[5]
        party_id = utils.org_name_to_popitid(party,base_url)
        
        payload['on_behalf_of_id'] = party_id
        payload['on_behalf_of'] = party
        
        start_date = mp[11]
        payload['start_date'] = start_date

        print mp[1]
        print payload

        #r = requests.put(url, headers=headers, json=payload)
        #print r.content


