#!/usr/bin/env python3
"""统计 MiniMind 教学子集的数据分布。在 Colab 的 /content/minimind 中运行。"""
import argparse,collections,json,statistics
from pathlib import Path
from transformers import AutoTokenizer

def stats(values):
 s=sorted(values); n=len(s)
 def p(q): return s[min(n-1,int((n-1)*q))]
 return {'n':n,'mean':round(statistics.mean(s),1),'p50':p(.5),'p90':p(.9),'p95':p(.95),'max':max(s)}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--root',default='/content/minimind'); ap.add_argument('--limit',type=int,default=50000); a=ap.parse_args()
 root=Path(a.root); tok=AutoTokenizer.from_pretrained(root/'model',trust_remote_code=True)
 pre=[]
 with (root/'dataset/pretrain_t2t_mini.jsonl').open(encoding='utf-8') as f:
  for i,line in enumerate(f):
   if i>=a.limit: break
   pre.append(json.loads(line)['text'])
 print('PRETRAIN chars',stats([len(x) for x in pre])); pt=[len(tok.encode(x,add_special_tokens=False)) for x in pre]
 print('PRETRAIN tokens',stats(pt),'over_256',sum(x>256 for x in pt),f'{100*sum(x>256 for x in pt)/len(pt):.1f}%')
 turns=[]; uc=[]; ac=[]; ut=[]; at=[]; roles=collections.Counter(); reasoning=0
 with (root/'dataset/sft_t2t_mini.jsonl').open(encoding='utf-8') as f:
  for i,line in enumerate(f):
   if i>=a.limit: break
   conv=json.loads(line)['conversations']; turns.append(len(conv))
   for m in conv:
    role=m.get('role'); text=m.get('content',''); roles[role]+=1
    if role=='user': uc.append(len(text)); ut.append(len(tok.encode(text,add_special_tokens=False)))
    elif role=='assistant':
     ac.append(len(text)); at.append(len(tok.encode(text,add_special_tokens=False))); reasoning += bool(m.get('reasoning_content'))
 print('SFT turns',stats(turns)); print('roles',roles); print('user chars',stats(uc)); print('assistant chars',stats(ac)); print('user tokens',stats(ut)); print('assistant tokens',stats(at)); print('assistant reasoning',reasoning,f'{100*reasoning/len(ac):.1f}%')
if __name__=='__main__': main()
