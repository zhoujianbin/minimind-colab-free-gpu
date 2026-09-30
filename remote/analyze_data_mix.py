#!/usr/bin/env python3
"""用透明的关键词规则估算教学子集的任务类型配比。

原始 MiniMind JSONL 没有统一的 source/category 标签，因此本结果是弱监督估算，
不是数据集官方标注。规则故意写在文件中，方便学习者审阅和修改。
"""
import argparse,collections,json
from pathlib import Path
RULES={
 '代码与技术':['代码','编程','python','javascript','java','c++','sql','函数','程序','算法','api','linux','软件','数据库'],
 '数学与逻辑推理':['数学','计算','方程','概率','证明','几何','求解','推理','逻辑题','多少'],
 '翻译与语言':['翻译','译成','英文','英语','中文','日语','法语','语法','单词'],
 '摘要改写与信息抽取':['总结','摘要','概括','提取','改写','润色','纠错','关键词','分类'],
 '创作与内容生成':['写一','生成一','诗','故事','文案','文章','小说','剧本','邮件','标题','创意','广告'],
 '建议规划与推荐':['建议','计划','规划','推荐','怎么办','方案','策略','步骤','如何准备'],
 '知识问答与解释':['什么是','为什么','解释','介绍','区别','原因','原理','历史','科学','请问','如何'],
 '身份与日常对话':['你是谁','模型','开发','你好','最近','喜欢','聊天','心情','谢谢','再见'],
 '安全伦理与拒答':['违法','犯罪','武器','毒品','自杀','攻击','黑客','隐私','伦理','安全'],
}
def labels(text):
 text=text.lower(); found=[name for name,words in RULES.items() if any(w.lower() in text for w in words)]
 return found or ['其他/难以判定']
def add_fraction(counter,names):
 for name in names: counter[name]+=1/len(names)
def show(title,counter,total):
 print(); print(title)
 for name,value in counter.most_common(): print(f'{name:18s} {value/total*100:6.2f}%  ({value:.1f})')
def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='/content/minimind'); p.add_argument('--limit',type=int,default=50000); a=p.parse_args(); root=Path(a.root)
 pre=collections.Counter(); pre_n=0
 with (root/'dataset/pretrain_t2t_mini.jsonl').open(encoding='utf-8') as f:
  for i,line in enumerate(f):
   if i>=a.limit: break
   add_fraction(pre,labels(json.loads(line)['text'])); pre_n+=1
 show('预训练：样本多标签均分后的任务类型估算',pre,pre_n)
 conv_mix=collections.Counter(); msg_mix=collections.Counter(); conv_n=user_n=0
 with (root/'dataset/sft_t2t_mini.jsonl').open(encoding='utf-8') as f:
  for i,line in enumerate(f):
   if i>=a.limit: break
   votes=collections.Counter(); conv_n+=1
   for m in json.loads(line)['conversations']:
    if m.get('role')!='user': continue
    ls=labels(m.get('content','')); add_fraction(msg_mix,ls); user_n+=1
    for x in ls: votes[x]+=1/len(ls)
   if votes:
    top=max(votes.values()); add_fraction(conv_mix,[k for k,v in votes.items() if v==top])
 show('SFT：每组对话的主导任务类型估算',conv_mix,conv_n)
 show('SFT：按 user 消息加权的任务类型估算',msg_mix,user_n)
 print(); print('注意：该数据没有官方类别标签；以上为关键词弱监督估算。请人工抽检并按目标任务重写 RULES。')
if __name__=='__main__': main()
