[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)

# Concept

Parsers extract data from sources (static files or other APIs) to upload them to database. 

# Output data structure

Parsing result is a list of dictionaries. Each dictionary represents one observation in time for a variable (datapoint).
Datapoint dictionary has `date`, `freq`, `name` and `value` keys. Same data structure is used to upload data to database.

Example:

```python 
 {'date': '2017-09-26', 
  'freq': 'd', 
  'name': 'USDRUR_CB', 
  'value': Decimal(57.566)},
```

# Individual parsers



| Class | Description | Frequency | Start date |
| ----- | ----------- | --------- | ---------- |
| KEP_Annual | Annual data from KEP publication (Rosstat) | a | 1999-01-01 |
| KEP_Qtr | Quarterly data from KEP publication (Rosstat) | q | 1999-01-01 |
| KEP_Monthly | Monthly data from KEP publication (Rosstat) | m | 1999-01-01 |
| Brent | Brent oil price (EIA) | d | 1987-05-20 |
| USDRUR | Official USD/RUR exchange rate (Bank of Russia) | d | 1992-07-01 |
| UST | US Treasuries interest rates (UST) | d | 1990-01-01 |

Use ```dataset.ReadmeTable()``` to update. 


#### Parser construction

Each parser is a child of `parsers.getter.base.ParserBase` class.

Each parser has itw own:
- observation start date (class attribute)
- frequency (class attribute) 
- url constructor (property)
- response parsing function (staticmethod)

Parsers are stored in `parsers.getter` folder.

#### Arguments

Creating a parser without arguments forces parser to scan full dataset, 
and it is a burden on the original sources. 

Parsers can return 
datapoints from a specific date to present: 

```python
from parsers.getter.cbr_fx import USDRUR
parser = CBR_USD(start_date='2017-09-01')
```

or for a fixed period in time:

```python
from parsers.getter.brent import Brent
parser = Brent('2017-09-15', '2017-10-17')
```

# Running  

Run individual parser:

```python
from parsers.getter import KEP_Annual

parser = KEP_Annual()
parser.extract()
parser.upload()
```

```Dataset``` class used to manipulate a group of parsers.

```python
from parser import Dataset
from parsers import PARSERS

d = Dataset(start_date, end_date) 
d.extract()
d.upload()
d.save_json(filename)
```
   
                          
TODO
====

#### repo: rosstat-806-regional
<https://github.com/epogrebnyak/data-rosstat-806-regional>

#### repo: data-rosstat-isep
<https://github.com/mini-kep/data-rosstat-isep>


Glossary
========

Types of parsers:

**heavy** - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

**thin** (*'clean'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is clean. These parsers usually do not require disk space to store intermeduate parsing result. 
