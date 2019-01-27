import requests
import datetime
from io import BytesIO


def check_date(response):
    data = response.json()
    current_date = str(datetime.date.today())
    for i in range(10):
        name = data['data'][i]['name']
        date = data['data'][i]['last_updated'][:10]
        if date != current_date:
            print('Date for {0} is {1}, current is {2}'.format(name, date, current_date))
            return False
    print('Date of update is {0}'.format(current_date))
    return True


def check_size(request):
    raw_data = request.raw.read()
    size = len(raw_data)
    request.raw._fp = BytesIO(raw_data)
    if size > 10000:
        print('Received size is {0} byte, max possible is {1} byte'.format(size, 10000))
        return False
    print('Received size is {0} byte'.format(size))
    return True


def check_response_time(request):
    time = request.elapsed.total_seconds()
    if time > 0.5:
        print('Response time is {0} seconds, max possible is {1} seconds'.format(time, 0.5))
        return False
    print('Response time is {0} seconds'.format(time))
    return True


def print_clear_data(request):
    data = request.json()
    for i in range(10):
        name = data['data'][i]['name']
        volume = data['data'][i]['quote']['USD']['volume_24h']
        print('{0}. {1} : {2}'.format(i+1, name, volume))


key = 'f311265c-a018-4ed2-8d91-88f18ffb5253'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
params = {'limit': '10', 'sort': 'volume_24h'}

r = requests.get(url, headers={'X-CMC_PRO_API_KEY': key}, params=params, stream=True)

if check_size(r) and check_response_time(r) and check_date(r):
    print("Test passed")
print_clear_data(r)
