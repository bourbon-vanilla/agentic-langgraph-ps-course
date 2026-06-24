# Project Setup Guide

## Prerequisites

Make sure you have Python 3.10 or higher installed.

Check your Python version:

- **Windows:** `python --version`
- **Mac:** `python3 --version`

## Project Folder Setup

1. Create a new folder anywhere on your computer (Example: `langgraph-course`)
2. Open VS Code
3. Click: File → Open Folder → Select your project folder
4. Open the terminal in VS Code: Terminal → New Terminal

Now you can run all commands from inside VS Code.

### Step 1 – Create a Virtual Environment

- **Windows:** `python -m venv venv`
- **Mac:** `python3 -m venv venv`

### Step 2 – Activate the Virtual Environment

- **Windows:** `venv\Scripts\activate`
- **Mac:** `source venv/bin/activate`

If activated correctly, you will see `(venv)` in your terminal.

### Step 3 – Install Project Dependencies

Make sure you are inside your activated virtual environment and in the project folder where `requirements.txt` exists.

```bash
pip install -r requirements.txt
```

This will install all required libraries.

### Step 4 – When You Add a New Package

If you manually add a package name to `requirements.txt`, then run:

```bash
pip install -r requirements.txt
```

This will install only the newly added packages.

If you install a package directly using pip, make sure your virtual environment is activated. To install the package, run:

```bash
pip install package-name
```

Then update the requirements file to capture this change:

```bash
pip freeze > requirements.txt
```

## Working with Jupyter Notebooks in VS Code

This course uses Jupyter Notebooks inside VS Code for running and experimenting with LangGraph code.

### Required Packages

Make sure the following packages are installed in your virtual environment:

- `jupyter`
- `ipykernel`

If they are already listed in `requirements.txt`, they will be installed automatically when you run:

```bash
pip install -r requirements.txt
```

If not, install them manually after activating your virtual environment:

```bash
pip install jupyter ipykernel
```

Then update your requirements file:

```bash
pip freeze > requirements.txt
```

### Opening Jupyter Notebooks in VS Code

1. Open VS Code
2. Open your project folder
3. Open any `.ipynb` file (or create a new one)
4. VS Code will automatically open the notebook interface.

### Selecting the Correct Python Kernel

It is very important to select the virtual environment kernel for your notebooks.

1. In the top-right corner of the notebook, click **Select Kernel**
2. Choose **Python Environments**
3. Select the Python interpreter from your project's virtual environment (Example: `venv (Python 3.12.4)`)

Once selected, all notebook cells will run using the same environment where LangGraph and its dependencies are installed.

> **Note:** Always activate the virtual environment before installing any new packages.

Ensure the same virtual environment is used in both:

- VS Code terminal
- Jupyter notebook kernel

If a package works in terminal but not in the notebook, the kernel is likely incorrect.
