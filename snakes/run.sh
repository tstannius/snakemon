#!/bin/bash

set -euo pipefail

TARGET=$1

rm -rf tmp
rm -rf out

snakemake $TARGET -j1 -p --forceall --wms-monitor http://127.0.0.1:8000
