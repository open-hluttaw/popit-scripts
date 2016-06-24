#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import pandas

import utils

base_url = "http://api.openhluttaw.org"

#store key in token.txt Don't commit this file
key = open('token.txt')
token = 'Token '+key.read().rstrip()

headers = {'Authorization': token }


#can't have single function right now because columns are not the same for
#different languages

#Update English
def update_en():

    lang = 'en'

    df = pandas.DataFrame.from_csv('data/mp-en.csv', header=1, index_col=False)
    
    MPs = df.itertuples()

    for mp in MPs:
        hluttaw_id = mp[1]

        popit_id = utils.hluttaw_to_popitid(hluttaw_id, base_url)
        
        if popit_id:
            url = base_url + "/" + lang + "/persons/" + popit_id

            honorific_prefix = mp[3]
            name = mp[4]
            gender = mp[15]
            national_identity = mp[23]
            image = mp[36]

            payload = { 
                        'honorific_prefix': honorific_prefix,
                        'name': name,
                        'gender': gender,
                        'national_identity': national_identity,
                        'image': image,
                        }

            #r = requests.put(url, headers=headers, json=payload)
            #print r.content


#Update Myanmar translations
def update_my():

    lang = 'my'

    df = pandas.DataFrame.from_csv('data/mp-my.csv', header=1, index_col=False)
    
    MPs = df.itertuples()

    for mp in MPs:
        hluttaw_id = mp[1]

        popit_id = utils.hluttaw_to_popitid(hluttaw_id, base_url)
        
        if popit_id:
            url = base_url + "/" + lang + "/persons/" + popit_id

            honorific_prefix = mp[3] #empty
            name = mp[4]
            gender = mp[15]
            national_identity = mp[23]

            payload = { 
                        #'honorific_prefix': honorific_prefix,
                        'name': name,
                        'gender': gender,
                        'national_identity': national_identity,
                        }

            r = requests.put(url, headers=headers, json=payload)
            print r.content
#update_en()
update_my()
