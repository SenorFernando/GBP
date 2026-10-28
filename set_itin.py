#!/usr/bin/env python3
# Uso: python3 set_itin.py data.json <A|B|C|D|E> <itin.json> [checked_ISO]
# itin.json: {"cheapest":ITIN,"best":ITIN}  (opcional "checked"); best puede omitirse = igual al más barato
# opcional "byAirline": [ITIN,...] el redondo más barato por aerolínea; se guarda ordenado por precio
# y se agrega {t,price} de cada aerolínea a s['airlineHistory'][aerolínea] (sin duplicar t)
import json,sys,datetime as D
f,i,src=sys.argv[1:4]
it=json.load(open(src))
if 'cheapest' not in it: sys.exit("itin.json necesita 'cheapest'")
it.setdefault('best',it['cheapest'])
it['checked']=sys.argv[4] if len(sys.argv)>4 else it.get('checked') or D.datetime.now(D.timezone(D.timedelta(hours=-6))).isoformat(timespec='seconds')
d=json.load(open(f));s=next((x for x in d['searches'] if x['id']==i),None)
if not s: sys.exit("id no encontrado: "+i)
s['itineraries']={"checked":it['checked'],"cheapest":it['cheapest'],"best":it['best']}
ba=it.get('byAirline')
if isinstance(ba,list) and ba:
  s['itineraries']['byAirline']=sorted([x for x in ba if isinstance(x,dict) and 'price' in x],key=lambda x:x['price'])
  # historial por aerolínea: airlineHistory[aerolínea] = [{t,price},...] ordenado por tiempo
  ah=s.setdefault('airlineHistory',{})
  def _k(t):
    try: return D.datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()
    except Exception: return 0
  for x in s['itineraries']['byAirline']:
    a=x.get('airline')
    if not a: continue
    pts=ah.setdefault(a,[])
    if any(p.get('t')==it['checked'] for p in pts): continue
    pts.append({"t":it['checked'],"price":x['price']})
    pts.sort(key=lambda p:_k(p.get('t','')))
json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
print("OK",i)
