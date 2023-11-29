# Multinational Retail Data Centralisation 💼
------------------
### Description

This project is for collating retail sales data for a multinational company, where data is spread across multiple data sources to one centralised database. Facilitating accessibility and analysing for company team members to become more data-driven.

### Aim

Using [![python](https://img.shields.io/badge/Python-1f425f.svg)](https://www.python.org/) class methods are utilised for **connecting** to data sources, data **extraction** and **cleaning** downloaded data.

Cleaned data will be uploaded to a centralised [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-1f425f.svg)](https://www.postgresql.org) database. The star-based database schema developed manually, ensuring data columns are of the correct data type.

Querying the newly created centralised database to get up-to-date business metrics, using [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-1f425f.svg)](https://www.postgresql.org).

### Learnt Objectives

 - Advanced object orientated programming in python.
 - Advanced development of class and methods
 - 

# Tasks

- [x] Project Title
- [x] Table of Contents, if the README file is long
- [ ] A description of the project: what it does, the aim of the project, and what you learned
- [ ] Installation instructions
- [ ] Usage instructions
- [ ] File structure of the project
- [ ] License information
------------------------
- [x] Clean up class methods files
- [ ] Access modifiers
- [ ] Testing_script
- [ ] Database schema file
- [ ] Database query file
- [ ] Read me file
- [ ] Set up and installation
- [ ] Examples
- [x] Docstrings for class and methods

## Installation Instructions ⚙
-------------
Download or Clone repository.

OR 

Download class files

    - database_utils.py
    - data_extraction.py
    - data_cleaning.py

(Note access keys and database connection files will need to be created for specified database connections.)


## Usage Instructions ⏯ 

Import class modules:

```py
import database_utils
import data_extraction
import data_cleaning
```

Create instances of each class:

```py
connector = database_utils.DatabaseConnector()
extractor = data_extraction.DataExtractor()
cleaning = data_cleaning.DataCleaning()

```
- [ ] examples of each data source connection
- [ ] cleaning example
- [ ] uploading to local database example 
- [ ] include template for local credentials file to connect to local sql server 

.....

## File Structure 📂
----------------------------

- [ ] input file structure


## License information 🗒
------------------------

- [ ] get license info

## Example Use / Demo
-----------------------

Input here examples of extracting, cleaning and uploading data. 

Use .pdf for workable online example. 

## Open source packages used in this project

![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![VsCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)


#### Database connecting
![sqlAlchemy](https://img.shields.io/badge/sqlAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![boto3](https://img.shields.io/badge/boto3-3775A9?style=for-the-badge&logo=amazonaws&logoColor=white)

#### Data extracting/downloading
![requests](https://img.shields.io/badge/requests-3775A9?style=for-the-badge&logo=pypi&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white)
![tabula](https://img.shields.io/badge/tabula-3775A9?style=for-the-badge&logo=pypi&logoColor=white)

#### Data cleaning
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Numpy]( https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)