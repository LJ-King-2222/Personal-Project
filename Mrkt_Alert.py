import os
import smtplib
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import time

EMAIL_ADDRESS ='this is your username'
EMAIL_PASSWORD ='This is your password'

msg = EmailMessage()

yf.pdr_override() # <== that's all it takes :-)

#This is the start date of when you want data to begin and sets to realtime whenever program is generated.
start =dt.datetime(2022,4,20)
now = dt.datetime.now()

stock="TSLA"
TargetPrice=130

#Choose the Subject line and where you want to send email.
msg['Subject'] = 'Alert on '+ stock+'!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'desiredrecepient@yahoo.com'

#Boolean phrase to make sure email isn't sent too many times.
alerted=False

#Here is where I begin a while loop. While 1: refers to it being always true.
while 1:
#These next two lines of code access the most recent stock price
	df = pdr.get_data_yahoo(stock, start, now)
	currentClose=df["Adj Close"][-1]
    
#Now we will create a boolean variable set to currenmt close greater than target price, in the loop it will be true if condition holds and otherwise false.
	condition=currentClose>TargetPrice
    
#Here we create an if statement of when email alert should be sent or not. The alerted=True line means that it will make sure you aren't emailed.
	if(condition and alerted==False):

		alerted=True

		message=stock +" Has activated the alert price of "+ str(TargetPrice) +\
		 "\nCurrent Price: "+ str(currentClose)

		print(message)
# Now lets set that to message of object      
		msg.set_content(message)
#Here in the following block until the email content (@ line 65) below is optional code if you want to send documents in your code. 
		files=[r"C:\\Users\\LJone\\Fin510\\ALERT\\FundamentalList.xlsx"]
#Here is a for loop where 
		for file in files:
			with open(file,'rb') as f:
				file_data=f.read()
				file_name="FundamentalList.xlsx"
#This is where we add the optional excel document information into the email.
				msg.add_attachment(file_data, maintype="application",
					subtype='ocetet-stream', filename=file_name)

#This is where we login to our email information and send the email when condition is true
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		    smtp.send_message(msg)

		    print("completed")
	else:
		print("No new alerts")
        #This next line will pause the program and run it every 60 seconds
	time.sleep(60)
