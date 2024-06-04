.ONESHELL:
SHELL = /bin/bash

# Define variables
ENV_YML = environment.yml
ENV_NAME = eoenv
KERNEL_NAME = eo
LOCAL_CONDA = ~/.conda

GIT_REPO = https://github.com/npikall/eodag-notebooks.git
GIT_BRANCH = main
REPO_NAME = eodag-notebooks

# Help command to display available targets
help:
	@echo "Makefile for setting up environment, kernel, and pulling notebooks"
	@echo ""
	@echo "Usage:"
	@echo "  make notebooks    - Pull the notebooks from the Git repository"
	@echo "  make environment  - Create the conda environment"
	@echo "  make kernel       - Create the Jupyter kernel"
	@echo "  make all          - Run all the above tasks"
	@echo "  "
	@echo "  make teardown     - Remove the environment and kernel"
	@echo "  make delete       - Deletes the cloned Repository and removes kernel and environment"
	@echo "  make clean        - Removes ipynb_checkpoints"
	@echo "  make help         - Display this help message"


.PHONY: all notebooks environment kernel teardown clean

all: notebooks environment kernel setup

# Pull the notebooks from the Git repository
notebooks: 
	@echo "Cloning the Git repository..."
	git clone $(GIT_REPO) -b $(GIT_BRANCH) $(REPO_NAME)
	@echo "Repository cloned."

setup:
	cd $(REPO_NAME)
	python setup.py

# Create the environment using conda
environment: 
	@echo "Creating conda environment..."
	mkdir -p ~/.conda/envs
	mamba env create -p $(LOCAL_CONDA)/envs/$(ENV_NAME) -f $(ENV_YML)
	@echo "Environment $(ENV_NAME) created."

# Create a Jupyter kernel from the environment
kernel: environment
	@echo "Creating Jupyter kernel..."
	mamba run -p $(LOCAL_CONDA)/envs/$(ENV_NAME) python -m ipykernel install --user --name "$(KERNEL_NAME)" --display-name "$(KERNEL_NAME)"
	@echo "Kernel $(KERNEL_NAME) created."

# Remove the environment and kernel
teardown:
	@echo "Removing the Kernel and the Environment..."
	jupyter kernelspec uninstall "$(KERNEL_NAME)" -f 
	mamba env remove -p $(LOCAL_CONDA)/envs/$(ENV_NAME)
	@echo "Kernel and Environment have been removed."

delete: teardown
	@echo "Deleting all files in $(REPO_NAME)..."
	rm -rf $(REPO_NAME)
	@echo "$(REPO_NAME) has been deleted."

# Clean up. Removes ipynb_checkpoints
clean:
	@echo "Removing ipynb_checkpoints..."
	rm --force --recursive .ipynb_checkpoints/
	@echo "Clean up completed."