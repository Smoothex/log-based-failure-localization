import os
import docker
from cassandra.cluster import Cluster
import time

"""
CASSANDRA-14989
https://issues.apache.org/jira/browse/CASSANDRA-14989
"""

user = os.getenv("USER", default=None)
version = '4.0'     # normal in 4.0 / bug in 3.11.14
execution = 'normal'  # normal / failure
container_name = 'cassandra' + version + '_' + execution

client = docker.from_env()

# Pull the image - if it throws an error, navigate to ~/.docker/config.json and change credsStore to credStore
# https://stackoverflow.com/questions/67642620/docker-credential-desktop-not-installed-or-not-available-in-path
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
# You might want to increase this time if you're getting a timeout error
time.sleep(15)

# Connect to the cluster inside the docker container
"""
Observation: the connection to the cluster is flaky. Sometimes it returns a timeout error, sometimes a
             "Connection reset by peers" error. Upon multiple tries to connect, it finally does - I am unsure whether
             the cluster needs more time to get fully initialized or something else. Worst case, you can create the
             cluster (manually or with the code above), then comment out lines 16-34 and rerun the rest of the script
             multiple times until a connection is established successfully.
"""
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

time.sleep(120)

# Write the Cassandra container logs to a file locally
os.system('docker logs '+cassandra_container.name+' > /home/'+user+'/Desktop/14989_'+execution+'.log 2>&1')
