# Elastic Search

## Index

- [Concepts](#concepts)
- [ES\_Index](#es_index)
- [ES\_Document](#es_document)
- [Jenkins\_Data\_Queries\_Examples](#jenkins_data_queries_examples)

## Concepts

- Cluster – An Elasticsearch cluster consists of one or more nodes and is identifiable by its cluster name.

- Node (VM o separate Box)
  - A single Elasticsearch instance. In most environments, each node runs on a separate box or virtual machine.

- Index (Collection of meaningful data about an Entity - "Table in SQL")
  - In Elasticsearch, an index is a collection of documents.

- Document ("Record in SQL")
  - It refers to the top-level, or root object that is serialized into JSON and stored in Elasticsearch under a **unique ID**.

- Shard (Divisions of the Index, thus missing shards > Data lost)
  - Because Elasticsearch is a distributed search engine, an index is usually split into elements known as shards that are distributed across multiple nodes. Elasticsearch automatically manages the arrangement of these shards. It also rebalances the shards as necessary, so users need not worry about the details.

- Replica (Copy of the Full Index, and the shards which compose it, HA for ES)
  - By default, Elasticsearch creates five primary shards and one replica for each index. This means that each index will consist of five **primary shards**, and each shard will have one copy (**replica shards**).

Allocating multiple shards and replicas is the essence of the design for distributed search capability, providing for high availability and quick access in searches against the documents within an index. The main difference between a primary and a replica shard is that only the primary shard can accept indexing requests. Both replicas and primary shards can serve querying requests.

![](../../img/docs/esCluster.png)

In the diagram above, we have an Elasticsearch cluster consisting of two nodes in a default shard configuration. Elasticsearch automatically arranges the five primary shards split across the two nodes. There is one replica shard that corresponds to each primary shard, but the arrangement of these replica shards is altogether different from that of the primary shards. Again, think distribution.

Allow us to clarify: Remember, the number_of_shards value pertains to indexes—not to the cluster as a whole. This value specifies the number of shards for each index (not the total primary shards in the cluster).

## ES_Index

List all indexes ("Table in SQL") => Get a description of one index ("Columns in SQL")

```sh
# curl [-u <USER>:<PASS>] "$elasticsearchURL/$index/_mapping"
> curl -u ***:**** "http://example.com/elasticsearch/builds-20170606/_mapping?v&pretty"

  "builds-20170606" : {
    "mappings" : {
      "run" : {
        "properties" : {
          "@timestamp" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "class" : {
            "type" : "string"
          },
          "classSimpleName" : {
            "type" : "string"
          },
          "displayName" : {
            "type" : "string"
          },
          "duration" : {
            "type" : "long"
          },
          "effectiveLabelAtoms" : {
            "type" : "string"
          },
          "fullDisplayName" : {
            "type" : "string"
          },
          "jenkins.metrics.impl.TimeInQueueAction" : {
            "properties" : {
              "buildingDurationMillis" : {
                "type" : "long"
              },
              "queuingDurationMillis" : {
                "type" : "long"
              },
              "totalDurationMillis" : {
                "type" : "long"
              }
            }
          },
          "masterId" : {
            "type" : "string"
          },
          "masterName" : {
            "type" : "string"
          },
          "masterName_analyzed" : {
            "type" : "string"
          },
          "monitoringId" : {
            "type" : "string"
          },
          "nodeReferences" : {
            "properties" : {
              "effectiveLabelAtoms" : {
                "type" : "string"
              },
              "nodeName" : {
                "type" : "string"
              },
              "timestamp" : {
                "type" : "long"
              }
            }
          },
          "number" : {
            "type" : "long"
          },
          "parent" : {
            "properties" : {
              "assignedLabel" : {
                "type" : "string"
              },
              "class" : {
                "type" : "string"
              },
              "classSimpleName" : {
                "type" : "string"
              },
              "createdDate" : {
                "type" : "long"
              },
              "description" : {
                "type" : "string"
              },
              "disabled" : {
                "type" : "boolean"
              },
              "fullDisplayName" : {
                "type" : "string"
              },
              "fullName" : {
                "type" : "string"
              },
              "monitoringId" : {
                "type" : "string"
              },
              "scm" : {
                "properties" : {
                  "classSimpleName" : {
                    "type" : "string"
                  },
                  "type" : {
                    "type" : "string"
                  }
                }
              },
              "type" : {
                "type" : "string"
              },
              "url" : {
                "type" : "string"
              }
            }
          },
          "result" : {
            "properties" : {
              "completed" : {
                "type" : "boolean"
              },
              "name" : {
                "type" : "string"
              }
            }
          },
          "startTimeInMillis" : {
            "type" : "long"
          },
          "type" : {
            "type" : "string"
          },
          "url" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

## ES_Document

Document = Record ("Row in SQL")

```sh
### DOCUMENT #####
{
##### METADATA #####
  "_index" : "builds-20170606",
  "_type" : "run",
  "_id" : "994",
  "_score" : 0.15342641,
##### END OF METADATA #####
##### SOURCE #####
  "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_2","class":"hudson.model.FreeStyleBuild","classSimpleName":"FreeStyleBuild","startTimeInMillis":1496727765817,"duration":632,"number":2,"displayName":"#2","fullDisplayName":"support » job-001 #2","description":null,"url":"job/support/job/job-001/2/","parent":{"type":"item","class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001","fullDisplayName":"supportjob-001","url":"job/support/job/job-001/","description":"","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496727765074,"scm":{"type":"hudson.scm.NullSCM","classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker"},"jenkins.metrics.impl.TimeInQueueAction":{"queuingDurationMillis":13449,"totalDurationMillis":14081,"buildingDurationMillis":632},"result":{"completed":true,"name":"SUCCESS"},"effectiveLabelAtoms":"docker","nodeReferences":[{"timestamp":1496727765817,"nodeName":"31498441","effectiveLabelAtoms":"docker"}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8","masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:42:45.817+0000"}
}
##### END OF SOURCE #####
### END OF ROW #####
```

## Jenkins_Data_Queries_Examples

A document needs to be indexed before you can search for it. Elasticsearch refreshes  every  second by default

Ref: [Exploring your data](https://www.elastic.co/guide/en/elasticsearch/reference/1.7/_exploring_your_data.html)

### 1. Across all indexes and all types

```sh
> curl [-u <USER>:<PASS>] -XGET '$elasticsearchURL/_search?v&pretty' -d { "query" : {<QUERY>}}
```

#### Matches all

```sh
> curl -u ****:**** -XGET  '$elasticsearchURL/_search?v&pretty' -d '{ "query" : { "match_all" : {}}}'
```

#### Select `{ "term" : {"fullName":"job"}` from all indexes and all types

```sh
> curl -u ***:*** -XGET  '$elasticsearchURL/_search?v&pretty' -d '{ "query" : { "term" : {"fullName":"job"}}}'
#### successful
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 56,
    "successful" : 56,
    "failed" : 0
  },
  "hits" : {
    "total" : 5,
    "max_score" : 0.15342641,
    "hits" : [ {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_2",
      "_score" : 0.15342641,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_2","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496727765817,"duration":632,"number":2,"displayName":"#2",
      "fullDisplayName":"support » job-001 #2","description":null,"url":"job/support/job/job-001/2/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496727765074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":13449,"totalDurationMillis":14081,"buildingDurationMillis":632},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"docker ","nodeReferences":[{"timestamp":1496727765817,"nodeName":"31498441",
      "effectiveLabelAtoms":"docker"}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:42:45.817+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_4",
      "_score" : 0.15342641,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_4","class":"hudson.model.FreeStyleBuild","classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728408886,"duration":14,"number":4,"displayName":"#4",
      "fullDisplayName":"support » job-001 #4","description":null,"url":"job/support/job/job-001/4/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728365074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"<any>"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":1,"totalDurationMillis":15,"buildingDurationMillis":14},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"","nodeReferences":[{"timestamp":1496728408886,"nodeName":"",
      "effectiveLabelAtoms":null}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:53:28.886+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_5",
      "_score" : 0.15342641,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_5","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728438161,"duration":14,"number":5,"displayName":"#5",
      "fullDisplayName":"support » job-001 #5","description":null,"url":"job/support/job/job-001/5/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728365074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"<any>"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":1,"totalDurationMillis":15,"buildingDurationMillis":14},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"","nodeReferences":[{"timestamp":1496728438161,"nodeName":"",
      "effectiveLabelAtoms":null}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:53:58.161+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_6",
      "_score" : 0.15342641,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_6","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728930206,"duration":491,"number":6,"displayName":"#6",
      "fullDisplayName":"support » job-001 #6","description":null,"url":"job/support/job/job-001/6/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728905073,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":23050,"totalDurationMillis":23541,"buildingDurationMillis":491},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"docker ","nodeReferences":[{"timestamp":1496728930206,"nodeName":"733d8368",
      "effectiveLabelAtoms":"docker"}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T06:02:10.206+0000"}
    }, {
      "_index" : "items",
      "_type" : "item",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT",
      "_score" : 0.15342641,
      "_source":{"type":"item","class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/
      job-001","fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728905073,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker",
      "masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8","masterName":"Master-1",
      "masterName_analyzed":"Master-1","@timestamp":"2017-06-06T06:01:45.073+0000"}
    } ]
  }
}
#### fails
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 56,
    "successful" : 56,
    "failed" : 0
  },
  "hits" : {
    "total" : 0,
    "max_score" : null,
    "hits" : [ ]
  }
}
```

### 2. Across 1 index and all types

```sh
> curl [-u <USER>:<PASS>] -XGET '$elasticsearchURL/$index/_search?v&pretty' -d { "query" : {<QUERY>}}
```

##### Search across all types in the `nodes-20170606` index

```sh
> curl -u ***:**** -XGET '$elasticsearchURL/nodes-20170606/_search?' -d '{ "query" : { "match_all" : {}}}'
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 3,
    "max_score" : 1.0,
    "hits" : [ {
      "_index" : "nodes-20170606",
      "_type" : "node",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YWU4NzI1ZTUtMjdmOC00MGE0LWE1YT",
      "_score" : 1.0,
      "_source":{"type":"node","monitoringId":"YWU4NzI1ZTUtMjdmOC00MGE0LWE1YT","name":"new-node","displayName":"new-node","class":"hudson.slaves.DumbSlave","timestamp":1496762235074,"isEphemeral":false,"isDeleted":false,"info":{"slave":{"name":"new-node","description":"","remoteFS":"/Users/fbelzunc/caca-slave","numExecutors":"1","mode":"NORMAL","retentionStrategy":"","launcher":"","label":"","nodeProperties":""}},"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8","masterName":"Master-1","masterName_analyzed":"Master-1"}
    }, {
      "_index" : "nodes-20170606",
      "_type" : "node",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-MzJkMjE0ZjYtYzEzOC00Yzc1LThkND",
      "_score" : 1.0,
      "_source":{"type":"node","monitoringId":"MzJkMjE0ZjYtYzEzOC00Yzc1LThkND","name":"733d8368","displayName":"733d8368","class":"com.cloudbees.tiger.plugins.palace.PalaceSlave","timestamp":1496728935073,"isEphemeral":false,"isDeleted":false,"info":{"com.cloudbees.tiger.plugins.palace.PalaceSlave":{"name":"733d8368","description":"Container provisioned from http://example.com/palace/v1/task/master-1.733d8368:f2c61499-35ec-40b7-b4f1-9e64a91f37f0","remoteFS":"/mnt/mesos/sandbox/jenkins","numExecutors":"1","mode":"NORMAL","retentionStrategy":"","launcher":"","label":"docker","nodeProperties":"","userId":"anonymous","template":{"actions":"","disabled":"false","cpus":"0.1","memory":"768","jvmArgs":"-Xms16m -XX:+UseConcMarkSweepGC -Djava.net.preferIPv4Stack=true","jnlpArgs":"","jvmMemory":"256","defaultLabel":"false","remoteFS":"/mnt/mesos/sandbox/jenkins","containerProperties":{"com.cloudbees.tiger.plugins.palace.model.VolumeSpec":{"containerPath":"/var/run/docker.sock","hostPath":"/var/run/docker.sock","readOnly":"false"},"com.cloudbees.tiger.plugins.palace.model.URISpec":{"value":"file:///root/docker.tar.gz","executable":"false","extract":"true"}},"image":"cloudbees/java-with-docker-client"},"slave":{"url":"http://example.com/palace/v1/task/master-1.733d8368:f2c61499-35ec-40b7-b4f1-9e64a91f37f0","account":"master-1","signature":"JNfGbJQnmSjJnu5Hn4VOx3cpkR1hMLP9PD9+Mo1V5Z/QGgVBxSDXblNq3FS4juhACLOVvOHbwczDlrjpCyYSZpvM/lBBfKg0/hJDx3Zbr4RBOxm5pqUOEYrndKTrFuH1sNm3AVvrAAvwAzDjbHARqrEtiYJhcFTr2Qd/RORFf9kd0MNWomtY8+/4PKOBIDc5F06vGQP02Y0E8ocTy0LdTpUhIeqS49gkaXnpkKHJKrta1OOm/oFlvaln43cG1iVyeJE2E8BNOXc0SEYWtu3pEogIeNJb/R/X9eeFGrA1d6U+nqGEM+wB0JOB+f+fxDVbAbxiuXrIQz50VQrP2FvsPA==","taskResponse":{"status":"TASK_PENDING","label":"docker","slaveId":"master-1.733d8368:f2c61499-35ec-40b7-b4f1-9e64a91f37f0","creationTime":"1496728916637","statusTime":"1496728916637"},"brokerRefUrl":"http://example.com/palace/v1/"},"brokerRefUrl":"http://example.com/palace/v1/","createdDate":"1496728916639"}},"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8","masterName":"Master-1","masterName_analyzed":"Master-1"}
    }, {
      "_index" : "nodes-20170606",
      "_type" : "node",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-NDg1MzBhZTktM2JhYi00NTEwLWI0Yz",
      "_score" : 1.0,
      "_source":{"type":"node","monitoringId":"NDg1MzBhZTktM2JhYi00NTEwLWI0Yz","name":"31498441","displayName":"31498441","class":"com.cloudbees.tiger.plugins.palace.PalaceSlave","timestamp":1496727765075,"isEphemeral":false,"isDeleted":false,"info":{"com.cloudbees.tiger.plugins.palace.PalaceSlave":{"name":"31498441","description":"Container provisioned from http://example.com/palace/v1/task/master-1.31498441:84d989bc-fd6b-4203-9ec8-e2a36dfc4859","remoteFS":"/mnt/mesos/sandbox/jenkins","numExecutors":"1","mode":"NORMAL","retentionStrategy":"","launcher":"","label":"docker","nodeProperties":"","userId":"anonymous","template":{"actions":"","disabled":"false","cpus":"0.1","memory":"768","jvmArgs":"-Xms16m -XX:+UseConcMarkSweepGC -Djava.net.preferIPv4Stack=true","jnlpArgs":"","jvmMemory":"256","defaultLabel":"false","remoteFS":"/mnt/mesos/sandbox/jenkins","containerProperties":{"com.cloudbees.tiger.plugins.palace.model.VolumeSpec":{"containerPath":"/var/run/docker.sock","hostPath":"/var/run/docker.sock","readOnly":"false"},"com.cloudbees.tiger.plugins.palace.model.URISpec":{"value":"file:///root/docker.tar.gz","executable":"false","extract":"true"}},"image":"cloudbees/java-with-docker-client"},"slave":{"url":"http://example.com/palace/v1/task/master-1.31498441:84d989bc-fd6b-4203-9ec8-e2a36dfc4859","account":"master-1","signature":"JNfGbJQnmSjJnu5Hn4VOx3cpkR1hMLP9PD9+Mo1V5Z/QGgVBxSDXblNq3FS4juhACLOVvOHbwczDlrjpCyYSZpvM/lBBfKg0/hJDx3Zbr4RBOxm5pqUOEYrndKTrFuH1sNm3AVvrAAvwAzDjbHARqrEtiYJhcFTr2Qd/RORFf9kd0MNWomtY8+/4PKOBIDc5F06vGQP02Y0E8ocTy0LdTpUhIeqS49gkaXnpkKHJKrta1OOm/oFlvaln43cG1iVyeJE2E8BNOXc0SEYWtu3pEogIeNJb/R/X9eeFGrA1d6U+nqGEM+wB0JOB+f+fxDVbAbxiuXrIQz50VQrP2FvsPA==","taskResponse":{"status":"TASK_PENDING","label":"docker","slaveId":"master-1.31498441:84d989bc-fd6b-4203-9ec8-e2a36dfc4859","creationTime":"1496727752422","statusTime":"1496727752422"},"brokerRefUrl":"http://example.com/palace/v1/"},"brokerRefUrl":"http://example.com/palace/v1/","createdDate":"1496727752425"}},"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8","masterName":"Master-1","masterName_analyzed":"Master-1"}
    } ]
  }
}
```

#### 3. Across 1 index and 1 type

```
> curl [-u <USER>:<PASS>] -XGET '$elasticsearchURL/$index/$type/_search?v&pretty' -d { "query" : {<QUERY>}}
```

##### Search across type `run` in the `builds-20170606` index

```sh
> curl -u ***:**** -XGET 'http://example.com/elasticsearch/builds-20170606/run/_search?v&pretty' -d '{ "query" : { "match_all" : {}}}'

