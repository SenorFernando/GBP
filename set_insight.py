#!/usr/bin/env python3
# Uso: python3 set_insight.py data.json <C|D|E> <low|typical|high|unknown> "<resumen_es>" "<rango>" <ISO>
# Ej.: python3 set_insight.py data.json E low "Precios bajos para esta búsqueda; normalmente cuestan $480–$620." "$480–$620" 2026-10-25T16:20:00-06:00
# Guarda en la búsqueda: "insight": {"level","text","range","updated"}  (rango puede ser "")
import json,sys,datetime as D
LEVELS=('low','typical','high','unknown')
if len(sys.argv)<6: sys.exit(__doc__ or "Uso: python3 set_insight.py data.json <id> <level> \"<resumen_es>\" \"<rango>\" [ISO]")
f,i,lv,txt,rg=sys.argv[1:6]
if lv not in LEVELS: sys.exit("level debe ser uno de: "+", ".join(LEVELS))
t=sys.argv[6] if len(sys.argv)>6 else D.datetime.now(D.timezone(D.timedelta(hours=-6))).isoformat(timespec='seconds')
D.datetime.fromisoformat(t)  # valida ISO
d=json.load(open(f));s=next((x for x in d['searches'] if x['id']==i),None)
if not s: sys.exit("id no encontrado: "+i)
s['insight']={"level":lv,"text":txt.strip(),"range":rg.strip(),"updated":t}
json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
print("OK",i,lv)
