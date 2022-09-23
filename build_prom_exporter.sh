#!/usr/bin/env bash
##
## Container build for prom-exporter
##

# Exit script on first error
set -o errexit

# Use UBI python as base container image
container=$(buildah --name promexporter from registry.access.redhat.com/ubi8/python-38)

buildah config --label maintainer="Federico 'tele' Rossi <ferossi@redhat.com>" $container

# Install packages
buildah run $container pip3 install requests prometheus-client

buildah config --user 1000:1000 $container
# default values
buildah config --env EXPORTER_PORT=9004 --env POLLING_INTERVAL_SECONDS=30 $container

# Copy promexporter
buildah copy $container promexporter.py

# example dummy data
buildah config --cmd 'echo "total_power_usage_watt\n50" > /tmp/metrics.csv' $container

buildah config --cmd 'python3.8 promexporter.py' $container

# Commit to local container storage
buildah commit $container promexporter
