# Sparkify ETL pipeline
## Context
The scope of this ETL pipeline is to process log and song data provided by Sparkify and store in AWS Redshift for further analytics. The resulting tables will enable the analytics team to gather insights about the listing behaviour of the users.

This pipeline consists out of two main steps:
- Read both the log and song data provided as JSON files stored in S3 and write this log data to two staging tables.
- Transform the staged data into a star schema for further analytics.



### Using the ETL pipeline

Requirements:

- An AWS Account with Redshift and S3 access
- Python 3.7 or greater
- Python packages [psycopg2](https://pypi.org/project/psycopg2/) and [configparser](https://docs.python.org/3/library/configparser.html)

Steps:

1. **Enter your AWS Redshift connection details into the dwh.cfg file.** So that the script can connect to the database.
2. **Run the create_tables.py script** to create the staging tables and the five fact and dimension tables
3. **Run etl.py** to load the source data from S3 into the staging tables and then transform to to the five fact/dimension tables. 

### ERD of the fact and dimension tables

Using an ETL script, we will transform the staged data into a star schema for further analytics.  The schema contains the following fact and dimension tables:

![Star schema ERD](Sparkify_ERD.png?raw=true "Sparkify ERD")


### Included files

#### create_tables.py

This is the first script that should be run, it will create the staging and fact.dimension tables on AWS Redshift.

#### etl.py

- This script will first load all data from S3 into both staging tables STAGING_EVENTS & STAGING_SONGS
- After this the script will transform the staging data into songplays (fact), user (dimension), artist (dimension), song (dimension) and time (dimension) tables.
- Only the logs where the page is equal to 'NextSong' will be copied to the fact and dimension tables.

#### sql_queries.py

This Python script contains all the SQL queries that will be executed on AWS Redshift, this script is invoked by create_tables.py and etl.py

#### dwh.cfg

This is a configuration file containing all the variables to connect to S3 and Redshift:

- Redshift hostname
- Database name and port
- User & password
- IAM Role ARN for connecting to S3
- S3 links to log and song data

## Example queries:

This section will provide some example queries than can be run on the star schema:

```SQL
-- Count the amount of songs played by paid and free users for a given day
select s.level, count(*)
from songplays s
join time t on s.start_time = t.start_time
where t.year = 2018 and t.month = 11 and t.day = 2
group by s.level
```

```SQL
-- Display a list of unique songs played by a user
select distinct b.title, c.name
from songplays a
left join song b on a.song_id = b.song_id
join artist c on b.artist_id = c.artist_id
where user_id = 44
```

```SQL
-- Amount of artists in the song database
select count(*)
from artist
```

```sql
-- Amount of songs in the song database
select count(*)
from song
```

```SQL
-- Top 3 most streamed artists
select a.name, count(*) as number_of_plays
from songplays s
join artist a on s.artist_id = s.artist_id
group by a.name
order by 2 desc
limit 3
```







