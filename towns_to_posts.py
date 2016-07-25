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

        post['pyithu_ids'] = pyithu_ids
	post['amyotha_ids'] = amyotha_ids

  	fish.animate(amount=progress)	

json_out = json.dumps(posts, indent=4, sort_keys=True, ensure_ascii=False, encoding='utf8')

with io.open('townships.json', 'w', encoding='utf8') as json_file:
	json_file.write(unicode(json_out))
