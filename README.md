# Log-based failure localization in distributed systems - A Case Study for Apache Cassandra

This work proposes a workflow for processing log files, which helps identify errors and presents a clear difference between correct and incorrect execution.

![image](https://user-images.githubusercontent.com/79105432/206227999-cfaea3c6-b9f8-4851-ac9b-9777facf5d82.png)

The proposed overview includes:
* generation of the log files (using the Python reproduction scripts)
* parsing the log files (using `templater.py`)
* extracting the differences between the parsed log files (using `comparer.py`)

## Prerequisites
* For CASSANDRA-14989 and CASSANDRA-11803: [Docker](https://docs.docker.com/get-docker/)
* For the rest of the reproduction scripts: [Cassandra Cluster Manager (CCM)](https://github.com/riptano/ccm)
* [DataStax Python Driver](https://docs.datastax.com/en/developer/python-driver/3.18/): `pip install cassandra-driver`
* It is advised to execute the scripts on a Linux system, since CCM has some known bugs on Windows

## Execution
