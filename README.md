# Death-App

## Introduction 
The Death app was created to analyze data and present the results visually. Data analysis relates to the most common 
causes of death in countries and different levels of development over the years. You can select the type of analysis and then enter the required input data. As a result, you will receive a graph containing the relevant analysis. You will be able to download each visualization. Application enables you to add your own data.  

## Requirements
To launch application you need to do [poetry installation](https://python-poetry.org/docs/#installation). 
To install the defined dependencies for this project, run command below.

```commandline
poetry install 
```
## Data 

### Used datasets 

To run this application you can use datasets stored on Google Drive. In the initial implementation, the following 
datasets were used:
1. Death dataset, downloaded from [the Our World in Data website][deaths-link] - `annual-number-of-deaths-by-causes.csv` 
2. Populations dataset, which contains information on populations by year in countries,
downloaded from [the World Bank website][populations-link] - `population_since_1990.csv`
3. HDI countries dataset, which contains data on Human Development Index values by countries
and years, downloaded from [the Our World in Data website][hdi-link] - `human-development-index.csv`

To download datasets you have to run command below.

```commandline
poe download
```
#### Preprocessing downloaded data to application 
After downloading three datasets, you have to preprocess them. Command below prepares new four datasets:
* preprocessed death dataset - `death_by_country.csv`, 
* preprocessed population dataset - `population_by_country.csv`,
* preprocessed hdi dataset - `index_mean_by_country.csv`,
* final dataset `input_dataset.csv` which contains information 
about death causes and population in each country during specific range of years. 

All datasets will be stored in the following folder structure `res/data`. 

To preprocess downloaded datasets you have to run command below. 

```commandline
poe all_preprocess
```
### Your own datasets 
Application also allows you to add your own data. You can choose two options: 
1. Adding only new death causes data with structure like in `annual-number-of-deaths-by-cause.csv` 
2. Adding two new datasets: death causes dataset and development index dataset   

#### First option 
If you have death dataset with structure like dataset downloaded from [the Our World in Data website][deaths-link], 
you have to put it in the following folder structure `res/data/raw` with name `annual-number-of-deaths-by-cause.csv`. If you don't have these 
folders you need to create them in project's root directory. Command below downloads two missing datasets:
* `human-development-index.csv` from Google Drive  
* `population_by_country.csv` from World Bank Dataset API in defined range of years from death dataset

First dataset will be saved in `res/data/raw` and the second one in `res/data`.

To download two missing datasets you have to run command below.

```commandline
poe download_missing
```
#### Preprocessing datasets to application 
To preprocess your death dataset and human development index dataset you have to run command below.

```commandline
poe preprocess
```
 
This command prepares new three datasets which will be stored in the following folder structure `res/data`:
* preprocessed death dataset - `death_by_country.csv`,
* preprocessed hdi dataset - `index_mean_by_country.csv` 
* final dataset `input_dataset.csv` which contains information 
about death causes and population in each country during specific range of years. 

#### Second option 
You have to prepare two datasets with specific requirements. You have to put them in the following folder structure `res/data/raw` 
with names `death_dataset.csv` and `index_dataset.csv`. If you don't have these folders you need to create them in 
project's root directory. 

**Death dataset requirements** 

| Columns Name        | Type and requirements                                             |
|---------------------|-------------------------------------------------------------------|
| country             | string, countries name                                            |
| code                | string, countries code                                            |
| year                | integer,  year by year;                                           |
| population          | float, 0 >=,  in thousands                                        |
| d: cause of death 1 | float, 0 >=, in thousands, name of cause have to start with 'd: ' |
| d: cause of death 2 | float, 0 >=, in thousands, name of cause have to start with 'd: ' |
| ...                 | float, 0 >=, in thousands, name of cause have to start with 'd: ' |
| d: cause of death N | float, 0 >=, in thousands, name of cause have to start with 'd: ' |

_Dataset must contain at least one column with cause of death._

**Index dataset requirements** 

| Columns Name | Type and requirements                                                    |
|--------------|--------------------------------------------------------------------------|
| country      | string, countries name                                                   |
| code         | string, countries code, at least one country code like in death dataset  |
| hdi          | float,  human development index                                          |
| development  | string, level of development                                             |

_Dataset must contain at least one row._

To check your data and make this application use it you have to run command below.   

```commandline
poe check 
```
* If your datasets is correct you will see a message  _New datasets are correct_ and application will use your 
datasets. So you can move to the section Run application. 
* If your datasets isn't correct you will see a message with error. You have to change your datasets and try again. 

## Run application 
To run application you have to execute command below.  

```commandline
streamlit run main.py 
```

[deaths-link]: https://ourworldindata.org/grapher/annual-number-of-deaths-by-cause
[populations-link]: https://data.worldbank.org/indicator/SP.POP.TOTL?end=2020&start=2005
[hdi-link]: https://ourworldindata.org/human-development-index
