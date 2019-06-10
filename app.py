from prometheus_client import start_http_server, Gauge, Counter
import os
# import subprocess
import time
import schedule

env_host = os.environ['PING_HOST']

ping_time = Gauge('ping_time', 'Ping Latency Time')
ping_status = Gauge('ping_status', 'Host Reachable')
ping_uptime = Counter('ping_uptime', 'Uptime of host in seconds (updated every 10 seconds)')

def ping_host(host):
    # TODO: Implement with subprocess and get ping time from output
    # with open(os.devnull, 'wb') as devnull:
    #     subprocess.check_call(['ping -c 1 ' + host], stdout=devnull, stderr=devnull)
    if os.system('ping -c 1 ' + host) == 0:
        return True
    else:
        return False

def check_host_availability(host):
    @ping_time.time()
    def do_ping():
        return ping_host(host)
    if do_ping():
        ping_status.set(1)
        ping_uptime.inc(10)
    else:
        ping_status.set(0)

def scheduled_run():
    check_host_availability(env_host)

if __name__ == '__main__':
    start_http_server(8000)
    schedule.every(10).seconds.do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)