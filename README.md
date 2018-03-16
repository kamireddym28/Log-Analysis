# Log Analysis Project -- FSDN Project3

 > The objective of this project is to analyze and query "News" database inorder to generate log results.

## Requirements

 - [**Python 2.7** or **Python 3.6**](https://www.python.org/downloads/)
 - [**Vagrant**](https://www.vagrantup.com/)
 - [**VirtualBox**](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Usage

 - Install either of the python versions from the URL provided
 - Install the VirtualMachine(VM) to run an SQL database server using the tools provided*
 - [Download](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91) the database and unzip it
 - Place the unziped file (newsdata.sql) in vagrant folder on local computer
 - Bring the VM online 
 - Load the database by ``` cd ``` into the ``` vagrant ``` directory
 - Set the path to the newsdata.sql inside the vagrant directory  
 - Execute the ***newsdatadb.py*** file using ``` python newsdatadb.py ```
 - Log results can be found in ***results.txt*** on succesful execution .py file
 - Use ``` CTRL+D ``` to exit the VM

## Description of files

 - ***newsdatadb.py***     : Code to analyze and generate log results on "News" DB. 
 - ***results.txt*** 	: Output file to which analyzed log results are written 
 - ***newsdata.sql*** 	: News DB containing "articles" , "authors"  and "log" tables
			     
## Commands 

 - Bring the VM online using ``` vagrant up ``` 
 - Log into VM using ``` vagrant ssh ```
 - Load the database using ``` psql -d news -f newsdata.sql ```
 - ``` import psycopg2 ``` is a module to connect to *** PostgreSQL *** , an open source RDBMS  

 ### VIEWS Created**
 - Part 1: 
 ``` 
	CREATE OR REPLACE VIEW popular_article as
	SELECT articles.slug as most_popular_articles, COUNT(*) as views
    FROM log, articles
    WHERE CONCAT('/article/',articles.slug)=log.path
    GROUP BY articles.slug
    ORDER BY views DESC limit 3;
 ```
 
 - Part 2:
 ```
	CREATE OR REPLACE VIEW popular_article_authors as
	SELECT authors.name,count(*) as views
	FROM authors, articles,log
	WHERE articles.author=authors.id
	AND CONCAT('/article/',articles.slug)=log.path
	GROUP BY authors.name
	ORDER BY views DESC;
 ```
 
 - Part 3:
 ```
	CREATE OR REPLACE VIEW error_log as
	SELECT (date(time)) as unique_date, count(*) as error
	FROM log
	WHERE status like '%4%'
	GROUP BY unique_date
	ORDER BY error DESC;

	CREATE OR REPLACE VIEW total_log as
	SELECT (date(time)) as unique_date, count(*) as status
	FROM log
	GROUP BY unique_date
	ORDER BY status DESC;

	CREATE OR REPLACE VIEW percent_error_requests as
	SELECT total_log.unique_date,
	ROUND((100.0/(total_log.status/error_log.error)),2) as error_percent
	FROM total_log, error_log
	WHERE total_log.unique_date=error_log.unique_date
	GROUP BY total_log.unique_date, total_log.status, error_log.error
	ORDER BY error_percent DESC;
 ```
 
## Courtesy

 News database (newsdata.sql) was provided by Udacity

 #### Note:
 
 Vagrant and VirtualBox are the tools to install and manage the VM*
 
 Reference "newsdatadb.py" to find the usage of the created VIEWs**
