## Project Purpose

## Pre-steps
1. Install Astronomer CLI in order to use Airflow. Follow this [guide](https://docs.astronomer.io/astro/cli/install-cli?tab=windows#install-the-astro-cli)
2. Make sure that all is correct
```
astro version
```
3. Create a new project
```
astro dev init
```
4. Start airflow
```
astro dev start
```
5. In case you want to stop this enviroment, type the following command:
```
astro dev stop
```
6. Active your Snowflake trial account.


## Tools
1. Airflow/Astronomer
2. Snowflake
3. Python

## Instructions
1. Create a new DataBase in Snowflake.
2. Create a DataWarehouse
3. Create a new stage with the following command:
```
CREATE OR REPLACE STAGE "FOOTBALL_PROJECT"."PUBLIC".demo_stage;
```
4. Create a table
```
CREATE OR REPLACE TABLE football_leagues (
id         VARCHAR (30) NOT NULL,
equipo     VARCHAR (30) NOT NULL,
Jugados    INTEGER NOT NULL,
ganados    INTEGER NOT NULL,
empatados  INTEGER NOT NULL,
perdidos   INTEGER NOT NULL,
gf         INTEGER NOT NULL,
gc         INTEGER NOT NULL,
diff       INTEGER NOT NULL,
puntos     INTEGER NOT NULL,
liga       VARCHAR (30) NOT NULL,
created_at VARCHAR (30) NOT NULL
);
```
5. List stage
```
LIST @FOOTBALL_PROJECT.PUBLIC.DEMO_STAGE;
```
## Notebook
Working on [notebook](notebooks/notebook.ipynb) in order to understand how to obtain the data.
## DAG
