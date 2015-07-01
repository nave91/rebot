# Rebot
Rebot provides a platform to automate debugging. Typical day in developer's life looks something like [this](https://www.youtube.com/watch?v=zkrzA5LUPxI).
In order to reduce the frustrations of developer and also improve the quality of software being built, this project was bootstrapped.
This project takes the first step in automating the process of typical developer searching for solution. 
The idea is to find the right fix that solves his specific personal problem.

## Why?
Rebot provides a platform for anyone to query for feature sets that help in finding a right solution for any given error.
Since the number of softwares used currently are increasing exponentially, having an automated mechanism to provide concise viable solutions helps 
developers write awesome code and also save a lot of time. 

The primary goal of this project is not to automate debugging but give a platform for developers to build tools that automate debugging.

# Technologies
The following technologies are configured to serve as backend for this platform:

* [Hadoop HDFS](http://hadoop.apache.org/)
* [Spark](https://spark.apache.org/)
* [Elasticsearch](https://www.elastic.co/)
* [Kafka](http://kafka.apache.org/)
* [Flume](https://flume.apache.org/)

## Dependencies
Service depends on following packages of python

* [Flask](http://flask.pocoo.org/)
* [WTForms](https://wtforms.readthedocs.org/en/latest/)
* [Restful](https://flask-restful.readthedocs.org/en/0.3.3/)
* [Pyes](https://elasticsearch-py.readthedocs.org/en/master/)

# Architecture

![](https://github.com/nave91/rebot/blob/gh-pages/img/Picture8.png)

# Demo and User search
The following instances are the courtesy of https://insightdataengineering.com/ and will be eventually taken down.
All the important configurations are stored in this repository for future use.

* [Search](http://rebot.link/search)
* [Demo](http://rebot.link/demo)

# Explanation
Please checkout the [presentation](https://nave91.github.io/rebot)

# Data
Courtesy of stackexchange and archive.com. For the demo 32GB of data was used. Which replicated to be around 60GB in Elasticsearch.

* [archive](https://archive.org/details/stackexchange)
