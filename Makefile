.ONESHELL:
SHELL = /bin/bash

# Define variables
ENV_YML = environment.yml
ENV_NAME = eoenv
KERNEL_NAME = eo

GIT_REPO = https://git.geo.tuwien.ac.at/npikall/eodag-workflows.git
GIT_BRANCH = main
REPO_NAME = eodag-workflows

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
	@echo "  make clean        - Removes ipynb_checkpoints"
	@echo "  make help         - Display this help message"


.PHONY: all notebooks environment kernel teardown clean

all: notebooks environment kernel 

# Pull the notebooks from the Git repository
notebooks:
	@echo "Cloning the Git repository..."
	git clone $(GIT_REPO) -b $(GIT_BRANCH) $(REPO_NAME)
	@echo "Repository cloned."

# Create the environment using conda
environment: 
	@echo "Creating conda environment..."
	cd $(REPO_NAME)
	mkdir -p ~/.conda/envs
	mamba env create -p ~/.conda/envs/$(ENV_NAME) -f $(ENV_YML)
	mamba clean --all
	@echo "Environment $(ENV_NAME) created."

# Create a Jupyter kernel from the environment
kernel: environment
	@echo "Creating Jupyter kernel..."
	mamba run -p ~/.conda/envs/$(ENV_NAME) python -m ipykernel install --user --name "$(KERNEL_NAME)" --display-name "$(KERNEL_NAME)"
	@echo "Kernel $(KERNEL_NAME) created."

# Remove the environment and kernel
teardown:
	@echo "Removing the Kernel and the Environment..."
	mamba activate ~/.conda/envs/$(ENV_NAME)
	jupyter kernelspec uninstall "$(ENV_NAME)" -f
	mamba deactivate
	mamba env remove -p ~/.conda/envs/$(ENV_NAME)
	@echo "Kernel and Environment have been removed."
	

# Clean up. Removes ipynb_checkpoints
clean:
	@echo "Removing ipynb_checkpoints..."
	rm --force --recursive .ipynb_checkpoints/
	@echo "Clean up completed."