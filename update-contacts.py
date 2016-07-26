#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import pandas

import utils

from fish import ProgressFish

base_url = "http://api.openhluttaw.org"

#store key in token.txt Don't commit this file
key = open('token.txt')
token = 'Token '+key.read().rstrip()

headers = {'Authorization': token }

def update_contact_translation_labels():

    page_request = requests.get('http://api.openhluttaw.org/my/persons')
    pages = page_request.json()['num_pages']

    persons = []

    for page in range(1,pages+1):
    	req_representatives = requests.get('http://api.openhluttaw.org/en/persons?page='+str(page))
        for person in json.loads(req_representatives.content)['results']:
            persons.append(person)

    for progress, person in enumerate(persons):
        if person['contact_details']:
            for contact in person['contact_details']:
                if contact['type'] == 'cell':
                    payload_mm = {'label':'ဖုန်းနံပါတ်'}
                    payload_en = {'label':'Mobile Phone'}

                    r = requests.put(base_url+'/my/persons/'+
                                     person['id'] + '/contact_details/' +
                                     contact['id'],
                                     headers = headers,
                                     json=payload_mm)
                    print r.content
                    r = requests.put(base_url+'/en/persons/'+
                                     person['id'] + '/contact_details/' +
                                     contact['id'],
                                     headers = headers,
                                     json=payload_en)
                    print r.content


                if contact['type'] == 'cell':
                    payload = {'label':'ဖုန်းနံပါတ်'}

                    r = requests.put(base_url+'/my/persons/'+
                                     person['id'] + '/contact_details/' +
                                     contact['id'],
                                     headers = headers,
                                     json=payload)
                    print r.content

update_contact_translation_labels()
