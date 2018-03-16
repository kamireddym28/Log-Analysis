#!/usr/bin/env python3

# "Database code" for the DB News.
# Imported all essential libraries

import psycopg2
import datetime
import sys

# Name of the database

DBName = "news"

# What are the most popular three articles of all time?
'''\
CREATE OR REPLACE VIEW popular_article as
SELECT articles.slug as most_popular_articles,
COUNT(*) as views
FROM log, articles
WHERE CONCAT('/article/',articles.slug)=log.path
GROUP BY articles.slug
ORDER BY views DESC limit 3;
'''
q1 = "SELECT * FROM popular_article"

# Who are the most popular article authors of all time?
'''\
CREATE OR REPLACE VIEW popular_article_authors as
SELECT authors.name,count(*) as views
FROM authors, articles,log
WHERE articles.author=authors.id
AND CONCAT('/article/',articles.slug)=log.path
GROUP BY authors.name
ORDER BY views DESC;
'''
q2 = "SELECT * FROM popular_article_authors"

# On which days did more than 1% of requests lead to errors?
'''\
CREATE VIEW error_log as
SELECT (date(time)) as unique_date, count(*) as error
FROM log
WHERE status like '%4%'
GROUP BY unique_date
ORDER BY error DESC;

CREATE VIEW total_log as
SELECT (date(time)) as unique_date, count(*) as status
FROM log
GROUP BY unique_date
ORDER BY status DESC;

CREATE VIEW percent_error_requests as
SELECT total_log.unique_date,
ROUND((100.0/(total_log.status/error_log.error)),2) as error_percent
FROM total_log, error_log
WHERE total_log.unique_date=error_log.unique_date
GROUP BY total_log.unique_date, total_log.status, error_log.error
ORDER BY error_percent DESC;
'''
q3 = "SELECT * FROM percent_error_requests WHERE error_percent>1.0"


# Connection establishment with the database

def connection():
    try:
        conn = psycopg2.connect(database=DBName)
        cursor = conn.cursor()
        return conn, cursor
    except:
        print "Error while connecting to database"


# Function to find top three articles of all times

def popular_article(q1):
    conn, cursor = connection()
    cursor.execute(q1)
    result = cursor.fetchall()
    print "\nPart 1:\nThree most popular articles of all times are:\n"
    for i in range(0, len(result)):
        article = result[i][0]
        views = result[i][1]
        print i+1, ')', '"', article, '"', '---->', views, "views"
    conn.close()


# Function to find the popular authors of all times

def popular_authors(q2):
    conn, cursor = connection()
    cursor.execute(q2)
    result = cursor.fetchall()
    print "\nPart 2:\nMost popular authors of all times are:\n"
    for i in range(0, len(result)):
        author = result[i][0]
        views = result[i][1]
        print i+1, ')', author, '---->', views, "views"
    conn.close()


# Function to find the days with >1% requests lead to errors

def error_percent(q3):
    conn, cursor = connection()
    cursor.execute(q3)
    result = cursor.fetchall()
    print "\nPart 3:\nDays with more than 1% of requests lead to errors :\n"
    for i in range(0, len(result)):
        date = result[i][0]
        percent = result[i][1]
        print 'On', date, 'with', percent, "%"
    conn.close()


# Function to write the output of newsdatadb.py to results.txt

def returning_output():
    sys.stdout = open("results.txt", "w")
    total_questions = 3
    for i in range(0, total_questions):
        if i == 0:
            popular_article(q1)
        elif i == 1:
            popular_authors(q2)
        else:
            error_percent(q3)
    sys.stdout.close()
if __name__ == '__main__':
    returning_output()
