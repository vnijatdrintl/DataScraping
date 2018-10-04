import requests, zipfile, io


def download(folder_path):

    r1 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/sres/BILLSTATUS-115-sres.zip')
    print('Request 1 (sres) Status Code: {}'.format(r1))
    z1 = zipfile.ZipFile(io.BytesIO(r1.content))
    z1.extractall(folder_path)


    r2 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/sjres/BILLSTATUS-115-sjres.zip')
    print('Request 2 (sjres) Status Code: {}'.format(r2))
    z2 = zipfile.ZipFile(io.BytesIO(r2.content))
    z2.extractall(folder_path)

    r3 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/sconres/BILLSTATUS-115-sconres.zip')
    print('Request 3 (sconres) Status Code: {}'.format(r3))
    z3 = zipfile.ZipFile(io.BytesIO(r3.content))
    z3.extractall(folder_path)

    r4 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115-s.zip')
    print('Request 4 (s) Status Code: {}'.format(r4))
    z4 = zipfile.ZipFile(io.BytesIO(r4.content))
    z4.extractall(folder_path)

    r5 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hres/BILLSTATUS-115-hres.zip')
    print('Request 5 (hres) Status Code: {}'.format(r5))
    z5 = zipfile.ZipFile(io.BytesIO(r5.content))
    z5.extractall(folder_path)

    r6 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115-hr.zip')
    print('Request 6 (hr) Status Code: {}'.format(r6))
    z6 = zipfile.ZipFile(io.BytesIO(r6.content))
    z6.extractall(folder_path)

    r7 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hjres/BILLSTATUS-115-hjres.zip')
    print('Request 7 (hjres) Status Code: {}'.format(r7))
    z7 = zipfile.ZipFile(io.BytesIO(r7.content))
    z7.extractall(folder_path)

    r8 = requests.get('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hconres/BILLSTATUS-115-hconres.zip')
    print('Request 8 (hconres) Status Code: {}'.format(r8))
    z8 = zipfile.ZipFile(io.BytesIO(r8.content))
    z8.extractall(folder_path)
