# File Ingestion Pattern

## Usage

```shell
usage: ingestion.py [-h] [-s SRCE_NM | --all] [--adhoc] [--fetch] [--debug]
                    [--silence]
                    CODE_APPL

positional arguments:
  CODE_APPL             CODE_APPL (Source Short Name)

optional arguments:
  -h, --help            show this help message and exit
  -s SRCE_NM, --srce_nm SRCE_NM
                        SRCE_NM (Source Name)
  --all                 Activates complete source load
  --adhoc               Ingests files in dataDropArea, matches on regex
  --fetch               Fetch files to process
  --debug               Increases verbosity in log file
  --silence             Turns off verbose
```

## Installation

Make sure the appropriate folders are created based on the `config.ini` file
provided in this repository. If not, modify it in a feature branch and follow
the appropriate git-flow. You will also need to create the `credentials.ini`
file for sensitive information. Here's the desired layout:

```ini
# INI FILE THAT CONTAINS CREDENTIALS FOR THE DATAHUB/SNOWFLAKE APPLICATIONS
# For new development, add the required section if it does not already exist
# Otherwise you can grab the values from an existing section
[MYSQL-CTRL]
USER = user_name
HOST = host_ip
PWD  = mysql_password

[SNOWFLAKE-EDH-INGEST]
USER = snowflake_user
PWD  = snowflake_password
ACCOUNT = snowflake_account

[AZURE-RAW]
ACCOUNT_NAME = azure_account_name
ACCOUNT_KEY = azure_account_key
```

*__Additional Steps for installation__*

Those steps should be ran before executing the application.

### Automatic Deploy

After filling the configs, run the installer located at:
`./bin/install.py`

### Manual Install

__Snowflake:__

```sql
CREATE SCHEMA RAW.STG_LOADING;
USE RAW.STG_LOADING;

CREATE FILE FORMAT file_standard
  TYPE = CSV
  FIELD_DELIMITER = ','
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE STAGE STG_LOADING.FILE_LOADING
  FILE_FORMAT = (FORMAT_NAME='file_standard')
  URL = 'azure://<account>.blob.core.windows.net/<container>[/<path>/]'
  [ CREDENTIALS = ( [ AZURE_SAS_TOKEN = <string> ] ) ]
  [ ENCRYPTION = ( [TYPE = { AZURE_CSE | NONE } ] [ MASTER_KEY = '<string>' ] ) ];
```

__MySQL Control Tables:__

To deploy control tables, run the create table ddls located in:
`./ingestion/tests/integration/data/sql/ddl/mysql_control_tables.sql`

__Folder Structure:__

You also need to create the proper folder structure. First decided on a `base path`
you wish to deploy the application into (for the Data Flow). Let's assume ours is
located at `/data_fs/dataingestion`:

```shell
mkdir -p /data_fs/dataingestion
mkdir -p /data_fs/dataingestion/data/archive
mkdir -p /data_fs/dataingestion/ingestion/dataDropArea
mkdir -p /data_fs/dataingestion/ingestion/TEMP_BACKUP
mkdir -p /data_fs/dataingestion/ingestion/workarea
```

## Detailed Description

### Flow Diagrams

![Alt text](docs/img/ingestion.png?raw=true "ingestion.py")

### Control Tables

#### INGEST_PARAM

This is the table where you input parameters for a desired file ingestion.

| Field             | Type         | Default | Comments |
| ---               | ---          | ---     | ---   |
| CODE_APPL         | varchar(50)  | NULL    | Source's CODE_APPL |
| SRCE_TYP          | varchar(20)  | NULL    | Source's type |
| SRCE_NM           | varchar(100) | NULL    | Source's file name without date of extension |
| SRCE_SUB_TYP      | varchar(20)  | NULL    | Source's sub type, like CSV, FWF, TXT |
| DEL_CHAR          | varchar(15)  | NULL    | Delimiter character in plain text: ; or , or /| or TAB or NAK |
| TRGT_TBL_NM       | varchar(100) | N/A     | Target table name |
| PART_TYP          | char(1)      | NULL    | Partition type: Either 'F' for FULL or 'P' for Partitioned |
| PART_FLAG         | char(1)      | N       | Partitioned or not: Y or N|
| PART_FREQNCY      | varchar(5)   | N/A     | Partition frequency: DAY or MONTH or YEAR |
| SRCE_COMPRSSN_TYP | varchar(10)  | NULL    | Source compression type: GZIP, ZIP |
| HEADER_LN         | tinyint(4)   | NULL    | Number of header line |
| FOOTER_LN         | tinyint(4)   | NULL    | Number of footer line |
| NMBR_COLMNS       | smallint(6)  | NULL    | Number of columns |
| COL_HDR_FLAG      | char(1)      | NULL    | Are there column names: Y or N |
| FILE_REGEX        | varchar(100) | N/A     | File's pick up regular expression |
| COPYBOOK_NM       | varchar(100) | N/A     | Copybook name if needed (FWF) otherwise N/A |
| PARSING_SCRIPT    | varchar(50)  | N/A     | Parsing Script if needed, otherwise N/A |

#### INGEST_CTRL

This is the table where you can monitor the execution of the different files.

| Field               | Type                | Null | Default             | Comments |
| ---                 | ---                 | ---  | ---                 | ---  |
| CODE_APPL           | varchar(50)         | YES  | NULL                |       |
| SRCE_TYP            | varchar(20)         | YES  | FILE                |       |
| SRCE_NM             | varchar(100)        | YES  | NULL                |       |
| FILE_OCCU_NM        | varchar(100)        | YES  | NULL                | Last ingested file name |
| ACTIVE_IND          | char(1)             | YES  | Y                   | Activation indicator |
| RUN_STATUS          | varchar(4)          | NO   | OK                  | Either OK, ABND or RUN |
| LAST_SUCCESSFUL_RUN | timestamp           | NO   | 2000-01-01 00:00:00 |       |
| LAST_RUN_START_TMSP | timestamp           | NO   | 2000-01-01 00:00:00 |       |
| LAST_RUN_STOP_TMSP  | timestamp           | NO   | 2000-01-01 00:00:00 |       |
| INFO                | varchar(100)        | YES  | NULL                |       |
| LOG_FILE            | varchar(100)        | YES  | NULL                |       |
| FILE_DATE           | timestamp           | NO   | 2000-01-01 00:00:00 |       |
| FILE_SIZE           | bigint(20) unsigned | YES  | NULL                |       |
| MD5_VALUE           | varchar(32)         | YES  | NULL                |       |
| NB_LINES            | int(10) unsigned    | YES  | NULL                |       |

#### INGEST_CTRL_LOG

This table is the same as ``INGEST_CTRL``, but it also has a ``LOG_ID`` column which is
automatically incremented for logging purposes.

## Developers

### Write a Custom Exception Module

1. Create a new python script under `./lib/ingestion/exception_modules`

2. Use template for ONE-TO-ONE exception modules:

    > `./lib/ingestion/exception_modules/template_one-to-one.py`

3. Use this template for ONE-TO-MANY exception modules:

    > `./lib/ingestion/exception_modules/template_one-to-many.py`

4. Add the script name in the control table's `PARSING_SCRIPT` column.

5. Don't forget to add the integration test for that new script.

## Notes
