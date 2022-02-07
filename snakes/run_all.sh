#!/bin/bash

set -euo pipefail

TARGET=all

rm -rf tmp
rm -rf out

snakemake $TARGET \
    -j1 -p \
    --forceall \
    --wms-monitor http://127.0.0.1:8000/smk \
    --wms-monitor-arg workflow=NGS name=210101_MYRUN
