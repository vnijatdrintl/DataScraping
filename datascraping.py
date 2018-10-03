import requests
import xml.etree.ElementTree as ET
import json
from datetime import timedelta
import datetime
from lxml import etree
import time


start_time=time.time()

def constructBillID(billType,billNumber):

    billType='.'.join(billType.upper())
    billID=billType+'.'+str(billNumber)+'-115'

    return billID


#get date
today = datetime.datetime.today()
s_date = today-timedelta(90)
s_date = s_date.strftime('%Y-%m-%d')


#use api to retrieve all the information
#make sure to modify the date parameter
api_key = 'Cmb2yQaN2Pc3aM3TvewSxZ8qrN79M1gZ0b8taMgH'

i=0

url = 'https://api.govinfo.gov/collections/BILLS/%sT00:00:00Z/?offset=0&pageSize=100&api_key=%s'%(s_date,api_key)
response = requests.get(url)
i+=1
print('initial response:',response.status_code)

with open('U:\\datascraping\\test.xml','w',encoding='utf-8') as f:
    f.write('<bills>')

    #load collection to a json object
    bills = json.loads(response.text)
    nextPage = bills['nextPage']

    j=0

    while nextPage != None:

        nextPage = bills['nextPage']
        packages = bills['packages']

        for package in packages:
            packageId = package['packageId']

            #check if it's from 115th congress
            if '-115' in packageId:

                #get info
                #construct summary URL
                pageLink = package['packageLink']
                summaryURL = '%s?api_key=%s'%(pageLink,api_key)

                summaryRequest = requests.get(summaryURL)
                j+=1

                while summaryRequest.status_code==503:
                    summaryRequest = requests.get(summaryURL)

                print('summary response:',summaryRequest.status_code)
                summaryJson = json.loads(summaryRequest.text)

                #f.write('<bill>')

                billTiltle = summaryJson['title']
                #f.write('<billTiltle>%s</billTiltle>'%billTiltle)

                #no category ID available
                billCategory = summaryJson['category']
                #f.write('<billCategory>%s</billCategory>'%billCategory)

                billType = summaryJson['billType']
                #f.write('<billType>%s</billType>'%billType)

                billNumber = summaryJson['billNumber']
                #f.write('<billNumber>%s</billNumber>'%billNumber)

                billID = constructBillID(billType,billNumber)
                #f.write('<billID>%s</billID>'%billID)

                #get detail info:summary, introduced date,and status
                billStatusLink=summaryJson['related']['billStatusLink']
                billStatusRequest=requests.get(billStatusLink)

                print('status response:',summaryRequest.status_code)
                billStatusET=ET.fromstring(billStatusRequest.content)

                billIntroducedDate=billStatusET.findall('bill/actions/item/actionDate')[-1].text

                date=datetime.datetime.strptime(billIntroducedDate,"%Y-%m-%d")
                s_date = today-timedelta(90)

                if date<s_date:
                    continue

                f.write('<bill>')
                f.write('<billTiltle>%s</billTiltle>'%billTiltle)
                f.write('<billCategory>%s</billCategory>'%billCategory)
                f.write('<billType>%s</billType>'%billType)
                f.write('<billNumber>%s</billNumber>'%billNumber)
                f.write('<billID>%s</billID>'%billID)
                f.write('<billIntroducedDate>%s</billIntroducedDate>'%billIntroducedDate)

                billStatus=billStatusET.findall('bill/latestAction/text')[0].text
                f.write('<billStatus>%s</billStatus>'%billStatus)

                #some bills dont have summaries
                if len(billStatusET.findall('bill/summaries/billSummaries/item/text'))>0:
                    billSummary=billStatusET.findall('bill/summaries/billSummaries/item/text')[0].text
                else:
                    billSummary=''
                f.write('<billSummary><![CDATA[%s'%billSummary)
                f.write(' ]]>')
                f.write('</billSummary>')
                f.write('</bill>')


            else:
                continue
        #just for testing
        #break
        if nextPage==None:
            break
        #time.sleep(100)
        url='%s&api_key=%s'%(nextPage,api_key)
        response = requests.get(url)
        i+=1
        print('\n')
        print('nextpage response:',response.status_code)
        print('\n')
        bills = json.loads(response.text)

    f.write('</bills>')

end_time=time.time()

run_time=end_time-start_time
print(run_time)