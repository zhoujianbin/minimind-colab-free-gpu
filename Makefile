.PHONY: check
check:
	bash -n scripts/*.sh remote/*.sh
	python3 -m compileall -q remote tests
	python3 -m json.tool notebooks/colab_minimind_from_scratch.ipynb >/dev/null
	python3 tests/check_repo.py
	@if command -v colab >/dev/null 2>&1; then colab exec --help | grep -q -- '--file'; colab upload --help | grep -q local_path; fi
	@if command -v shellcheck >/dev/null 2>&1; then shellcheck scripts/*.sh remote/*.sh; fi
