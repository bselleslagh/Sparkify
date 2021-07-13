import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender char,
    itemInSession int,
    lastName varchar,
    length varchar,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration bigint,
    sessionId int,
    song varchar,
    status int,
    ts varchar,
    userAgent varchar,
    userId int )
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id varchar,
    artist_latitude float,
    artist_location varchar,
    artist_longitude float,
    artist_name varchar,
    duration float,
    num_songs int,
    song_id varchar,
    title varchar,
    year int)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id BIGINT IDENTITY(0,1) not null,
    start_time timestamp,
    user_id int,
    level varchar,
    song_id varchar,
    artist_id varchar,
    session_id int,
    location varchar,
    user_agent varchar,
    primary key(songplay_id))
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int not null,
    first_name varchar,
    last_name varchar,
    gender char(1),
    level varchar,
    primary key(user_id))
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song (
    song_id varchar not null,
    title varchar not null,
    artist_id varchar not null,
    year int,
    duration float,
    primary key(song_id))
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artist (
    artist_id varchar not null,
    name varchar not null,
    location varchar,
    latitude real,
    longtitude real,
    primary key(artist_id))
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time timestamp not null,
    hour int not null,
    day int not null,
    week int not null,
    month int not null,
    year int not null,
    weekday int not null,
    primary key(start_time))
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    iam_role {}
    format as json {}
    region 'us-west-2';
""".format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], \
    config['S3']['LOG_JSONPATH']))
                       
staging_songs_copy = ("""
    copy staging_songs from {}
    iam_role {}
    json 'auto ignorecase'
    region 'us-west-2';
""".format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN']))



# FINAL TABLES

songplay_table_insert = ("""
insert into songplays(start_time , user_id , level, song_id , artist_id , session_id , location , user_agent )
select timestamp 'epoch' +  ts/1000   * interval '1 second' AS start_time, se.userid as user_id, se.level, ss.song_id , ss.artist_id , se.sessionid , se.location , se.useragent 
from staging_events se 
left join staging_songs ss on se.artist = ss.artist_name and se.song = ss.title 
where se.page = 'NextSong'
""")

user_table_insert = ("""
insert into users 
select distinct userid , firstname as first_name, lastname as last_name, gender , "level" 
from staging_events se 
where se.auth = 'Logged In' AND se.page = 'NextSong'
""")

song_table_insert = ("""
insert  into song 
select distinct song_id , title , artist_id , "year" , duration 
from staging_songs ss 
""")

artist_table_insert = ("""
insert into artist
select distinct artist_id , artist_name as name, artist_location as location, artist_latitude as latitude, artist_longitude  as longtitude
from staging_songs ss 
""")

time_table_insert = ("""
insert into time
select distinct start_time, 
extract(hour from start_time) as hour, 
extract(day from start_time) as day, 
extract(week from start_time) as week, 
extract(month from start_time) as month,
extract(year from start_time) as year,
extract(weekday from start_time) as weekday
from songplays 
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
