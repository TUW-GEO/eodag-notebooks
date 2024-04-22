# Setup a new Project

This File intends to explain the steps to properly start a new codeing project and makeing a repo.

## Conda venv (Virtual Environment)
### Initialisation
Use the following to create a new conda environment. Use something descriptive as the Environment name (in this example it is `myenv`).

```
conda create -n myenv
```

Next you might want to see which Environments you already have and which is already beeing used. The following command shows you all available environments and the `*` symbolizes which environment is activated.

```
conda env list
```

```
    # conda environments:
    #
    base                  *  C:\ProgramData\anaconda3
    myenv                    C:\Users\user\.conda\envs\myenv
```

Now you want to activate your new environment. (in VSCode you will need to change the Interpreter)

```
conda activate myenv
```

After the Environment has been activated you can start installing packages.
Either you install a single Package (like `numpy` in this example)

```
conda install numpy
```

or you can install many packages.

```
conda install numpy pandas matplotlib
```
It is even possible to install with pip (as long as pip is installed in conda)
```
pip install numpy
```
### Clone Environment
To clone an environment form a `.yml` file use:
```
conda env create -n myenv --file ENV.yml
```
Or from a text file useing
```
conda create -n myenv --file ENV.txt
```

### Sharing your Environment
To share your Environment you could either use `conda` or `pip`. 
For conda use:
```
conda env export -n myenv > environment.yml
```
For pip use:
```
pip freeze > requirements.txt
```

### Removing (Deleting) an Environment

In order to delete a conda environment use
```
conda remove -n myenv --all
```


## Python venv (Virtual Environment)
### Initialisation

1. Make a directory where the project should be
2. Initialize a new virtual environment. Use the following command to create the .venv directory which houses the environment (any Name can be given, but env, .env, venv, .venv are often used)
```
python -m venv .venv
```

3. Activate the environment `.venv` by useing (for Linux)
```
source .venv/bin/activate
```
or for Windows use (might need to deactivate base environment beforehand with `conda deactivate`)
```
activate
```

4. Create a file called `.gitignore` and write `.venv` (or in general files that shouldn`t be tracked). Git will then ignore the environment, or else Git might have too many files too track (easily more than 10 000) aftrer initialization

5.  Use the following command to install the Packages required for the project
```
pip install <file1> [<file2> ...]
```

6. Create the actual `.py` or `.ipynb` files to start writing the code
7. Start tracking your files with `git init` or use a remote repo
8. To create a requirements file (which helps other people to easily install all needed packages in the future when useing your code) use the following command
```
pip freeze > requirements.txt
```

9. Write a  `README.md` file, which lets others know how to use the repo

### Remove an environment
In order to remove a virtual environment that has been made with ``python venv`` the environment needs to be __deactivated__ at first (similar command as creation, just with *deactivate* instead of *activate*). After that use the following comand to remove or delete your environment.
```
rm -r .venv
```

## README file convention
The following informations are taken from [Github Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

A README is often the first item a visitor will see when visiting your repository. README files typically include information on:

- What the project does
- Why the project is useful
- How users can get started with the project
- Where users can get help with your project
- Who maintains and contributes to the project