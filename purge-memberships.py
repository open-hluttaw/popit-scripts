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

def purge_committee():
    r = requests.get(base_url +
             '/en/search/memberships?q=organization.classification:Committee')
    
    pages = r.json()['num_pages']

    memberships =[]

    for page in range(1,pages+1):
    r_memberships = \
            requests.get('http://api.openhluttaw.org/en/search/memberships?q:organization.classification:Committee&page='+str(page))
    for m in r_memberships.json()['results']
        memberships.append(m)
