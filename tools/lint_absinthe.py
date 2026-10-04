#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1]
s=(root/'server/npc/absinthe_tower.txt').read_text()
errors=[]
for token in ['32100','32102','32103','32104','32105','32106','32107','32108']:
    if token not in s: errors.append(f'missing item {token} in script')
for bgm in ['absinthe_t1.mid','absinthe_t2.mid','absinthe_t3.mid','absinthe_boss.mid','absinthe_victory.mid']:
    if not (root/'client/data/BGM'/bgm).exists(): errors.append(f'missing BGM {bgm}')
if '<TAB>' in s: errors.append('literal <TAB> markers remain in NPC script')
if 'playbgmall' in s: errors.append('legacy lowercase playbgmall remains; use playBGMall')
# Shop arrays should have equal lengths.
arrs=[]
for name in ['shop_id','shop_amt','shop_cost']:
    m=re.search(r'setarray\s+\.'+name+r',\s*(.*?);',s)
    if not m: errors.append(f'missing {name} array'); continue
    vals=[x for x in m.group(1).split(',') if x.strip()]
    arrs.append((name,len(vals)))
if len({n for _,n in arrs})>1: errors.append(f'shop array length mismatch: {arrs}')
print('Shop arrays:',arrs)
if errors:
    print('FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print('PASS: static Absinthe Tower package checks succeeded.')
