export const snapshots = {
  "snapshot_id": "af3b2103-2793-4adf-82c3-f72d65278b3b",
  "committed_at": "2023-03-01T12:00:00Z",
  "operation": "append",
  "manifest_list": "hdfs://path/to/manifests/af3b2103-2793-4adf-82c3-f72d65278b3b",
  "children": [
    {
      "snapshot_id": "4a9def68-f9ef-43bd-b58c-93b703aa8ecc",
      "committed_at": "2023-03-02T12:00:00Z",
      "operation": "append",
      "manifest_list": "hdfs://path/to/manifests/4a9def68-f9ef-43bd-b58c-93b703aa8ecc",
      "children": [
        {
          "snapshot_id": "7ff9aec2-e4ae-4383-bbd2-025c6bf41150",
          "committed_at": "2023-03-04T12:00:00Z",
          "operation": "append",
          "manifest_list": "hdfs://path/to/manifests/7ff9aec2-e4ae-4383-bbd2-025c6bf41150",
          "children": []
        }
      ]
    },
    {
      "snapshot_id": "f929b3b3-40fd-4d36-be94-21700b9ff7b2",
      "committed_at": "2023-03-03T12:00:00Z",
      "operation": "append",
      "manifest_list": "hdfs://path/to/manifests/f929b3b3-40fd-4d36-be94-21700b9ff7b2",
      "children": [
        {
          "snapshot_id": "be90572b-5845-4289-98ae-475c7c1db462",
          "committed_at": "2023-03-05T12:00:00Z",
          "operation": "append",
          "manifest_list": "hdfs://path/to/manifests/be90572b-5845-4289-98ae-475c7c1db462",
          "children": []
        }
      ]
    }
  ]
}

export const branches = [
  {
    "name": "ML_new",
    "type": "BRANCH",
    "snapshot_id": "7367054809802582990",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "main",
    "type": "BRANCH",
    "snapshot_id": "1542775573264603010",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "ML_exp",
    "type": "BRANCH",
    "snapshot_id": "2548069857708149163",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  }
]

export const tags = [
  {
    "name": "june_data",
    "type": "TAG",
    "snapshot_id": "3103801334122039208",
    "max_reference_age_in_ms": 864000000.0,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "tag_1",
    "type": "TAG",
    "snapshot_id": "2256763123076765788",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "tag_2",
    "type": "TAG",
    "snapshot_id": "2595734063664140046",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "tag_3",
    "type": "TAG",
    "snapshot_id": "3281318750438982151",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  },
  {
    "name": "tag_4",
    "type": "TAG",
    "snapshot_id": "6563344135811683800",
    "max_reference_age_in_ms": null,
    "min_snapshots_to_keep": null,
    "max_snapshot_age_in_ms": null
  }
]



export const databaseList = ["DatabaseA", "DatabaseB", "DatabaseC"];


export const tables = {
  DatabaseA: ["Table1", "Table2", "Table3"],
  DatabaseB: ["Table4", "Table5"],
  DatabaseC: ["Table6", "Table7", "Table8", "Table9"]
}

export const snapshotDetail = {
  made_current_at: "2024-04-18T19:24:21.767Z",
  snapshot_id: 8104528337525736000,
  is_current_ancestor: true,
  committed_at: "2024-04-18T19:24:21.767Z",
  operation: "append",
  manifest_list: "s3a://warehouse/toyDb/taxis1/metadata/snap-8104528337525736285-1-83f1833a-2cb4-4a46-8233-c59e263efc26.avro",
  summary: {
    "total-equality-deletes": "0",
    "changed-partition-count": "0",
    "total-position-deletes": "0",
    "total-files-size": "0",
    "total-records": "0",
    "total-delete-files": "0",
    "total-data-files": "0",
    "spark.app.id": "local-1713468174582"
  }
};