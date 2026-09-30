#!/usr/bin/env python3
"""在 Colab 安装 MiniMind、下载数据并生成教学规模子集。"""
import argparse,itertools,subprocess
from pathlib import Path
ROOT=Path('/content/minimind'); FULL=ROOT/'dataset_full'; DATA=ROOT/'dataset'
FILES=('pretrain_t2t_mini.jsonl','sft_t2t_mini.jsonl')
def run(*args):
 print('+',' '.join(map(str,args)),flush=True); subprocess.run(list(map(str,args)),check=True)
def main():
 p=argparse.ArgumentParser(); p.add_argument('--sample-count',type=int,default=50000); a=p.parse_args()
 if not (ROOT/'.git').exists(): run('git','clone','--depth','1','https://github.com/jingyaogong/minimind',ROOT)
 run('uv','pip','install','--system','transformers==4.57.6','datasets==3.6.0','modelscope==1.37.0','sentencepiece','tiktoken','jsonlines','ujson','einops')
 FULL.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
 for name in FILES:
  src=FULL/name
  if not src.exists(): run('modelscope','download','--dataset','gongjy/minimind_dataset',name,'--local_dir',FULL)
  dst=DATA/name
  with src.open(encoding='utf-8') as fin,dst.open('w',encoding='utf-8') as fout: fout.writelines(itertools.islice(fin,a.sample_count))
  print(f'{name}: {a.sample_count} 条 -> {dst}')
 print('DATA_READY')
if __name__=='__main__': main()
