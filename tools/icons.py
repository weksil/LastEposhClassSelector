import re, json
from PIL import Image
css=open('sprite.css').read()
pos={m[0]:(int(m[1]),int(m[2]),int(m[3]),int(m[4])) for m in re.findall(r'\.icons-r-(\d+)\{background-position:(-?\d+)(?:px)? (-?\d+)(?:px)?;width:(\d+)px;height:(\d+)px\}', css)}
print(len(pos))
sp=Image.open('sprite.webp').convert('RGBA')
cls=json.load(open('cls_src.json')); mst=json.load(open('mst_src.json')); ab=json.load(open('ab_src.json'))
ids=list(cls)+list(mst)
for i in ids:
  n=ab[i]['sprite'].replace('a-r-','')
  x,y,w,h=pos[n]; x,y=-x,-y
  im=sp.crop((x,y,x+w,y+h))
  im.save(f'../assets/skills/{i}.webp','WEBP',quality=90,method=6)
print('icons', len(ids))
