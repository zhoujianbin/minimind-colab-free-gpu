from pathlib import Path
p=Path('/content/minimind-training.log'); lines=p.read_text(errors='replace').splitlines()
for key in ('TRAINING_START=','CONFIG ','PRETRAIN_SECONDS=','SFT_SECONDS=','TOTAL_SECONDS=','TRAINING_END=','TRAINING_COMPLETE'):
 vals=[x for x in lines if x.startswith(key)]; print(vals[-1] if vals else key+'MISSING')
for needle in ('(3125/3125)','(6250/6250)'):
 vals=[x for x in lines if needle in x]; print(vals[-1] if vals else needle+' MISSING')
