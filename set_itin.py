#!/usr/bin/env python3
# Uso: python3 set_itin.py data.json <A|B|C|D> <itin.json> [checked_ISO]
# itin.json: {"cheapest":ITIN,"best":ITIN}  (opcional "checked"); best puede omitirse = igual al más barato
import json,sys,datetime as D
f,i,src=sys.argv[1:4]
it=json.load(open(src))
if 'cheapest' not in it: sys.exit("itin.json necesita 'cheapest'")
it.setdefault('best',it['cheapest'])
it['checked']=sys.argv[4] if len(sys.argv)>4 else it.get('checked') or D.datetime.now(D.timezone(D.timedelta(hours=-6))).isoformat(timespec='seconds')
d=json.load(open(f));s=next((x for x in d['searches'] if x['id']==i),None)
if not s: sys.exit("id no encontrado: "+i)
s['itineraries']={"checked":it['checked'],"cheapest":it['cheapest'],"best":it['best']}
json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
print("OK",i)
