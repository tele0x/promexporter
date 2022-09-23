import os, sys, time, requests, csv
from datetime import datetime
from prometheus_client import Gauge, start_http_server

def log(msg):
    print('[%s] %s' % (datetime.now().strftime('%m/%d/%Y %H:%M:%S'), msg))

class PromMetrics:
    
    def __init__(self, data_file, polling_interval_seconds=10):
        self.polling_interval_seconds = polling_interval_seconds
        self.data_file = data_file
        
        # Metrics definition
        self.total_power_usage_watt = Gauge('total_power_usage_watt', 'Total power uage in watt')


    def fetch(self):
        with open(self.data_file, newline='') as csv_file:
            metrics_reader = csv.DictReader(csv_file)
            for row in metrics_reader:
                log('Update metric total_power_usage_watt value %s' % row['total_power_usage_watt'])
                self.total_power_usage_watt.set(row['total_power_usage_watt'])
            

    def metrics_loop(self):
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

if __name__ == '__main__':

    polling_interval_seconds = int(os.getenv('POLLING_INTERVAL_SECONDS'))
    exporter_port = int(os.getenv('EXPORTER_PORT', '9004'))
    data_file = str(os.getenv('DATA_FILE'))
    
    newton_metrics = PromMetrics(data_file, polling_interval_seconds)

    log('Polling interval set to %s seconds' % os.getenv('POLLING_INTERVAL_SECONDS'))
    log('Data file: %s' % data_file)

    if os.path.isfile(data_file):
        log('Start exporter on port %s' % exporter_port)
        start_http_server(exporter_port)
        newton_metrics.metrics_loop()
    else:
        log('NO DATA FILE FOUND')
        sys.exit(1)
