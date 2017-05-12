#!/usr/bin/env bash
set -e


docker build -t test/nc_gdx .
docker run \
    --env NC_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/nc_gdx:/nc_gdx \
    -v$GDX_DATA:/gdx_data \
    -v${GDX_BIN}/gdx:/usr/local/bin/gdx \
    test/nc_gdx
