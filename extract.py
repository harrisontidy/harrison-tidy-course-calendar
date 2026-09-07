import openpyxl,json,re
from pathlib import Path
w=openpyxl.load_workbook(r'C:\Users\harri\Downloads\View_My_Courses.xlsx',data_only=True)
out=[]
for row in list(w.active.values)[3:]:
    code,title=row[1].replace('_V','').split(' - ',1)
    patterns=[]
    for part in row[10].split('\n\n'):
        p=[x.strip() for x in part.split('|')]
        start,end=p[0].split(' - ')
        def minute(t):
            h,m,ap=re.match(r'(\d+):(\d+) ([ap])',t).groups()
            return (int(h)%12+(12 if ap=='p' else 0))*60+int(m)
        a,b=p[2].split(' - ')
        patterns.append(dict(start=start,end=end,days=[['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].index(d) for d in p[1].split() if d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']],alternate='Alternate' in p[1],fromMin=minute(a),toMin=minute(b),building=p[4] if len(p)>4 else '',floor=p[5].replace('Floor: ','') if len(p)>5 else '',room=p[6].replace('Room: ','') if len(p)>6 else ''))
    out.append(dict(id=len(out),code=code,title=title,term=1 if row[12].year==2026 else 2,section=row[6].split(' - ')[0].replace('_V',''),kind=row[8],delivery=row[9],instructor=(row[11] or 'Not listed').replace('\n\n',', '),credits=row[4],patterns=patterns))
Path(__file__).parent.joinpath('app/courses.json').write_text(json.dumps(out,indent=2))
print(f'Extracted {len(out)} sections, {len(set(c["code"] for c in out))} courses, {sum(len(c["patterns"]) for c in out)} meeting patterns')
