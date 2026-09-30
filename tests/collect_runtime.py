import platform,torch,transformers,datasets,modelscope
print('python',platform.python_version()); print('torch',torch.__version__); print('cuda',torch.version.cuda); print('gpu',torch.cuda.get_device_name(0)); print('transformers',transformers.__version__); print('datasets',datasets.__version__); print('modelscope',modelscope.__version__)
