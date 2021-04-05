
from jira import JIRA
import json
import requests
import getpass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas.io.json import json_normalize
import time
import datetime
import matplotlib.patches as patches
import numpy as np
from pandas.tseries.offsets import BDay
from PIL import Image, ImageFont, ImageDraw
import textwrap
from apscheduler.schedulers.blocking import BlockingScheduler
start = time.perf_counter()


font = ImageFont.truetype("arial.ttf", 1)
#Get User credentials for JIRA authorization
username = input('Enter your user name: ')
password = getpass.getpass(prompt="Enter Password")
jira = JIRA(basic_auth = (username, password), options = {'server': 'https://jira.troweprice.com'})
x, y = 30, 10
x2, y2 = 300, 500
pointsize = 30
fillcolor = "white"
shadowcolor = "white"

badList=[]
warningList=[]
def targetdatealert():
    today = datetime.date.today()
    priority = jira.search_issues('filter = 48302')
    for issue in priority:
        currentID = issue.key
        targetdelivery = datetime.datetime.strptime(issue.fields.customfield_21501, '%Y-%m-%d')
        days = np.busday_count(today, targetdelivery.date())
        pointsAvailable = days * 2
        pointsOutstanding = 0
        for link in issue.fields.issuelinks:
            if hasattr(link, "outwardIssue"):
                outwardIssue = link.outwardIssue
                if "NYCIO" in outwardIssue.key:
                    if (outwardIssue.fields.status.name not in 'QA' and outwardIssue.fields.status.name not in 'Accepted' and outwardIssue.fields.status.name not in 'Rejected' and outwardIssue.fields.status.name not in 'Released'):
                        link = jira.issue(outwardIssue.key)
                        if link.fields.customfield_10502 is not None:
                            pointsOutstanding = pointsOutstanding + link.fields.customfield_10502
            elif hasattr(link, "inwardIssue"):
                inwardIssue = link.inwardIssue
                if "NYCIO" in inwardIssue.key:
                    if (inwardIssue.fields.status.name not in 'QA' and inwardIssue.fields.status.name not in 'Accepted' and inwardIssue.fields.status.name not in 'Rejected' and inwardIssue.fields.status.name not in 'Released'):
                        link = jira.issue(inwardIssue.key)
                        if link.fields.customfield_10502 is not None:
                            pointsOutstanding = pointsOutstanding + link.fields.customfield_10502
        #print(f'Key: {currentID} Points Available: {pointsAvailable} Points Outstanding: {pointsOutstanding}')
        if (pointsOutstanding > pointsAvailable and currentID not in badList):
            badList.append(currentID)
            text= currentID + " will land on time. FALSE.  There are " + str(pointsOutstanding) + " points outstanding and " + str(pointsAvailable) + " points of capacity availble"
            # thin border
            memerizer(text, 1, currentID, pointsOutstanding, pointsAvailable)
            '''
            draw = ImageDraw.Draw(alert)
            text1 = currentID + "will land on time"
            text2 = "FALSE.  There are " + str(pointsOutstanding) + " points outstanding and " + str(pointsAvailable) + " points of capacity availble"
            # thin border
            draw.text((x-1, y), text1, font=font, fill=shadowcolor)
            draw.text((x+1, y), text1, font=font, fill=shadowcolor)
            draw.text((x, y-1), text1, font=font, fill=shadowcolor)
            draw.text((x, y+1), text1, font=font, fill=shadowcolor)
            draw.text((x-1, y), text2, font=font, fill=shadowcolor)
            draw.text((x+1, y), text2, font=font, fill=shadowcolor)
            draw.text((x, y-1), text2, font=font, fill=shadowcolor)
            draw.text((x, y+1), text2, font=font, fill=shadowcolor)
            # thicker border
            draw.text((x-1, y-1), text1, font=font, fill=shadowcolor)
            draw.text((x+1, y-1), text1, font=font, fill=shadowcolor)
            draw.text((x-1, y+1), text1, font=font, fill=shadowcolor)
            draw.text((x+1, y+1), text1, font=font, fill=shadowcolor)
            draw.text((x-1, y-1), text2, font=font, fill=shadowcolor)
            draw.text((x+1, y-1), text2, font=font, fill=shadowcolor)
            draw.text((x-1, y+1), text2, font=font, fill=shadowcolor)
            draw.text((x+1, y+1), text2, font=font, fill=shadowcolor)
            draw.text((10, 10), text1, font = font, fill = fillcolor)

            alert.save('O:/alert2.jpg')
            files = {
            "message": '<messageML> !!!!ALERT!!!: '+currentID +' is NOT projected to meet delivery date!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' </messageML>'
            }
            url = 'https://prodsymib.troweprice.com/integration/v1/whi/simpleWebHookIntegration/5948074ce4b00855c258bcaa/602ffcc998ace369120dfbc2'
            #print(files)
            r = requests.post(url, files=files,  verify=False)
            '''
        if (pointsAvailable > 0 and pointsOutstanding-pointsAvailable > 0 and pointsOutstanding-pointsAvailable < 5 and currentID not in warningList and currentID not in badList):
            warningList.append(currentID)
            text = "I see you like to live dangerously " + currentID + " has " +str(pointsOutstanding) + " and " + str(pointsAvailable) + " of capacity available"
            memerizer(text, 0, currentID, pointsOutstanding, pointsAvailable)
            '''
            files = {
            "message": '<messageML> Warning: ticket '+currentID +' is at risk for meeting projected delivery date!!!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' </messageML>'
            }
            url = 'https://prodsymib.troweprice.com/integration/v1/whi/simpleWebHookIntegration/5948074ce4b00855c258bcaa/602ffcc998ace369120dfbc2'
            #print(files)
            r = requests.post(url, files=files,  verify=False)
            '''
        if (pointsOutstanding <= pointsAvailable and currentID in badList):
            badList.remove(currentID)
        if  (pointsAvailable > 0 and pointsOutstanding-pointsAvailable > 0 and pointsOutstanding-pointsAvailable >= 5 and currentID in warningList):
            warningList.remove(currentID)
