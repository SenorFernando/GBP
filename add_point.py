#!/usr/bin/env python3
# Uso: python3 add_point.py data.json <ID> <precio> "<aerolínea>" [ISO_t]
# IDs: C, D, CV (desde Ciudad Juárez) · NY1, NY2, NY3 (desde Nueva York, viajes de Dannia)
# Ej.: python3 add_point.py data.json NY1 832 "Viva" 2026-11-02T15:47:00-06:00
# Solo agregar precios verificados en el sitio oficial de la aerolínea.
import json,sys,datetime as D
BLOCKED={'E'}  # búsqueda retirada: nunca volver a agregarla
if len(sys.argv)<4: sys.exit("Uso: python3 add_point.py data.json <ID> <precio> \"<aerolínea>\" [ISO_t]")
f,i,p=sys.argv[1],sys.argv[2],int(sys.argv[3]);a=sys.argv[4] if len(sys.argv)>4 else None
if i in BLOCKED: sys.exit("id bloqueado: "+i)
t=sys.argv[5] if len(sys.argv)>5 else D.datetime.now(D.timezone(D.timedelta(hours=-6))).isoformat(timespec='seconds')
D.datetime.fromisoformat(t)  # valida ISO
d=json.load(open(f));s=next((x for x in d['searches'] if x['id']==i),None)
if not s: sys.exit("id no encontrado: "+i+" (válidos: "+", ".join(x['id'] for x in d['searches'])+")")
s.setdefault('history',[]).append({"t":t,"price":p,"airline":a});d['updated']=t
json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
print("OK",i,p)
