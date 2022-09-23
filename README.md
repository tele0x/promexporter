# Example prometheus sidecar container

Use this container as a sidecar to expose metrics for prometheus
Set the following env variables on your deployment yaml file:

DATA_FILE cvs data file containing the metrics
POLLING_INTERVAL_SECONDS how often the data file is read
EXPORTER_PORT Default port 9004

Container already available for use: quay.io/ferossi/promexporter
