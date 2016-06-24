import requests
import json
import pandas

def hluttaw_to_popitid(identifier_hluttaw,base_url):
    # Get PopitID matching identifier_hluttaw column id for
    # representatives

    #using en due to bug https://github.com/Sinar/popit_ng/issues/171
    search_url = base_url + '/' + 'en' + '/search/persons?q="' + identifier_hluttaw +'"'
    search_req = requests.get(search_url)
    
    if search_req.json()['results']:
        return search_req.json()['results'][0]['id']
    else:
        return None

def org_name_to_popitid(name,base_url):
    # Get PopitID matching organization name

    #using en due to bug https://github.com/Sinar/popit_ng/issues/171
    search_url = base_url + '/' + 'en' + '/search/organizations?q="' +name + '"'
    search_req = requests.get(search_url)
    
    if search_req.json()['results']:
        return search_req.json()['results'][0]['id']
    else:
        return None

def post_to_popitid(post_label,base_url):

    search_url = base_url + '/' + 'en' + '/search/posts?q=' + post_label 
    search_req = requests.get(search_url)

    
    if search_req.json()['results']:
        return search_req.json()['results'][0]['id']
        
    else:
        return None

def search_post(post_label,base_url):
    #returns only if exact match
    #should loop through until exact match before returning None

    search_url = base_url + '/' + 'en' + '/search/posts?q=' + post_label 
    search_req = requests.get(search_url)
    
    if search_req.json()['results']:
	if search_req.json()['results'][0]['label'] == post_label: 
        	return search_req.json()['results'][0]
        
    else:
        return None

def post(post_id,base_url):
    search_url = base_url + '/' + 'en' + '/posts/' + post_id
    search_req = requests.get(search_url)
    
    if search_req.json()['result']:
    	return search_req.json()['result']
        
    else:
        return None

