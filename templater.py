import re
import os

user = os.getenv("USER", default=None)
bug_number = '16577'  # or one of the other tickets

debugLogFailure = "/home/" + user + "/Desktop/" + bug_number + "_failure/debug.log"
debugLogNormal = "/home/" + user + "/Desktop/" + bug_number + "_normal/debug.log"

with open(debugLogFailure, 'r+') as fp:
    log = fp.read()
    # 2022-07-14 17:24:51,916
    date_regex = r'(\d{4}\-\d{2}\-\d{2}\s)?\d{1,2}\:\d{1,2}\:\d{1,2}(\,\d{3})?'

    # home/[a-zA-Z0-9]/.ccm/test_python_failure/node2
    clusterName_regex = r'\/home\/[a-zA-Z0-9]{0,9}\/\.ccm\/.*/node2'  # using a star for any cluster name

    # java:314
    javaID_regex = r'java\:\d{0,9}'

    # token 7380111211969652565
    tokenID_regex = r'token\s+(-?)\d{1,20}'

    # ranges [(1784141832831967637,1814758406832185510], (3758994068070487793,3775166499811927842], .....]
    localRanges_regex = r'ranges \[.*\]'

    # Ranges needing transfer are [(...], (...],...]
    needingTransfer_regex = r'needing transfer are \[.*\]'

    # 5.677KiB
    KiB_regex = r'\d{1,4}\.\d{1,4}KiB'
    MiB_regex = r'\d{1,4}\.\d{1,4}MiB'

    # Classpath: .../..../..../....jar
    classpath_regex = r'Classpath: .*\.jar'

    # @5a18cd76[...]
    cfmetadata_regex = r'CFMetaData\@.*\[.*\]\]'

    # token(s) [-107910199436536903, -1213662480926735592, -1221822647174710395,...,]
    tokens_regex = r'token(s?) \[.*\]'

    # @1448674088(...)
    num_regex = r'\@[0-9]+\('

    # Node configuration:[...]
    nodeConfiguration_regex = r'Node configuration\:\[.*\]'

    # remote=9353c531-906f-300a-af1f-a3d469583b70
    remoteServer_regex = r'remote=[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+'

    # init = 2555904(2496K) used = 4727040(4616K) committed = 4784128(4672K) max = 251658240(245760K)
    memory_regex = r'init = [0-9]+\([0-9]+K\) ' \
                   r'used = [0-9]+\([0-9]+K\) ' \
                   r'committed = [0-9]+\([0-9]+K\) ' \
                   r'max = (-?)[0-9]+\((-?)[0-9]+K\)'

    # segmentId=1658758350815, position=543
    commitlog_regex = r'segmentId=[0-9]+\, position=[0-9]+'

    # at 1658758105488 with
    id_regex = r'at [0-9]+ with'

    # me-1-big-Data.db
    db_regex = r'm(e|d)-[0-9]+-big(-Data.db)?'

    # Compacting (3e27ae50-0c23-11ed-8cad-4304f9841101)
    compacting_regex = r'Compacting \(.*\) \[.*\]'
    compacted_regex = r'Compacted \([a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\)'

    # in 59ms
    time_regex = r'in [0-9]+ms'

    # created 0858462d-89a5-441a-ab3e-9637e5b0109c
    created_regex = r'created [a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+'

    # schema version: bcd1c7bf-1e18-3d33-9184-48929d14af1f
    schemaVersion_regex = r'schema version(:?) [a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+'

    # InternalResponseStage:2
    internalResponseStage_regex = r'InternalResponseStage:\d'

    # Using Netty Version: [...]
    nettyVersion_regex = r'Netty Version\: \[.*\]'

    # Range (6847199561877748027,6877733767749234154] already in all replicas
    rangeAlreadyInAllReplicas_regex = r'Range \((-?)[0-9]+\,(-?)[0-9]+\] already'

    # Range (-1542563990710368884,-1513591220337879440] will be responsibility
    rangeResponsibility_regex = r'Range \((-?)[0-9]+\,(-?)[0-9]+\] will be responsibility'

    # [Stream #6d5662c0-0c23-11ed-8cad-4304f9841101]
    streamID_regex = r'\[Stream #[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+'

    # ____-37f71aca7dc2383ba70672528af04d4f/
    peers_regex = r'peers-[a-z0-9]+'
    droppedColumns_regex = r'\/dropped_columns-[a-z0-9]+'
    local_regex = r'\/local-[a-z0-9]+'
    sstableActivity_regex = r'\/sstable_activity-[a-z0-9]+'
    sizeEstimates_regex = r'\/size_estimates-[a-z0-9]+'
    transferredRanges_regex = r'\/transferred_ranges-[a-z0-9]+'

    # Setting tokens to [...]
    settingTokens_regex = r'Setting tokens to \[.*\]'

    # Hostname: ...
    hostname_regex = r'Hostname: .*'

    # apache-cassandra-3.11.11.jar:3.11.11
    cassandraVersion_regex = r'apache-cassandra-[0-9]*\.[0-9]*(\.[0-9]*)?\.jar:[0-9]*\.[0-9]*(\.[0-9]*)?'

    # Cassandra version: 3.11.11
    cassandraVersion_regexSecond = r'Cassandra version: [0-9]*\.[0-9]*\.[0-9]*'

    # JVM Arguments: [...]
    jvmArguments_regex = r'JVM Arguments\: \[.*\]'

    # /home/smoothex/.ccm/
    user_regex = r'/home/.*/.ccm/'

    # : 1.616KiB (0%) on-heap, 0.000KiB (0%) off-heap
    # (0%) off-heap
    onHeap_regex = r'[0-9]+ \([0-9]*%\) on-heap, [0-9]+ \([0-9]*%\) off-heap'

    # 326 bytes to 239 (~72% of original)
    compactionInBytes_regex = r'(([0-9]*?\,)?)[0-9]* bytes to (([0-9]*?\,)?)[0-9]*'
    compactionInKiB_regex = r'(([0-9]*?\,)?)[0-9]*KiB to (([0-9]*?\,)?)[0-9]*KiB'

    # 0.003999MB/s.
    speed_regex = r'[0-9]*\.[0-9]*MB/s\.'

    # sstables to [...] to level=
    compactedSSTablesTo_regex = r'sstables to \[.*\] to level='

    # Completed flushing /home/<USER>/.ccm/13337_failure/node1/data0/system_schema/columns-24101c25a2ae3af787c1b40ee1aca33f/mc
    completedFlushing_regex = r'Completed flushing .* \('

    # Generated random tokens. tokens are [...]
    randomTokens_regex = r'Generated random tokens. tokens are \[.*\]'

    # Only 62.813GiB free
    freeGig_regex = r'Only [0-9]*\.[0-9]*GiB free'
    freeMB_regex = r'Only [0-9]*(\.[0-9]*)? MB free'

    # CompilerOracle: ...
    # CompileCommand: ...
    compile_regex = r'Compile(rOracle|Command): .*'

    # baseTableId
    baseTableId_regex = r'baseTableId=[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+'

    # ViewDefinition@6fbffeaf[
    viewDefinition_regex = r'ViewDefinition\@[a-z0-9]+\['

    # VM/1.8.0_72-internal
    jvmVersion_regex = r'VM/.*'

    # [CompactionExecutor:2]
    threadNumber_regex = r'r:\d]'
    threadNumber_regex2 = r'e:\d]'
    threadNumber_regex3 = r'h:\d]'

    # : 351 (
    moreNumbers_regex = r': [0-9]+ \('

    worker_regex = r'Worker-[0-9]+'

    ops_regex = r', [0-9]+ ops,'

    # Flushed to [BigTableReader(path='....')]
    flushPath_regex = r'path=\'.*\''

    checkingDirectory_regex = r'Checking directory \/.*\/node[0-9]+\/'

    nativeTransportRequests_regex = r'Native-Transport-Requests-[0-9]+'
    perDiskMemtable_regex = r'PerDiskMemtableFlushWriter_[0-9]+:[0-9]+'
    configurationLocation_regex = r'file:.*\/cassandra.yaml'

    # ~73% of original
    ofOriginal_regex = r'\~[0-9]*\% of original'

    # Row Throughput = ~41/s
    rowThroughput_regex = r'Row Throughput = \~[0-9]*\/s'

    # ReadStage-4
    readStage_regex = r'ReadStage-[0-9]+'

    ringVersion_regex = r'ringVersion( )?=( )?[0-9]+'

    completedLoading_regex = r'Completed loading \([0-9]* ms; [0-9]* keys\)'

    # adding expire time for endpoint : \/127.0.0.[0-9]+ ([0-9]+)'
    expireTime_regex = r'adding expire time for endpoint : \/127\.0\.0\.([0-9]+) \([0-9]+\)'

    log = re.sub(pattern=date_regex,
                 repl="<TIMESTAMP>",
                 string=log)
    log = re.sub(pattern=clusterName_regex,
                 repl="<DIR>",
                 string=log)
    log = re.sub(pattern=javaID_regex,
                 repl="<JAVA_ID>",
                 string=log)
    log = re.sub(pattern=tokenID_regex,
                 repl="<TOKEN_ID>",
                 string=log)
    log = re.sub(pattern=localRanges_regex,
                 repl="ranges <TOKEN_RANGES>",
                 string=log)
    log = re.sub(pattern=KiB_regex,
                 repl="<NUM>KiB",
                 string=log)
    log = re.sub(pattern=MiB_regex,
                 repl="<NUM>MiB",
                 string=log)
    log = re.sub(pattern=classpath_regex,
                 repl="Classpath: <CLASSPATH>",
                 string=log)
    log = re.sub(pattern=cfmetadata_regex,
                 repl="CFMetaData@<ID>[<METADATA>]]",
                 string=log)
    log = re.sub(pattern=tokens_regex,
                 repl="tokens [<TOKEN_IDs>]",
                 string=log)
    log = re.sub(pattern=num_regex,
                 repl="@<ID>(",
                 string=log)
    log = re.sub(pattern=nodeConfiguration_regex,
                 repl="Node configuration:[<NODE_CONF>]",
                 string=log)
    log = re.sub(pattern=remoteServer_regex,
                 repl="remote=<IP>",
                 string=log)
    log = re.sub(pattern=memory_regex,
                 repl="init = <NUM> used = <NUM> committed = <NUM> max = <NUM>",
                 string=log)
    log = re.sub(pattern=commitlog_regex,
                 repl="segmentId=<NUM>, position=<NUM>",
                 string=log)
    log = re.sub(pattern=id_regex,
                 repl="at <ID> with",
                 string=log)
    log = re.sub(pattern=db_regex,
                 repl="<.db FILE>",
                 string=log)
    log = re.sub(pattern=compacting_regex,
                 repl="Compacting (<ID>) [<COMPACTED .db FILES>]",
                 string=log)
    log = re.sub(pattern=compacted_regex,
                 repl="Compacted (<ID>)",
                 string=log)
    log = re.sub(pattern=time_regex,
                 repl="in <NUM>ms",
                 string=log)
    log = re.sub(pattern=created_regex,
                 repl="created <IP>",
                 string=log)
    log = re.sub(pattern=schemaVersion_regex,
                 repl="current schema version: <IP>",
                 string=log)
    log = re.sub(pattern=internalResponseStage_regex,
                 repl="InternalResponseStage:<NUM>",
                 string=log)
    log = re.sub(pattern=needingTransfer_regex,
                 repl="needing transfer are <TOKEN_RANGES>",
                 string=log)
    log = re.sub(pattern=nettyVersion_regex,
                 repl="Netty Version: <NETTY_VERSIONS>",
                 string=log)
    log = re.sub(pattern=rangeAlreadyInAllReplicas_regex,
                 repl="Range <TOKEN_RANGE> already",
                 string=log)
    log = re.sub(pattern=rangeResponsibility_regex,
                 repl="Range <TOKEN_RANGE> will be responsibility",
                 string=log)
    log = re.sub(pattern=streamID_regex,
                 repl="[Stream <STREAM_ID>",
                 string=log)
    log = re.sub(pattern=peers_regex,
                 repl="peers-<ID>",
                 string=log)
    log = re.sub(pattern=droppedColumns_regex,
                 repl="/dropped_columns-<ID>",
                 string=log)
    log = re.sub(pattern=local_regex,
                 repl="/local-<ID>",
                 string=log)
    log = re.sub(pattern=sstableActivity_regex,
                 repl="/sstable_activity-<ID>",
                 string=log)
    log = re.sub(pattern=sizeEstimates_regex,
                 repl="/size_estimates-<ID>",
                 string=log)
    log = re.sub(pattern=settingTokens_regex,
                 repl="Setting tokens to [<TOKEN_IDs>]",
                 string=log)
    log = re.sub(pattern=transferredRanges_regex,
                 repl="/transferred_ranges-<ID>",
                 string=log)
    log = re.sub(pattern=hostname_regex,
                 repl="Hostname: <HOSTNAME>",
                 string=log)
    log = re.sub(pattern=cassandraVersion_regex,
                 repl="apache-cassandra-<VERSION>.jar:<VERSION>",
                 string=log)
    log = re.sub(pattern=cassandraVersion_regexSecond,
                 repl="Cassandra version: <VERSION>",
                 string=log)
    log = re.sub(pattern=jvmArguments_regex,
                 repl="JVM Arguments: [<JVM_ARGS>]",
                 string=log)
    log = re.sub(pattern=user_regex,
                 repl="/home/<USER>/.ccm/",
                 string=log)
    log = re.sub(pattern=compactionInBytes_regex,
                 repl="<NUM> bytes to <NUM>",
                 string=log)
    log = re.sub(pattern=compactionInKiB_regex,
                 repl="<NUM>KiB to <NUM>KiB",
                 string=log)
    log = re.sub(pattern=speed_regex,
                 repl="<NUM>MB/s.",
                 string=log)
    log = re.sub(pattern=compactedSSTablesTo_regex,
                 repl="sstables to [<PATH>] to level=",
                 string=log)
    log = re.sub(pattern=completedFlushing_regex,
                 repl="Completed flushing [<.db FILES>] (",
                 string=log)
    log = re.sub(pattern=onHeap_regex,
                 repl="<NUM> (<NUM>%) on-heap, <NUM> (<NUM>%) off-heap",
                 string=log)
    log = re.sub(pattern=randomTokens_regex,
                 repl="Generated random tokens. tokens are [<TOKEN_IDs>]",
                 string=log)
    log = re.sub(pattern=freeGig_regex,
                 repl="Only <NUM>GiB free",
                 string=log)
    log = re.sub(pattern=freeMB_regex,
                 repl="Only <NUM> MB free",
                 string=log)
    log = re.sub(pattern=compile_regex,
                 repl="<COMPILE_INFO>",
                 string=log)
    log = re.sub(pattern=baseTableId_regex,
                 repl="baseTableId=<ID>",
                 string=log)
    log = re.sub(pattern=viewDefinition_regex,
                 repl="ViewDefinition@<ID>[",
                 string=log)
    log = re.sub(pattern=jvmVersion_regex,
                 repl="VM/<VERSION>",
                 string=log)
    log = re.sub(pattern=threadNumber_regex,
                 repl="r:<NUM>]",
                 string=log)
    log = re.sub(pattern=threadNumber_regex2,
                 repl="e:<NUM>]",
                 string=log)
    log = re.sub(pattern=threadNumber_regex3,
                 repl="h:<NUM>]",
                 string=log)
    log = re.sub(pattern=moreNumbers_regex,
                 repl=": <NUM> (",
                 string=log)
    log = re.sub(pattern=worker_regex,
                 repl="Worker-<NUM>",
                 string=log)
    log = re.sub(pattern=ops_regex,
                 repl=", <NUM> ops,",
                 string=log)
    log = re.sub(pattern=flushPath_regex,
                 repl="path= <PATH>",
                 string=log)
    log = re.sub(pattern=checkingDirectory_regex,
                 repl="Checking directory <PATH>/",
                 string=log)
    log = re.sub(pattern=nativeTransportRequests_regex,
                 repl="Native-Transport-Requests-<NUM>",
                 string=log)
    log = re.sub(pattern=perDiskMemtable_regex,
                 repl="PerDiskMemtableFlushWriter_<NUM>:<NUM>",
                 string=log)
    log = re.sub(pattern=configurationLocation_regex,
                 repl="file:<PATH>/cassandra.yaml",
                 string=log)
    log = re.sub(pattern=ofOriginal_regex,
                 repl="~<NUM>% of original",
                 string=log)
    log = re.sub(pattern=rowThroughput_regex,
                 repl="Row Throughput = ~<NUM>/s",
                 string=log)
    log = re.sub(pattern=readStage_regex,
                 repl="ReadStage-<NUM>",
                 string=log)
    log = re.sub(pattern=ringVersion_regex,
                 repl="ringVersion=<NUM>",
                 string=log)
    log = re.sub(pattern=completedLoading_regex,
                 repl="Completed loading (<NUM> ms; <NUM> keys)",
                 string=log)
    log = re.sub(pattern=expireTime_regex,
                 repl=r"adding expire time for endpoint : /127.0.0.\1 (<NUM>)",  # prefix the string with "r"
                                                                                 # so that \ isn't treated as
                                                                                 # an escape character
                 string=log)

    fp.seek(0)
    fp.write(log)
    fp.truncate()
