# Store-Warehouse

# Table of content
1. [About](#about)
2. [Installation](#installation)
    1. [General](#1-general)
    2. [Making migrations](#2-making-migrations)
3. [Development](#development)
    1. [Running](#1-running)

# About
API communication between 2 services: Store and Warehouse  

# Installation
### 1. General
- Create virtual environment `virtualenv --python=/usr/bin/python3.6 .venv`
- Activate env `source .venv/bin/activate`
- Run `pip install -r requirements.txt` to install dependencies
- Configure `STORE_URL` at `Warehouse/Warehouse/settings.py`
- Configre `WAREHOUSE_URL` at `Store/Store/settings.py`

#### 2. Making migrations
- Run `python Warehouse/manage.py makemigrations`
- Run `python Warehouse/manage.py migrate` to apply migrations
- Run `python Warehouse/manage.py runserver {PORT}`
- Run `python Store/manage.py makemigrations`
- Run `python Store/manage.py migrate` to apply migrations
- ***Do not forget to provide superuser for each service***

# Development
#### 1. Running
- Run `python {SERVICE}/manage.py runserver {PORT}` for each service (`Warehouse` first). 
  Make it sure, that you running services on the different ports

