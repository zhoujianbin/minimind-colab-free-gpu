#!/usr/bin/env python3
import os,subprocess
prompt=os.environ.get('PROMPT','').strip()
if not prompt: raise SystemExit('PROMPT 不能为空')
os.chdir('/content/minimind')
cmd=['python','eval_llm.py','--load_from','model','--weight','full_sft','--hidden_size','512','--num_hidden_layers','8','--max_new_tokens',os.environ.get('MAX_NEW_TOKENS','128'),'--temperature','0.7','--top_p','0.9','--open_thinking','0','--device','cuda:0']
r=subprocess.run(cmd,input='1\n'+prompt+'\n\n',text=True,capture_output=True)
print(r.stdout); print(r.stderr)
if r.returncode: raise SystemExit(f'推理失败: {r.returncode}')
print('INFERENCE_OK')
