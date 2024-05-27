.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean install environment test version dist
POETRY_ACTIVATE = source $$(poetry env info --path)/bin/activate
EODAG_PATH = $$(poetry env info --path)

help:
	@echo "make clean"
	@echo " clean all jupyter checkpoints"
	@echo "make kernel"
	@echo " make ipykernel and environment based on eoenv.yml file"
	@echo "make environment"
	@echo " create a environment from eoenv.yml file"
	@echo "make teardown"
	@echo "uninstalls the kernel and removes environment"
	@echo "make jupyter"
	@echo " launch JupyterLab server"

clean:
	rm --force --recursive .ipynb_checkpoints/

kernel:
	make environment
	conda run -p ~/.conda/envs/eoenv python -m ipykernel install --user --name "eoenv" --display-name "eoenv"
	@echo -e "conda jupyter kernel is ready"

environment:
	cd ~/work/eodag-workflows/setup
	mkdir -p ~/.conda/envs
	mamba env create -p ~/.conda/envs/eoenv -f eoenv.yml
	mamba clean --all -f -y #&& fix-permissions /home/$NB_USER/.conda
	@echo -e "environment has been created and cleaned"

teardown:
	source activate ~/.conda/envs/eoenv
	jupyter kernelspec uninstall "eoenv" -f
	conda deactivate
	conda env remove -p ~/.conda/envs/eoenv

jupyter: #kernel develop
	jupyter lab ..