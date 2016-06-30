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

def import_all():

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


def missing_memberships():
    persons = utils.persons(base_url)
    missing = [ (person['id'],person['identifiers'][0]['identifier']) \
                for person in persons if not person ['memberships'] ]

    for mp in MPs:
        payload = {}
        
        if isinstance(mp[5], basestring):

            for missing_party in missing:
                if mp[2] == missing_party[1]:

                    payload['role'] = 'MP'
                    payload['person_id'] = missing_party[0]
                    post_label = mp[8]
                   
                    post = utils.search_post(post_label, base_url)
                    
                    post_id = post['id']
                    organization_id = post['organization_id']

                    payload['post_id'] = post_id
                    payload['organization_id'] = organization_id

                    party = mp[6]
                    party_id = utils.org_name_to_popitid(party,base_url)
                    
                    payload['on_behalf_of_id'] = party_id
                    
                    start_date = mp[12]
                    payload['start_date'] = start_date

                    print mp[2]
                    print payload
                    
                    url = base_url + '/en/memberships'

                    r = requests.post(url, headers=headers, json=payload)
                    print r.content
                   

def missing_posts():
    amyotha_req = requests.get('http://api.openhluttaw.org/en/organizations/897739b2831e41109713ac9d8a96c845')
    memberships = amyotha_req.json()['result']['memberships']

    missing_posts = [ [ membership['id'], membership['person_id'] ] \
            for membership in memberships if not membership['post_id'] ]

    missing_hluttaw = [ [ id[0], id[1], utils.popitid_to_hulttaw(id[1],base_url)] for id in missing_posts ]
  
        
    for mp in MPs:

        for missing in missing_hluttaw:

            if mp[2] == missing[2]:

                payload = {}
                payload['role'] = 'MP'
                payload['person_id'] = missing[1]
                post_label = mp[8]
               
                post = utils.search_post(post_label, base_url)
                
                post_id = post['id']
                organization_id = post['organization_id']

                payload['post_id'] = post_id
                payload['organization_id'] = organization_id

                party = mp[6]
                party_id = utils.org_name_to_popitid(party,base_url)
                
                payload['on_behalf_of_id'] = party_id
                
                start_date = mp[12]
                payload['start_date'] = start_date

                print mp[2]
                print payload
                
                url = base_url + '/en/memberships/' + missing[0]

                print url

                r = requests.put(url, headers=headers, json=payload)
                print r.content

def missing_posts_pyithu():
    pyithu_req = requests.get('http://api.openhluttaw.org/en/organizations/7f162ebef80e4a4aba12361ea1151fce')
    memberships = pyithu_req.json()['result']['memberships']

    missing_posts = [ [ membership['id'], membership['person_id'] ] \
            for membership in memberships if not membership['post_id'] ]

    missing_hluttaw = [ [ id[0], id[1], utils.popitid_to_hulttaw(id[1],base_url)] for id in missing_posts ]
  
        
    for mp in MPs:

        for missing in missing_hluttaw:

            if mp[2] == missing[2]:

                payload = {}
                payload['role'] = 'MP'
                payload['person_id'] = missing[1]
                post_label = mp[8]
               
                post = utils.search_post(post_label, base_url)
                
                post_id = post['id']
                organization_id = post['organization_id']

                payload['post_id'] = post_id
                payload['organization_id'] = organization_id

                party = mp[6]
                party_id = utils.org_name_to_popitid(party,base_url)
                
                payload['on_behalf_of_id'] = party_id
                
                start_date = mp[12]
                payload['start_date'] = start_date

                print mp[2]
                print payload
                
                url = base_url + '/en/memberships/' + missing[0]

                print url

                r = requests.put(url, headers=headers, json=payload)
                print r.content
