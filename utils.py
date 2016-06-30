import requests
import json
import pandas

def hluttaw_to_popitid(identifier_hluttaw,base_url):
    # Get PopitID matching identifier_hluttaw column id for
    # representatives

    #using en due to bug https://github.com/Sinar/popit_ng/issues/171
    search_url = base_url + '/' + 'en' + '/search/pmersons?q="' + identifier_hluttaw +'"'
    search_req = requests.get(search_url)
    
    if search_req.json()['results']:
        return search_req.json()['results'][0]['id']
    else:
        return None

def popitid_to_hulttaw(popit_id,base_url):
    url = base_url + '/en/persons/' + popit_id
    r = requests.get(url)
    
    if r.json()['result']:
        return r.json()['result']['identifiers'][0]['identifier']
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

def persons(base_url,id=None):
    #returns json of one person if id provided, or all if None
    #Getting total number of pages via REST request
   
    if id:
        url = base_url + '/' + 'en' + '/person/' + id
        req_representatives = requests.get(base_url + '/en/persons/' + id)
        return json.loads(req_representatives.content)['result']

    else:
        page_request = requests.get('http://api.openhluttaw.org/en/persons')
        pages = page_request.json()['num_pages']
 
        persons =[]
        for page in range(1,pages+1):
            req_representatives = requests.get(base_url + '/en/persons?page='+str(page))
            for person in json.loads(req_representatives.content)['results']:
                persons.append(person)
        return persons

def search_area(base_url,area):
    #return area json
    
    r = requests.get(base_url + '/en/areas')
    
    if search_req.json()['results']:
        print search_req.json()['results']
        if search_req.json()['results'][0]['name'] == area:
        	return search_req.json()['results'][0]
        
    else:
        return None


