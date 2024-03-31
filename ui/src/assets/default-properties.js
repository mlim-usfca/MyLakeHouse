export const properties = [
  {
  "property": "read.split.target-size",
  "description": "Target size when combining data input splits",
  "value": 128,
  "unit": "MB",
  "options": [128],
  "type": "read"
},
  {
    "property": "read.split.metadata-target-size",
    "description": "Target size when combining metadata input splits",
    "value": 32,
    "unit": "MB",
    "options": [32],
    "type": "read"
  },
  {
    "property": "read.split.planning-lookback",
    "description": "Number of bins to consider when combining input splits",
    "value": 10,
    "unit": "",
    "options": [10],
    "type": "read"
  },
  {
    "property": "read.split.open-file-cost",
    "description": "The estimated cost to open a file, used as a minimum weight when combining splits.",
    "value": 4,
    "unit": "MB",
    "options": [4],
    "type": "read"
  },
  {
    "property": "read.parquet.vectorization.enabled",
    "description": "Controls whether Parquet vectorized reads are used",
    "value": true,
    "unit": "",
    "options": [true],
    "type": "read"
  },
  {
    "property": "read.parquet.vectorization.batch-size",
    "description": "The batch size for parquet vectorized reads",
    "value": 5000,
    "unit": "",
    "options": [5000],
    "type": "read"
  },
  {
    "property": "read.orc.vectorization.enabled",
    "description": "Controls whether orc vectorized reads are used",
    "value": false,
    "unit": "",
    "options": [false],
    "type": "read"
  },
  {
    "property": "read.orc.vectorization.batch-size",
    "description": "The batch size for orc vectorized reads",
    "value": 5000,
    "unit": "",
    "options": [5000],
    "type": "read"
  },

  {
    "property": "write.format.default",
    "description": "Default file format for the table; parquet, avro, or orc",
    "value": "parquet",
    "unit": "",
    "options": ["parquet"],
    "type": "write"
  },
  {
    "property": "write.delete.format.default",
    "description": "Default delete file format for the table; parquet, avro, or orc",
    "value": "data file format",
    "unit": "",
    "options": ["data file format"],
    "type": "write"
  },
  {
    "property": "write.parquet.row-group-size-bytes",
    "description": "Parquet row group size",
    "value": 128,
    "unit": "MB",
    "options": [128],
    "type": "write"
  },
  {
    "property": "write.parquet.page-size-bytes",
    "description": "Parquet page size",
    "value": 1,
    "unit": "MB",
    "options": [1],
    "type": "write"
  },
  {
    "property": "write.parquet.page-row-limit",
    "description": "Parquet page row limit",
    "value": 20000,
    "unit": "",
    "options": [20000],
    "type": "write"
  },
  {
    "property": "write.parquet.dict-size-bytes",
    "description": "Parquet dictionary page size",
    "value": 2,
    "unit": "MB",
    "options": [2],
    "type": "write"
  },
  {
    "property": "write.parquet.compression-codec",
    "description": "Parquet compression codec: zstd, brotli, lz4, gzip, snappy, uncompressed",
    "value": "zstd",
    "unit": "",
    "options": ["zstd", "brotli", "lz4", "gzip", "snappy", "uncompressed"],
    "type": "write"
  },
  {
    "property": "write.parquet.compression-level",
    "description": "Parquet compression level",
    "value": null,
    "unit": "",
    "options": [null],
    "type": "write"
  },
  {
    "property": "write.parquet.bloom-filter-enabled.column.col1\t",
    "description": "Hint to parquet to write a bloom filter for the column: col1",
    "value": "(not set)",
    "unit": "",
    "options": [null],
    "type": "write"
  },
  {
    "property": "write.parquet.bloom-filter-max-bytes",
    "description": "The maximum number of bytes for a bloom filter bitset",
    "value": 1,
    "unit": "MB",
    "options": [1],
    "type": "write"
  },
  {
    "property": "write.avro.compression-codec",
    "description": "Avro compression codec: gzip(deflate with 9 level), zstd, snappy, uncompressed",
    "value": "gzip",
    "unit": "",
    "options": ["gzip", "zstd", "snappy", "uncompressed"],
    "type": "write"
  },
  {
    "property": "write.avro.compression-level",
    "description": "Avro compression level",
    "value": null,
    "unit": "",
    "options": [null],
    "type": "write"
  },
  {
    "property": "write.orc.stripe-size-bytes",
    "description": "Define the default ORC stripe size, in bytes",
    "value": 64,
    "unit": "MB",
    "options": [64],
    "type": "write"
  },
  {
    "property": "write.orc.block-size-bytes",
    "description": "Define the default file system block size for ORC files",
    "value": 256,
    "unit": "MB",
    "options": [256],
    "type": "write"
  },
  {
    "property": "write.orc.compression-codec",
    "description": "ORC compression codec: zstd, lz4, lzo, zlib, snappy, none",
    "value": "zlib",
    "unit": "",
    "options": ["zlib", "zstd", "lz4", "lzo", "snappy", "none"],
    "type": "write"
  },
  {
    "property": "write.orc.compression-strategy",
    "description": "ORC compression strategy: speed, compression",
    "value": "speed",
    "unit": "",
    "options": ["speed", "compression"],
    "type": "write"
  },
  {
    "property": "write.orc.bloom.filter.columns",
    "description": "Comma separated list of column names for which a Bloom filter must be created",
    "value": "(not set)",
    "unit": "",
    "options": [null],
    "type": "write"
  },
  {
    "property": "write.orc.bloom.filter.fpp",
    "description": "False positive probability for Bloom filter (must > 0.0 and < 1.0)",
    "value": 0.05,
    "unit": "",
    "options": [0.05],
    "type": "write"
  },
  {
    "property": "write.location-provider.impl",
    "description": "Optional custom implementation for LocationProvider",
    "value": null,
    "unit": "",
    "options": [null],
    "type": "write"
  },
  {
    "property": "write.metadata.compression-codec",
    "description": "Metadata compression codec; none or gzip",
    "value": "none",
    "unit": "",
    "options": ["none", "gzip"],
    "type": "write"
  },
  {
    "property": "write.metadata.metrics.max-inferred-column-defaults",
    "description": "Defines the maximum number of columns for which metrics are collected",
    "value": 100,
    "unit": "",
    "options": [100],
    "type": "write"
  },
  {
    "property": "write.metadata.metrics.default",
    "description": "Default metrics mode for all columns in the table; none, counts, truncate(length), or full",
    "value": 16,
    "unit": "",
    "options": ["none","full", 16],
    "type": "write"
  },
  {
    "property": "write.metadata.metrics.column.col1",
    "description": "Metrics mode for column 'col1' to allow per-column tuning; none, counts, truncate(length), or full",
    "value": "",
    "unit": "",
    "options": ["none", "full"],
    "type": "write"
  },
  {
    "property": "write.target-file-size-bytes",
    "description": "Controls the size of delete files generated to target about this many bytes",
    "value": 64,
    "unit": "MB",
    "options": [64],
    "type": "write"
  },
  {
    "property": "write.distribution-mode",
    "description": "Defines distribution of write data: none: don't shuffle rows; hash: hash distribute by partition key ; range: range distribute by partition key or sort key if table has an SortOrder",
    "value": "none",
    "unit": "",
    "options": ["none"],
    "type": "write"
  },
  {
    "property": "write.delete.distribution-mode",
    "description": "False positive probability for Bloom filter (must > 0.0 and < 1.0)",
    "value": 0.05,
    "unit": "",
    "options": [0.05],
    "type": "write"
  },
  {
    "property": "write.update.distribution-mode",
    "description": "Defines distribution of write delete data",
    "value": "hash",
    "unit": "",
    "options": ["hash"],
    "type": "write"
  },
  {
    "property": "write.merge.distribution-mode",
    "description": "Defines distribution of write merge data",
    "value": "none",
    "unit": "",
    "options": ["none"],
    "type": "write"
  },
  {
    "property": "write.wap.enabled",
    "description": "Enables write-audit-publish writes",
    "value": false,
    "unit": "",
    "options": [false],
    "type": "write"
  },
  {
    "property": "write.summary.partition-limit",
    "description": "Includes partition-level summary stats in snapshot summaries if the changed partition count is less than this limit",
    "value": 0,
    "unit": "",
    "options": [0],
    "type": "write"
  },
  {
    "property": "write.metadata.delete-after-commit.enabled",
    "description": "Controls whether to delete the oldest tracked version metadata files after commit",
    "value": false,
    "unit": "",
    "options": [false],
    "type": "write"
  },
  {
    "property": "write.metadata.previous-versions-max",
    "description": "The max number of previous version metadata files to keep before deleting after commit",
    "value": 100,
    "unit": "",
    "options": [100],
    "type": "write"
  },
  {
    "property": "write.spark.fanout.enabled",
    "description": "Enables the fanout writer in Spark that does not require data to be clustered; uses more memory",
    "value": false,
    "unit": "",
    "options": [false],
    "type": "write"
  },
  {
    "property": "write.object-storage.enabled",
    "description": "Enables the object storage location provider that adds a hash component to file paths",
    "value": false,
    "unit": "",
    "options": [false],
    "type": "write"
  },
  {
    "property": "write.data.path",
    "description": "Base location for data files",
    "value": "table location + /data",
    "unit": "",
    "options": ["table location + /data"],
    "type": "write"
  },
  {
    "property": "write.metadata.path",
    "description": "Base location for metadata files",
    "value": "table location + /metadata",
    "unit": "",
    "options": ["table location + /metadata"],
    "type": "write"
  },
  {
    "property": "write.delete.mode",
    "description": "Mode used for delete commands: copy-on-write or merge-on-read (v2 only)\n",
    "value": "copy-on-write",
    "unit": "",
    "options": ["copy-on-write"],
    "type": "write"
  },
  {
    "property": "write.delete.isolation-level",
    "description": "Isolation level for delete commands: serializable or snapshot",
    "value": "serializable",
    "unit": "",
    "options": ["serializable"],
    "type": "write"
  },
  {
    "property": "write.update.mode",
    "description": "Mode used for update commands: copy-on-write or merge-on-read (v2 only)",
    "value": "copy-on-write",
    "unit": "",
    "options": ["copy-on-write"],
    "type": "write"
  },
  {
    "property": "write.update.isolation-level",
    "description": "Isolation level for update commands: serializable or snapshot",
    "value": "serializable",
    "unit": "",
    "options": ["serializable"],
    "type": "write"
  },
  {
    "property": "write.merge.mode",
    "description": "Mode used for merge commands: copy-on-write or merge-on-read (v2 only)",
    "value": "copy-on-write",
    "unit": "",
    "options": ["copy-on-write"],
    "type": "write"
  },
  {
    "property": "write.merge.isolation-level",
    "description": "Isolation level for merge commands: serializable or snapshot",
    "value": "serializable",
    "unit": "",
    "options": ["serializable"],
    "type": "write"
  }
]