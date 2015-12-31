VENV = venv

PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

PIP_MIRROR = https://pypi.tuna.tsinghua.edu.cn/simple

PIP_INSTALL = $(PIP) install


deps:
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -r requirements.txt

venv:
	@virtualenv $(VENV) --prompt '<venv:resimsimi>'
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -U pip setuptools
