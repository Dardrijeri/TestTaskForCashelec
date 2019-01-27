import requests
import datetime
import threading
import numpy
import time
from io import BytesIO


class ThreadRequest(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number
        self.time = 0
        self.passed = True

    def run(self):
        print('Starting Test #{0}'.format(self.number))
        key = 'f311265c-a018-4ed2-8d91-88f18ffb5253'
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        params = {'limit': '10', 'sort': 'volume_24h'}

        r = requests.get(url, headers={'X-CMC_PRO_API_KEY': key}, params=params, stream=True)
        self.process_request(r)

    def process_request(self, r):
        self.check_size(r)
        self.check_date(r)
        self.check_response_time(r)
        if self.passed:
            print('Test #{0} passed'.format(self.number))
        else:
            print('Test #{0} failed'.format(self.number))

    def check_date(self, response):
        data = response.json()
        current_date = str(datetime.date.today())
        for i in range(10):
            date = data['data'][i]['last_updated'][:10]
            if date != current_date:
                self.passed = False
                break

    def check_size(self, request):
        raw_data = request.raw.read()
        size = len(raw_data)
        request.raw._fp = BytesIO(raw_data)
        if size > 10000:
            self.passed = False

    def check_response_time(self, request):
        self.time = request.elapsed.total_seconds()
        if self.time > 0.5:
            self.passed = False


def main():
    all_time = []
    all_threads = []
    failed_threads = []
    current_time = time.time()

    for i in range(8):
        thread = ThreadRequest(i+1)
        all_threads.append(thread)
        thread.start()

    while threading.active_count() != 1:
        pass

    rps = 8 / (time.time() - current_time)

    for thread in all_threads:
        all_time.append(thread.time)
        if not thread.passed:
            failed_threads.append(thread.number)
    latency = numpy.percentile(all_time, 80)
    if latency > 0.450 or rps < 5 or failed_threads != []:
        print("Overall test failed")
    else:
        print("Overall test passed")
    print("80% latency : {0}, rps : {1}, failed tests : {2}".format(latency, rps, failed_threads))

if __name__ == "__main__":
    main()
