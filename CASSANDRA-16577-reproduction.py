import os
import subprocess

"""
CASSANDRA-16577
https://issues.apache.org/jira/browse/CASSANDRA-16577
"""

# 3.11.11 - normal execution
# os.system('ccm create 16577_normal --vnodes -n 3 -s -v 3.11.11')

# DON'T FORGET TO STOP THE NORMAL CLUSTER AFTER RUNNING THE SCRIPT WITH IT SO THAT THE PORTS ARE FREE FOR THE NEXT ONE

# 3.11.10 - gives error
os.system('ccm create 16577_failure --vnodes -n 3 -s -v 3.11.10')

# Remove two nodes
os.system('ccm node2 decommission')
os.system('ccm node3 decommission')
os.system('ccm node2 remove')
os.system('ccm node3 remove')

# Create keyspace to change the schema. It works if the schema never changes.
cmd = "ccm node1 cqlsh -x \"CREATE KEYSPACE k WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\': 1};\""
subprocess.run(cmd, shell=True)

# Add allocate parameter
allocate = "ccm updateconf \'allocate_tokens_for_keyspace: k\'"
subprocess.run(allocate, shell=True)

# Add node2 again to cluster
os.system('ccm add node2 -i 127.0.0.2 -j 7200 -r 2200')
os.system('ccm node2 start')
