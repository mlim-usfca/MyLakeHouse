#!/bin/sh

# Wait until MinIO is available and configure mc
until /usr/bin/mc config host add minio http://minio:9000 admin password; do
  echo 'Waiting for MinIO...'
  sleep 1
done

# Check if the 'warehouse' bucket exists, create it if it doesn't
if ! /usr/bin/mc ls minio/warehouse; then
  /usr/bin/mc mb minio/warehouse
  /usr/bin/mc policy set public minio/warehouse
else
  echo 'Bucket already exists.'
fi

# Keep the container running
tail -f /dev/null
