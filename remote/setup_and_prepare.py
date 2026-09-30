#!/usr/bin/env python3
"""在干净 Colab 运行时准备固定版本 MiniMind 和确定性前缀教学子集。"""
import argparse,hashlib,itertools,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path('/content/minimind'); FULL=ROOT/'dataset_full'; DATA=ROOT/'dataset'
FILES=('pretrain_t2t_mini.jsonl','sft_t2t_mini.jsonl'); MINIMIND_COMMIT='f659b55761b754d306bd140573493a6543cafd7f'
def run(*args): print('+',' '.join(map(str,args)),flush=True); subprocess.run(list(map(str,args)),check=True)
def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()
def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--sample-count',type=int,default=int(os.environ.get('SAMPLE_COUNT','50000'))); args,_=parser.parse_known_args()
 count=args.sample_count
 if count<=0: raise SystemExit('SAMPLE_COUNT 必须大于 0')
 if not shutil.which('uv'): run(sys.executable,'-m','pip','install','uv')
 if not (ROOT/'.git').exists():
  run('git','clone','--filter=blob:none','--no-checkout','https://github.com/jingyaogong/minimind',ROOT); run('git','-C',ROOT,'fetch','--depth','1','origin',MINIMIND_COMMIT); run('git','-C',ROOT,'checkout','--detach',MINIMIND_COMMIT)
 head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
 if head!=MINIMIND_COMMIT: raise SystemExit(f'MiniMind 版本不匹配: {head}')
 run('uv','pip','install','--system','transformers==4.57.6','datasets==3.6.0','modelscope==1.37.0','sentencepiece','tiktoken','jsonlines','ujson','einops')
 FULL.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True); manifest={'minimind_commit':head,'sampling':'prefix','requested_count':count,'files':{}}
 for name in FILES:
  src=FULL/name
  if not src.exists(): run('modelscope','download','--dataset','gongjy/minimind_dataset',name,'--local_dir',FULL)
  fd,tmp=tempfile.mkstemp(prefix=name+'.',suffix='.tmp',dir=DATA); actual=0
  try:
   with os.fdopen(fd,'w',encoding='utf-8') as fout,src.open(encoding='utf-8') as fin:
    for line in itertools.islice(fin,count): fout.write(line); actual+=1
   if actual<count: raise RuntimeError(f'{name} 只有 {actual} 条，少于请求的 {count}')
   os.replace(tmp,DATA/name)
  finally:
   if os.path.exists(tmp): os.unlink(tmp)
  manifest['files'][name]={'count':actual,'bytes':(DATA/name).stat().st_size,'sha256':sha256(DATA/name)}; print(name,manifest['files'][name])
 (DATA/'tutorial_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8'); print('DATA_READY',json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__': main()
