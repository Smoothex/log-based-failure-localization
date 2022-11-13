import os
import docker
from cassandra.cluster import Cluster
import time

"""
CASSANDRA-14989
https://issues.apache.org/jira/browse/CASSANDRA-14989
"""

user = os.getenv("USER", default=None)
version = '3.11.3'     # fixed in 4.0
execution = 'failure'  # normal / failure
container_name = 'cassandra' + version + '_' + execution

client = docker.from_env()

# Pull the image
images = client.images.pull('cassandra', tag=version)

# Run the Cassandra container and expose its port 9042 to the host's port 9042
cassandra_container = client.containers.run(image='cassandra:' + version,
                                            name='14989_' + execution,
                                            ports={'9042/tcp': ('127.0.0.1', 9042)},
                                            detach=True)

print("Container created")
print("Container name: " + cassandra_container.name)
print("Container ID: " + cassandra_container.short_id)

# Give the container some time to get fully initialized
time.sleep(15)

# Connect to the cluster inside the docker container
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()
print("Connected to container! Session ID: ", session.session_id)

session.execute("CREATE KEYSPACE k WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
session.execute("CREATE TABLE k.reproduction ("
                "pk1 uuid, "
                "pk2 text, "
                "PRIMARY KEY ((pk1, pk2)));")   # this is a two-part primary key
session.execute("INSERT INTO "
                "k.reproduction(pk1,pk2) "
                "VALUES (uuid(),\'pk2\');")
try:
    session.execute("SELECT TOKEN(pk1) FROM k.reproduction")
except:
    pass

# Write the Cassandra container logs to a file locally
os.system('docker logs '+cassandra_container.name+' > /home/'+user+'/Desktop/14989_'+execution+'.log 2>&1')
