import os
import subprocess
from cassandra.cluster import Cluster

"""
CASSANDRA-13337
https://issues.apache.org/jira/browse/CASSANDRA-13337
"""

version = '3.0.12'  # 3.0.13 - normal execution / 3.0.12 - gives error
execution = 'normal'  # alternatively 'failure'

# Start the container
os.system('ccm create 13337_' + execution + ' -v ' + version + ' -n 1 -s')

# Connect to the cluster and specifically to the first (and in this case only) node
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create a keyspace
session.execute("CREATE KEYSPACE k WITH REPLICATION = {\'class\': \'SimpleStrategy\', \'replication_factor\': 1};")

# Create a table
session.execute("CREATE TABLE k.test (key1 int, key2 int, entry1 int, entry2 int, entry3 int, entry4 int, entry5 int,"
                "PRIMARY KEY(key1, key2));")

# Make some changes to the table
session.execute("UPDATE k.test SET entry2 = 1, entry3 = 3, entry4 = 4 WHERE key1 = 1 AND key2 = 0;")

session.execute("ALTER TABLE k.test DROP entry2;")
session.execute("ALTER TABLE k.test DROP entry3;")
session.execute("ALTER TABLE k.test DROP entry4;")
session.execute("SELECT * FROM k.test;")

# Stop the cluster
os.system("ccm stop")
