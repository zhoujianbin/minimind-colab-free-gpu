.PHONY: check
check:
	bash -n scripts/*.sh remote/*.sh
	python3 -m compileall -q remote
	python3 -m json.tool notebooks/colab_minimind_from_scratch.ipynb >/dev/null
