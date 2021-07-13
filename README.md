# Sparkify ETL pipeline
## Context
The scope of this ETL pipeline is to process log and song data provided by Sparkify and store in AWS Redshift for further analytics. The resulting tables will enable the analytics team to gather insights about the listing behaviour of the users.

This pipeline consists out of two main steps:
- Read both the log and song data provided as JSON files stored in S3 and write this log data to two staging tables.
- Transform the staged data into a star schema for further analytics.

## Reading the log data from S3
First, we will connect to S3 to read the data provided by Sparkify. This consist out of both the log and song data stored as JSON files. We will save this information in 2 staging tables: STAGING_EVENTS & STAGING_SONGS

## Transform the data into a star-schema
Using an ETL script, we will transform the staged data into a star schema for further analytics.  The schema contains the following fact and dimension tables:
-- IMAGE -- 

# Example queries
This section will provide some example queries than can be run on the star schema:






