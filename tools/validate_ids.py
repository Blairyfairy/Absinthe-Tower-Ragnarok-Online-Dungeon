#!/usr/bin/env python3
import argparse,re,sys
from pathlib import Path

CUSTOM=range(32100,32109)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rathena',type=Path,help='Optional rAthena checkout to scan for IDs')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    script=(root/'server/npc/absinthe_tower.txt').read_text()
    mobs=[]
    for m in re.finditer(r'(?<!\d)(\d{3,5})(?=,)',script):
        n=int(m.group(1))
        if n not in CUSTOM and n not in mobs: mobs.append(n)
    print(f'Found {len(mobs)} numeric monster/item references in script.')
    print('Custom item IDs:', ', '.join(map(str,CUSTOM)))
    if args.rathena:
        candidates=list(args.rathena.glob('db/**/*.yml'))+list(args.rathena.glob('db/**/*.txt'))
        blob='\n'.join(p.read_text(errors='ignore') for p in candidates)
        missing=[n for n in mobs if str(n) not in blob]
        if missing:
            print('WARNING: numeric references not found textually in rAthena DB files:',missing)
        else:
            print('All referenced numeric IDs were found textually in DB files.')
    else:
        print('No rAthena checkout supplied; runtime validation is still required.')
    return 0
if __name__=='__main__': sys.exit(main())