{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 5,
    "max_score" : 1.0,
    "hits" : [ {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_2",
      "_score" : 1.0,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_2","class":"hudson.model.FreeStyleBuild","classSimpleName":"FreeStyleBuild","startTimeInMillis":1496727765817,"duration":632,"number":2,"displayName":"#2",
      "fullDisplayName":"support » job-001 #2","description":null,"url":"job/support/job/job-001/2/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496727765074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":13449,"totalDurationMillis":14081,"buildingDurationMillis":632},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"docker ","nodeReferences":[{"timestamp":1496727765817,"nodeName":"31498441",
      "effectiveLabelAtoms":"docker"}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:42:45.817+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YjI4MjQ4MTItYjE2NC00MTNkLWEwZj_2",
      "_score" : 1.0,
      "_source":{"type":"run","monitoringId":"YjI4MjQ4MTItYjE2NC00MTNkLWEwZj_2","class":"hudson.model.FreeStyleBuild","classSimpleName":"FreeStyleBuild","startTimeInMillis":1496744093251,"duration":500012,"number":2,"displayName":"#2",
      "fullDisplayName":"support » sleep-500 #2","description":null,"url":"job/support/job/sleep-500/2/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/sleep-500",
      "fullDisplayName":"support » sleep-500","url":"job/support/job/sleep-500/","description":"",
      "monitoringId":"YjI4MjQ4MTItYjE2NC00MTNkLWEwZj","createdDate":1495519450571,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"<any>"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":1,"totalDurationMillis":500013,"buildingDurationMillis":500012},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"","nodeReferences":[{"timestamp":1496744093251,"nodeName":"",
      "effectiveLabelAtoms":null}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T10:14:53.251+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_4",
      "_score" : 1.0,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_4","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728408886,"duration":14,"number":4,"displayName":"#4",
      "fullDisplayName":"support » job-001 #4","description":null,"url":"job/support/job/job-001/4/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728365074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"<any>"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":1,"totalDurationMillis":15,"buildingDurationMillis":14},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"","nodeReferences":[{"timestamp":1496728408886,"nodeName":"",
      "effectiveLabelAtoms":null}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:53:28.886+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_5",
      "_score" : 1.0,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_5","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728438161,"duration":14,"number":5,"displayName":"#5",
      "fullDisplayName":"support » job-001 #5","description":null,"url":"job/support/job/job-001/5/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728365074,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"<any>"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":1,"totalDurationMillis":15,"buildingDurationMillis":14},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"","nodeReferences":[{"timestamp":1496728438161,"nodeName":"",
      "effectiveLabelAtoms":null}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T05:53:58.161+0000"}
    }, {
      "_index" : "builds-20170606",
      "_type" : "run",
      "_id" : "9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8-YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_6",
      "_score" : 1.0,
      "_source":{"type":"run","monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT_6","class":"hudson.model.FreeStyleBuild",
      "classSimpleName":"FreeStyleBuild","startTimeInMillis":1496728930206,"duration":491,"number":6,"displayName":"#6",
      "fullDisplayName":"support » job-001 #6","description":null,"url":"job/support/job/job-001/6/","parent":{"type":"item",
      "class":"hudson.model.FreeStyleProject","classSimpleName":"FreeStyleProject","fullName":"support/job-001",
      "fullDisplayName":"support » job-001","url":"job/support/job/job-001/","description":"",
      "monitoringId":"YTZhNmJiM2EtNjZmYi00MTA5LTkxNT","createdDate":1496728905073,"scm":{"type":"hudson.scm.NullSCM",
      "classSimpleName":"NullSCM"},"disabled":false,"assignedLabel":"docker"},"jenkins.metrics.impl.TimeInQueueAction":
      {"queuingDurationMillis":23050,"totalDurationMillis":23541,"buildingDurationMillis":491},"result":{"completed":true,
      "name":"SUCCESS"},"effectiveLabelAtoms":"docker ","nodeReferences":[{"timestamp":1496728930206,"nodeName":"733d8368",
      "effectiveLabelAtoms":"docker"}],"masterId":"9948CA2B12F467B4C3C0C8146E81225CCD05EE1B47E916D564501BACFDF439C8",
      "masterName":"Master-1","masterName_analyzed":"Master-1","@timestamp":"2017-06-06T06:02:10.206+0000"}
    } ]
  }
}
```
