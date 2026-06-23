********PROJECT SETUP GUIDE********

***PREREQUISITES***
Make sure you have Python 3.10 or higher installed.

Check your Python version:
On Windows:  python --version 
On Mac:  python3 --version

***PROJECT FOLDER SETUP***
Create a new folder anywhere on your computer
(Example: langgraph-course)

Open VS Code
Click: File → Open Folder → Select your project folder

Open the terminal in VS Code: Terminal → New Terminal

Now you can run all commands from inside VS Code.

# STEP 1 – CREATE A VIRTUAL ENVIRONMENT
On Windows:  python -m venv venv
On Mac:  python3 -m venv venv

# STEP 2 – ACTIVATE THE VIRTUAL ENVIRONMENT
On Windows:  venv\Scripts\activate
On Mac:  source venv/bin/activate

If activated correctly, you will see (venv) in your terminal.

# STEP 3 – INSTALL PROJECT DEPENDENCIES

Make sure you are inside your activated virtual environment and in the project folder where requirements.txt exists.

Run:
pip install -r requirements.txt

This will install all required libraries.

# STEP 4 – WHEN YOU ADD A NEW PACKAGE

If you manually add a package name to requirements.txt, then run:

pip install -r requirements.txt

This will install only the newly added packages.

If you install a package directly using pip, make sure your virtual environment is activated.
To install the package, run:

pip install package-name

Then update the requirements file to capture this change:

pip freeze > requirements.txt


***WORKING WITH JUPYTER NOTEBOOKS IN VS CODE***

This course uses Jupyter Notebooks inside VS Code for running and experimenting with LangGraph code.

# Required Packages:
Make sure the following packages are installed in your virtual environment:
jupyter
ipykernel

If they are already listed in requirements.txt, they will be installed automatically when you run:

pip install -r requirements.txt

If not, install them manually after activating your virtual environment:
pip install jupyter ipykernel
Then update your requirements file:
pip freeze > requirements.txt

# Opening Jupyter Notebooks in VS Code

Open VS Code
Open your project folder
Open any .ipynb file (or create a new one)
VS Code will automatically open the notebook interface.

# Selecting the Correct Python Kernel

It is very important to select the virtual environment kernel for your notebooks.
In the top-right corner of the notebook, click Select Kernel
Choose Python Environments
Select the Python interpreter from your project’s virtual environment
(Example: venv (Python 3.12.4))

Once selected, all notebook cells will run using the same environment where LangGraph and its dependencies are installed.


Always activate the virtual environment before installing any new packages

Ensure the same virtual environment is used in both:
VS Code terminal
Jupyter notebook kernel

If a package works in terminal but not in the notebook, the kernel is likely incorrect. 