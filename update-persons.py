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

    df = pandas.DataFrame.from_csv('data/mp-en.csv', header=0, index_col=False)
    df = df.where((pandas.notnull(df)), None)

    MPs = df.to_dict(orient='records')

    for mp in MPs:
        hluttaw_id = mp['identifier__hluttaw']

        if mp['popit_id']:
            popit_id = mp['popit_id']

        else:
            popit_id = utils.hluttaw_to_popitid(hluttaw_id, base_url)
   
        if popit_id:

            url = base_url + "/" + lang + "/persons/" + popit_id

            honorific_prefix = mp['honorific_prefix']
            name = mp['name']
            gender = mp['gender']
            national_identity = mp['national_identity']
            image = mp['image']

            if type(image) == float:
                print "nan"

            payload = { 
                        'honorific_prefix': honorific_prefix,
                        'name': name,
                        'gender': gender,
                        'national_identity': national_identity,
                        'image' : image
                        }

            r = requests.put(url, headers=headers, json=payload)
            print r.content

#Update Myanmar translations
def update_my():

    lang = 'my'

    df = pandas.DataFrame.from_csv('data/mp-my.csv', header=1, index_col=False)
    df = df.where((pandas.notnull(df)), None)

    MPs = df.to_dict(orient='records')

    for mp in MPs:
        hluttaw_id = mp['identifier_hluttaw']

        popit_id = utils.hluttaw_to_popitid(hluttaw_id, base_url)
        
        if popit_id:
            url = base_url + "/" + lang + "/persons/" + popit_id

            honorific_prefix = mp['honorific_prefix']
	    #not used
            name = mp['name']
            gender = mp['gender']
            national_identity = mp['national_identity']

            payload = { 
                        #'honorific_prefix': honorific_prefix,
                        'name': name,
                        'gender': gender,
                        'national_identity': national_identity,
                        }

            #r = requests.put(url, headers=headers, json=payload)
            #print r.content

def clean_duplicate_sms():
    #Getting total number of pages via REST request
    page_request = requests.get('http://api.openhluttaw.org/en/persons')
    pages = page_request.json()['num_pages']

    #Fetch and build list of all representatives
    persons =[]
    for page in range(1,pages+1):
	req_representatives = requests.get('http://api.openhluttaw.org/en/persons?page='+str(page))
	for person in json.loads(req_representatives.content)['results']:
	    persons.append(person)

    for person in persons:
	sms_ids = [ contact['id'] for contact in person['contact_details'] if contact['label'] == 'SMS']

	if len(sms_ids) == 2:
		url = base_url + '/en/persons/' + person['id'] + "/contact_details/" + sms_ids[0]
		#r = requests.delete(url,headers=headers)
		#print r.content

    
#update_en()
#update_my()
