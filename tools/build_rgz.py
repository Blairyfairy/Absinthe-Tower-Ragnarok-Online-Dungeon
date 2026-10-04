#!/usr/bin/env python3
"""Build a Ragnarok Online RGZ patch from client/data and selected client Lua files.
RGZ layout follows the rAthena RGZ documentation: gzip-compressed sequential
entries with file/directory/end records.
"""
from pathlib import Path
import gzip, struct, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'client'/'patch'/'absinthero_0.2.0.rgz'
SRC=ROOT/'client'

def entry(kind: bytes, name: str, data=b''):
    raw=name.encode('utf-8')+b'\0'
    if len(raw)>255: raise ValueError(name)
    b=kind+bytes([len(raw)])+raw
    if kind==b'f': b+=struct.pack('<I',len(data))+data
    return b

files=[]
for p in (SRC/'data').rglob('*'):
    if p.is_file(): files.append(p)
lua=SRC/'lua'/'ItemInfo_AbsintheTower.lua'
if lua.exists(): files.append(lua)
files.sort()
seen=set(); payload=b''
for p in files:
    rel=p.relative_to(SRC).as_posix().replace('/','\\')
    parts=rel.split('\\')
    cur=[]
    for part in parts[:-1]:
        cur.append(part)
        d='\\'.join(cur)
        if d not in seen:
            payload+=entry(b'd',d); seen.add(d)
    payload+=entry(b'f',rel,p.read_bytes())
payload+=entry(b'e','end')
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('wb') as fh:
    with gzip.GzipFile(fileobj=fh, mode='wb', mtime=0) as gz: gz.write(payload)
print(f'Wrote {OUT} with {len(files)} files')
