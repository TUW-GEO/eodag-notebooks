.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean install environment test version dist
POETRY_ACTIVATE = source $$(poetry env info --path)/bin/activate
EODAG_PATH = $$(poetry env info --path)

help:
	@echo "make clean"
	@echo " clean all jupyter checkpoints"
	@echo "make manifest"
	@echo " lock dependencies of poetry environment"
	@echo "make develop"
	@echo " create a development poetry environment"
	@echo "make kernel"
	@echo " make ipykernel based on poetry lock file"
	@echo "make jupyter"
	@echo " launch JupyterLab server"

clean:
	rm --force --recursive .ipynb_checkpoints/

develop:
	poetry install
	$(POETRY_ACTIVATE) pangeo-workflow-examples
	@echo -e "poetry development environment is ready."

kernel:
	cd ~/work/eodag-workflows/setup
	mkdir -p ~/.conda/envs
	mamba env create -p ~/.conda/envs/eoenv -f eoenv.yml
	mamba clean --all -f -y #&& fix-permissions /home/$NB_USER/.conda
	@echo -e "environment has been created and cleaned"
	conda run -p ~/.conda/envs/eoenv python -m ipykernel install --user --name "eoenv" --display-name "eoenv"
	@echo -e "conda jupyter kernel is ready"

simple-kernel:
	cd ~/work/eodag-workflows/setup
	mkdir -p ~/.conda/envs
	mamba env create -p ~/.conda/envs/eoenv -f eoenv-simple.yml
	mamba clean --all -f -y #&& fix-permissions /home/$NB_USER/.conda
	@echo -e "environment has been created and cleaned"
	conda run -p ~/.conda/envs/eoenv python -m ipykernel install --user --name "eoenv" --display-name "eoenv"
	@echo -e "conda jupyter kernel is ready"

teardown:
	source activate ~/.conda/envs/eoenv
	jupyter kernelspec uninstall "eoenv" -f
	conda deactivate
	conda env remove -p ~/.conda/envs/eoenv

jupyter: kernel develop
	jupyter lab .
