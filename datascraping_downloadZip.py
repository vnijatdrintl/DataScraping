import xml.etree.ElementTree as ET
from datetime import timedelta
import datetime, os, time, re
from lxml import etree
import downloadBills
from tkinter import filedialog
import tkinter as tk
from getVotes import getVotes

start_time=time.time()

# def constructBillID(billType,billNumber):
#
#     billType='.'.join(billType.upper())
#     billID=billType+'.'+str(billNumber)+'-115'
#
#     return billID

def constructBillID(billType,billNumber):

    billID=billType.lower()+str(billNumber)+'-115'

    return billID

#get date
today = datetime.datetime.today()
s_date = today-timedelta(90)

votes=getVotes(s_date)
print(votes)

root = tk.Tk()
root.withdraw()
folder_path=filedialog.askdirectory()
downloadBills.download(folder_path)

with open('U:\\datascraping\\test.xml','w',encoding='utf-8') as f:
    f.write('<bills>')

    os.chdir(folder_path)

    for file in os.listdir(folder_path):
        filename=os.fsdecode(file)

        if filename.endswith('.xml'):

            billStatusET=ET.parse(filename)

            regex = re.compile(r"&(?!amp;)")

            billIntroducedDate=billStatusET.findall('bill/actions/item/actionDate')[-1].text
            date=datetime.datetime.strptime(billIntroducedDate,"%Y-%m-%d")

            billNumber=billStatusET.findall('bill/billNumber')[0].text
            billType=billStatusET.findall('bill/billType')[0].text
            billID=constructBillID(billType,billNumber)
            print(billID)

            if date<s_date or billID in votes:
                continue

            # "billCategory" pulled from "<policyArea><name>"
            if len(billStatusET.findall('bill/policyArea/name'))>0:
                billCategory=billStatusET.findall('bill/policyArea/name')[0].text
            else:
                billCategory=''

            #no billCategoryID found

            billTitle=billStatusET.findall('bill/title')[0].text
            billStatus=billStatusET.findall('bill/latestAction/text')[0].text

            if len(billStatusET.findall('bill/summaries/billSummaries/item/text'))>0:
                billSummary=billStatusET.findall('bill/summaries/billSummaries/item/text')[0].text
            else:
                billSummary=''

            f.write('<bill>')

            billID=regex.sub("&amp;", billID)
            f.write('<billID>%s</billID>'%billID)

            billType=regex.sub("&amp;", billType)
            f.write('<billType>%s</billType>'%billType)

            billNumber=regex.sub("&amp;", billNumber)
            f.write('<billNumber>%s</billNumber>'%billNumber)

            billCategory=regex.sub("&amp;", billCategory)
            f.write('<billCategory>%s</billCategory>'%billCategory)

            #billCategoryID n/a
            billTitle=regex.sub("&amp;", billTitle)
            f.write('<billTiltle>%s</billTiltle>'%billTitle)

            billStatus=regex.sub("&amp;", billStatus)
            f.write('<billStatus>%s</billStatus>'%billStatus)

            billIntroducedDate=regex.sub("&amp;", billIntroducedDate)
            f.write('<billIntroducedDate>%s</billIntroducedDate>'%billIntroducedDate)

            f.write('<billSummary><![CDATA[%s'%billSummary)
            f.write(' ]]>')
            f.write('</billSummary>')
            f.write('</bill>')

    f.write('</bills>')

end_time=time.time()

run_time=end_time-start_time
print(run_time/ 60)
