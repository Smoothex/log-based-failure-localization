import os
import subprocess

"""
CASSANDRA-16577
https://issues.apache.org/jira/browse/CASSANDRA-16577
"""

"WARNING: You need Java 8 JDK 8u321 for this test case! JDK 8u331 does not work!"

version = '3.11.10'  # 3.11.11 - normal execution / 3.11.10 - gives error
execution = 'failure'  # normal / failure

# DON'T FORGET TO STOP THE NORMAL CLUSTER AFTER RUNNING THE SCRIPT WITH IT SO THAT THE PORTS ARE FREE FOR THE NEXT ONE

# Start the container
os.system('ccm create 16577_'+execution+' --vnodes -n 3 -s -v '+version)

# Remove two nodes
os.system('ccm node2 decommission')
os.system('ccm node3 decommission')
os.system('ccm node2 remove')
os.system('ccm node3 remove')

# Create a keyspace
cmd = "ccm node1 cqlsh -x \"CREATE KEYSPACE k WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\': 1};\""
subprocess.run(cmd, shell=True)

# Invoke a new assignment of tokens (since 2 nodes left the ring)
allocate = "ccm updateconf \'allocate_tokens_for_keyspace: k\'"
subprocess.run(allocate, shell=True)

# Add node2 again to cluster
os.system('ccm add node2 -i 127.0.0.2 -j 7200 -r 2200')
os.system('ccm node2 start')

# Stop the cluster
os.system("ccm stop")
