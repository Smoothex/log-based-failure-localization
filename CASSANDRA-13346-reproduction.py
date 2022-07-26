import os
from cassandra.cluster import Cluster

"""
CASSANDRA-13346
https://issues.apache.org/jira/browse/CASSANDRA-13346
"""

version = '3.11.0'    # 3.11.0 - normal execution / 3.9 - gives error
execution = 'normal'  # normal / failure

# DON'T FORGET TO STOP THE NORMAL CLUSTER AFTER RUNNING THE SCRIPT WITH IT SO THAT THE PORTS ARE FREE FOR THE NEXT ONE

# Create a cluster called 13346_normal / 13346_failure and populate it with 1 node
os.system('ccm create 13346_'+execution+' -n 1 -v '+version+' -s')

# Connect to the cluster and specifically to the first (and in this case only) node
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create a keyspace (which will be dropped afterwards)
session.execute("CREATE KEYSPACE k WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor': 1 };")

# Create a table
session.execute("CREATE TABLE k.tableTest ("
                "entry1 int,"
                "entry2 text,"
                "entry3 text,"
                "PRIMARY KEY (entry1, entry2)"
                ");")

# Create materialized view
session.execute("CREATE MATERIALIZED VIEW k.materializedview AS "
                "SELECT entry1, entry2, entry3 FROM k.tableTest WHERE "
                "entry1 IS NOT NULL AND entry2 IS NOT NULL AND entry3 IS NOT NULL "
                "PRIMARY KEY (entry1, entry2, entry3);")

# Fill up the table
session.execute("INSERT INTO k.tableTest (entry1, entry2, entry3) VALUES (1, 'congrats', 'you');")
session.execute("INSERT INTO k.tableTest (entry1, entry2, entry3) VALUES (2, 'found', 'an');")
session.execute("INSERT INTO k.tableTest (entry1, entry2, entry3) VALUES (2, 'easter', 'egg');")

# Drop the keyspace
session.execute("DROP KEYSPACE k;")

# Stop the cluster
os.system("ccm stop")
