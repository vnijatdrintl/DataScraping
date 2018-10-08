import requests, json, time, datetime
from datetime import timedelta

api_key='dxXYILBaKx6puqspbFgCbq30K2l5JflixJLoVgao'

headers={
    'X-API-KEY':api_key
}


def getVotes(start_date):
    date1 = start_date+timedelta(30)
    date1 = date1.strftime('%Y-%m-%d')

    date2 = start_date+timedelta(31)
    date2 = date2.strftime('%Y-%m-%d')

    date3 = start_date+timedelta(60)
    date3 = date3.strftime('%Y-%m-%d')

    date4 = start_date+timedelta(61)
    date4 = date4.strftime('%Y-%m-%d')

    start_date=start_date.strftime('%Y-%m-%d')

    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d')



    r1=requests.get('https://api.propublica.org/congress/v1/both/votes/%s/%s.json'%(start_date,date1),headers=headers)
    j1=json.loads(r1.text)

    r2=requests.get('https://api.propublica.org/congress/v1/both/votes/%s/%s.json'%(date2,date3),headers=headers)
    j2=json.loads(r2.text)

    r3=requests.get('https://api.propublica.org/congress/v1/both/votes/%s/%s.json'%(date4,today),headers=headers)
    j3=json.loads(r3.text)

    results=[j1['results']['votes'],j2['results']['votes'],j3['results']['votes']]

    ans=[]

    for votes in results:
        for vote in votes:

            try:
                id=vote['bill']['bill_id']
            except:
                continue
            if id in ans:
                continue
            else:
                ans.append(id)

    return ans
