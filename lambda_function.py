import datetime
import json

import dateutil.tz
import urllib3


def lambda_handler(event, context):
    today = datetime.datetime.now(dateutil.tz.gettz('Asia/Kolkata'))
    cowin_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=262524&date={today.day}-{today.month}-{today.year}"
    print(f"connecting to {cowin_url}")

    apptype_header = {
        'Content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Origin': 'https://www.cowin.gov.in',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.cowin.gov.in/',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }

    http = urllib3.PoolManager()

    response = http.request('GET', url=cowin_url, headers=apptype_header)
    if response.status != 200:
        raise Exception(f"API call failed {response.__dict__}")

    response = json.loads(response.data)
    centers = response['centers']
    
    _18_plus = [
        {'name': x['name'], 'details': {key: val for key, val in session.items() if key in ['date', 'available_capacity']}}
        for x in centers
        for session in x['sessions']
        if session['min_age_limit'] == 18 and session['available_capacity'] > 0
    ]

    print(_18_plus)

    if _18_plus:
        return {
            'statusCode': 200,
            'body': json.dumps(_18_plus)
        }

    raise Exception(f"No 18+ slots available {response}")
