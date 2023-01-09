# Youtube_analytics

This is a python program to analyse our youtube analytics from Google Takeout data.

To run this programm you have to :

  #1 - Download on https://takeout.google.com/settings/takeout your Youtube Data JSON files.
  
  #2 - Place the github folder in the folder Youtube data names : 'Youtube and Youtube Music'
  
  #3 - Run Number_api_key.py and notes this number (i hope, his is under or equal to 10 otherwise it is dead. In fact, Google autorize only 10 API key for 10,000 request for each per day)
  
  #4 - Go to https://console.cloud.google.com/ to take the number API key you needed.
     1) Sign in ou sign up with a Google account
     2) Creat a new project
     3) Go to dashbord, scroll down and click on 'explore and activate APIs' in 'First Step' section
     4) On the top click on 'Activate APIs and the services'
     5) Choose 'Youtube Data API v3' and active it
     6) Click on 'Create Identifiers on the top right
     7) Click on 'Public Data' and 'Next'
     8) Copy this API Key
     
 #5 Repeat this eight steps for the number of API key you needed in #3 step
 
 #6 Paste all of your API key in the list 'list_KEY' in the python programm 'Youtube_analytics.py'
 
 #7 Run it 
