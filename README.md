# Multinational Retail Data Centralisation 💼


## Project Description 📝

Collating retail data for multinational company to one centralised database. 

Through a system of classes to retrieve, clean and upload data to central database.

### Data Retrieval

Data located in AWS RDS, pdfs, Web APIs, and AWS s3. 

### Data Cleaning

Cleaning up data using pandas 

### Querying Data

Obtaining up-to-date business metrics with SQL. 

## Installation Instructions ⚙

Import the class files: 

    1. database_utils.py
    2. data_extraction.py
    3. data_cleaning.py

## Usage Instructions ⏯ 

Import class modules:

```
import database_utils
import data_extraction
import data_cleaning
```

Create instances of each class:

```
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

- [ ] input file structure


## License information 🗒

- [ ] get license info