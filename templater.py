debugLogFailure = "/home/smoothex/Desktop/debug.log"
debugLogNormal = "/home/smoothex/.ccm/test_python_normal/node2/logs/debug.log"

import re

with open(debugLogFailure, 'r+') as fp:
    log = fp.read()
    # 2022-07-14 17:24:51,916
    date_regex = r'\d{4}\-\d{2}\-\d{2}\s+\d{1,2}\:\d{1,2}\:\d{1,2}\,\d{3}'

    # home/[a-zA-Z0-9]/.ccm/test_python_failure/node2
    clusterName_regex = r'\/home\/[a-zA-Z0-9]{0,9}\/\.ccm\/.*/node2'  # using a star for any cluster name

    # java:314
    javaID_regex = r'java\:\d{0,9}'

    # token 7380111211969652565
    tokenID_regex = r'token\s+(-?)\d{1,20}'

    # Got local ranges [(1784141832831967637,1814758406832185510], (3758994068070487793,3775166499811927842], .....]
    localRanges_regex = r'Got local ranges \[.*\]'

    # 5.677KiB
    KiB_regex = r'\d{1,4}\.\d{1,4}KiB'
    MiB_regex = r'\d{1,4}\.\d{1,4}MiB'

    # Classpath: .../..../..../....jar
    classpath_regex = r'Classpath: .*\.jar'

    # CFMetaData@5a18cd76
    cfmetadata_regex = r'CFMetaData\@.*\[.*\]'

    # tokens [-107910199436536903, -1213662480926735592, -1221822647174710395,...,]
    tokens_regex = r'tokens \[.*\]'

    # peers@1448674088(...)
    peers_regex = r'peers\@.*\('

    # Node configuration:[...]
    nodeConfiguration_regex = r'Node configuration\:\[.*\]'

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
    log = re.sub(pattern=peers_regex,
                 repl="peers@<ID>(",
                 string=log)
    log = re.sub(pattern=nodeConfiguration_regex,
                 repl="Node configuration:[<NODE_CONF>]",
                 string=log)
    fp.seek(0)
    fp.write(log)
    fp.truncate()
