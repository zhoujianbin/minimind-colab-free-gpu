#!/usr/bin/env python3
import json
from pathlib import Path
p=Path('/content/minimind/dataset/tutorial_manifest.json')
if not p.exists(): raise SystemExit('数据 manifest 不存在，准备阶段失败')
m=json.loads(p.read_text()); requested=int(m['requested_count'])
for name in ('pretrain_t2t_mini.jsonl','sft_t2t_mini.jsonl'):
 item=m['files'].get(name,{}); data=p.parent/name
 if item.get('count')!=requested or not data.exists() or data.stat().st_size!=item.get('bytes'): raise SystemExit(f'数据校验失败: {name}')
print('DATA_VERIFIED',json.dumps(m,ensure_ascii=False))
