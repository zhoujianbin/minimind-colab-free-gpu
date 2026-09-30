#!/usr/bin/env python3
import os,subprocess
os.chdir('/content/minimind')
qs=['你好，请简单介绍一下你自己。','请用三句话解释什么是人工智能。','北京有哪些值得游览的地方？','写一个Python函数，计算两个整数之和。','为什么天空通常是蓝色的？']
text='1\n'+'\n'.join(qs+['exit'])+'\n'
cmd=['python','eval_llm.py','--load_from','model','--weight','full_sft','--hidden_size','512','--num_hidden_layers','8','--max_new_tokens','160','--temperature','0.7','--top_p','0.9','--open_thinking','0','--device','cuda:0']
subprocess.run(cmd,input=text,text=True,check=False)
