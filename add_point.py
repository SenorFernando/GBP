#!/usr/bin/env python3
# Uso: python3 add_point.py data.json A 139 "Viva vía MTY" [ISO_t]
import json,sys,datetime as D
f,i,p=sys.argv[1],sys.argv[2],int(sys.argv[3]);a=sys.argv[4] if len(sys.argv)>4 else None
t=sys.argv[5] if len(sys.argv)>5 else D.datetime.now(D.timezone(D.timedelta(hours=-6))).isoformat(timespec='seconds')
d=json.load(open(f));s=next(x for x in d['searches'] if x['id']==i)
s['history'].append({"t":t,"price":p,"airline":a});d['updated']=t
json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
