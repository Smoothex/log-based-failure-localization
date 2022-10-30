import os
import docker
from cassandra.cluster import Cluster
import time

"""
CASSANDRA-11803
https://issues.apache.org/jira/browse/CASSANDRA-11803
"""

version = '3.3'
execution = 'failure'  # alternatively 'failure'
container_name = 'cassandra' + version + '_' + execution

# Run a Cassandra container and expose its port 9042 to the host's port 9042
client = docker.from_env()
cassandra_container = client.containers.run(image='cassandra:' + version,
                                            name='cassandra' + version + '_' + execution,
                                            ports={'9042/tcp': ('127.0.0.1', 9042)},
                                            detach=True)

print("Container created")
print("Container name: " + cassandra_container.name)
print("Container ID: " + cassandra_container.id)

# Give the container some time to get fully initialized
time.sleep(15)

# Connect to the cluster inside the docker container
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()
print("Connected to container! Session ID: ", session.session_id)

# Reproduce the error
session.execute("CREATE KEYSPACE account WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
session.execute("CREATE TABLE account.session ("
                "\"token\" blob, "
                "account_id uuid,"
                "PRIMARY KEY(\"token\")"
                ")WITH compaction={'class': 'LeveledCompactionStrategy'} "
                "AND compression={'sstable_compression': 'LZ4Compressor'};")

# Here is where the error occurs. Use try-except to bypass it, so that it doesn't crash the execution
try:
    session.execute("CREATE MATERIALIZED VIEW account.account_session AS "
                    "SELECT account_id,\"token\" FROM account.session "
                    "WHERE \"token\" IS NOT NULL and account_id IS NOT NULL "
                    "PRIMARY KEY (account_id, \"token\");")
except:
    pass

# Write the Cassandra container logs to a file locally
os.system('docker logs cassandra3.3_failure > /home/smoothex/Desktop/11803_failure.logs 2>&1')