def memerizer(text, type, currentID, pointsOutstanding, pointsAvailable):
    if type == 1:
        image = Image.open("Dwight.jpg")
        color = "red"
        files = {
        "message": '<messageML> !!!!ALERT!!!: '+currentID +' is NOT projected to meet delivery date!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' <img src="C:\\Users\\' + username + '\\OneDrive - TRowePrice\\meme.jpg"/> </messageML>'
        }
    else:
        image = Image.open("Wonka.jpg")
        color = "yellow"
        files = {
        "message": '<messageML> Warning: ticket '+currentID +' is at risk for meeting projected delivery date!!!  Points Outstanding: ' + str(pointsOutstanding)+' Capacity Availble:'+str(pointsAvailable)+' <img src="C:\\Users\\' + username + '\\OneDrive - TRowePrice\\meme.jpg"/> </messageML>'
        }
    width, height = image.size
    font_type = ImageFont.truetype("arial.ttf", 40)
    font_type2 = ImageFont.truetype("arial.ttf", 15)
    draw = ImageDraw.Draw(image)
    if len(text) > 18:
        split = textwrap.wrap(text, 29)
        draw.text(xy=(10,10), text=split[0], fill=(color), font = font_type)
        draw.text(xy=(12,12), text=split[0], fill=(0,0,0), font=font_type)
        y1 = height - 102
        y2 = height - 100
        draw.text(xy=(10,y1), text=split[1] + " " + split[2] + " " + split[3], fill=(color), font = font_type2)
        draw.text(xy=(12,y2), text=split[1] + " " + split[2] + " " + split[3], fill=(0,0,0), font = font_type2)

        '''
        y3 = height -122
        y4 = height -100
        draw.text(xy=(10,y3), text=split[2], fill=(color), font = font_type)
        draw.text(xy=(12,y4), text=split[2], fill=(0,0,0), font = font_type)
        '''
    image.save('C:\\Users\\' + username + '\\OneDrive - TRowePrice\\meme.jpg')
    url = 'https://prodsymib.troweprice.com/integration/v1/whi/simpleWebHookIntegration/5948074ce4b00855c258bcaa/602ffcc998ace369120dfbc2'
    r = requests.post(url, files=files,  verify=False)
    #image.show()
targetdatealert()
scheduler = BlockingScheduler()
scheduler.add_job(targetdatealert, 'interval', minutes=15)
scheduler.start()
