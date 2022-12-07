# Log-based failure localization in distributed systems - A Case Study for Apache Cassandra

This work proposes a workflow for processing log files, which helps identify errors and presents a clear difference between correct and incorrect execution.

![image](https://user-images.githubusercontent.com/79105432/206227999-cfaea3c6-b9f8-4851-ac9b-9777facf5d82.png)

The proposed overview includes:
* generation of the log files (using the Python reproduction scripts)
* parsing the log files (using `templater.py`)
* extracting the differences between the parsed log files (using `difference.py`)

## Prerequisites
* For CASSANDRA-14989 and CASSANDRA-11803: [Docker](https://docs.docker.com/get-docker/)
* For the rest of the reproduction scripts: [Cassandra Cluster Manager (CCM)](https://github.com/riptano/ccm) (and its dependencies)
* [DataStax Python Driver](https://docs.datastax.com/en/developer/python-driver/3.18/): `pip install cassandra-driver`
* It is advised to execute the scripts on a Linux system, since CCM has some known bugs on Windows

## Execution
The scripts are to be executed separately by simply running the specific file. The program should terminate with exit code `0` and the log files are generated in `/home/<USER>/.ccm/<CLUSTER_NAME>/<NODE_NAME>/logs/`, where NODE_NAME is by default node1, node2, etc. For this work, the important file is `debug.log`.

The `debug.log` can then be copied to a desktop folder named `13346_failure` or `13346_normal` (or the numbers of the other bugs). The copy of `debug.log` is then ingested into `templater.py`.

The parsed log file then goes through `difference.py`, which generates an output file consisting of the different log entries.
