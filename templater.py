debugLogFailure = "/home/smoothex/Desktop/test_python_failure/debug.log"
debugLogNormal = "/home/smoothex/Desktop/test_python_normal/debug.log"

import re

with open(debugLogNormal, 'r+') as fp:
    log = fp.read()
    # 2022-07-14 17:24:51,916
    date_regex = r'\d{4}\-\d{2}\-\d{2}\s+\d{1,2}\:\d{1,2}\:\d{1,2}\,\d{3}'

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

    # CFMetaData@5a18cd76
    cfmetadata_regex = r'CFMetaData\@.*\[.*\]'

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
    compacting_regex = r'Compacting \([a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\)'
    compacted_regex = r'Compacted \([a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\)'

    # in 59ms
    time_regex = r'in \d{1,2}ms'

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

    log = re.sub(pattern=date_regex,
                 repl="<DATE>",
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
                 repl="Got local ranges <TOKEN_RANGES>",
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
                 repl="CFMetaData@<ID>[<METADATA>]",
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
                 repl="Compacting (<ID>)",
                 string=log)
    log = re.sub(pattern=compacted_regex,
                 repl="Compacted (<ID>)",
                 string=log)
    log = re.sub(pattern=time_regex,
                 repl="in <TIME>ms",
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

    fp.seek(0)
    fp.write(log)
    fp.truncate()
