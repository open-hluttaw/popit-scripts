#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import pandas
import io
from fish import ProgressFish

import utils

base_url = "http://api.openhluttaw.org"

df = pandas.DataFrame.from_csv('data/posts.csv',header=0,index_col=False)
df = df.where((pandas.notnull(df)), None)

del df['popit_id']

posts = df.to_dict(orient='records')

fish = ProgressFish(total=len(posts))

for progress,post in enumerate(posts):

	pyithu = [ i.strip() for i in post['constituency_pyithu'].split(',')]
	amyotha  = [i.strip() for i in post['constituency_amyotha'].split(',')]
	
	pyithu_ids = [ utils.search_post(id,base_url)['id'] for id in pyithu ]
	amyotha_ids = [ utils.search_post(id,base_url)['id'] for id in amyotha ]

        pyithu_list = []

        for pyithu_id in pyithu_ids:
            r = requests.get(base_url+'/en/posts/'+ pyithu_id)
            en_label = r.json()['result']['label']
            r = requests.get(base_url+'/my/posts/'+ pyithu_id)
            mm_label = r.json()['result']['label']

            pyithu_json = { 'popit_id': pyithu_id,
                            'label_en': en_label,
                            'label_mm' :mm_label,
                          }

            pyithu_list.append(pyithu_json)

        post['pyithu'] = pyithu_list

        amyotha_list = []

        for amyotha_id in amyotha_ids:
            r = requests.get(base_url+'/en/posts/'+ amyotha_id)
            en_label = r.json()['result']['label']
            r = requests.get(base_url+'/my/posts/'+ amyotha_id)
            mm_label = r.json()['result']['label']

            amyotha_json = { 'popit_id': amyotha_id,
                            'label_en': en_label,
                            'label_mm' :mm_label,
                          }
            amyotha_list.append(amyotha_json)


	post['amyotha'] = amyotha_list

  	fish.animate(amount=progress)	

json_out = json.dumps(posts, indent=4, sort_keys=True, ensure_ascii=False, encoding='utf8')

with io.open('townships.json', 'w', encoding='utf8') as json_file:
	json_file.write(unicode(json_out))
