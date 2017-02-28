#!/usr/bin/python

import pymysql
import shlex, subprocess
import sys
from datetime import datetime
import requests
import json

def grantaccess(ip_src):
   
   url = 'http://127.0.0.1:8080/myswitch/cmd/2'
   payload = {'cmd': '2'}
   payload["ip_src"]= ip_src
   # Create your header as required
   headers = {"content-type": "application/json", "Authorization": "<auth-key>" }

   r = requests.put(url, data=json.dumps(payload), headers=headers)


conn = pymysql.connect(host='localhost', user='root', passwd='root', db='ovsDB')
cur = conn.cursor()
cur.execute("SELECT * FROM nmap_queue WHERE CHK_Status ='New'") 
scanlist= []
results = cur.fetchall()
           # Check if anything at all is returned
for row in results:  

   print "True"
   sid = row[0]
   sip = row[1]
   #add this into a tuple
   print sid
   print sip
   scanlist.append((sid,sip))
cur.close()
#insert 2nd loop here
cur2 = conn.cursor()
for pc in scanlist:
   sid, sip = pc  
   cur2.execute("UPDATE nmap_queue SET CHK_Status='Pending' WHERE ID=%s AND IP_ADDR=%s", (sid, sip))
conn.commit()
cur2.close()
#insert a 3rd loop here
cur3=conn.cursor()
for pc in scanlist:
   sid, sip = pc 
   cur3.execute("UPDATE nmap_queue SET CHK_Status='Scanning' WHERE ID=%s AND IP_ADDR=%s", (sid, sip))
   conn.commit()
   filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")+" "+sip
  
   proc = subprocess.call(["nmap", "-oN", "/home/faucet/ryu/ryu/app/nmapscans/"+filename1, sip])
   
   file = open("/home/faucet/ryu/ryu/app/nmapscans/"+filename1, "r")
   file_content = file.read()
   word = "open"
   query = "UPDATE nmap_queue SET Scan_Results = %s, CHK_Status = 'Cleared' WHERE ID =%s AND IP_ADDR =%s"
   if file_content.find(word) != -1:
      query = "UPDATE nmap_queue SET Scan_Results = %s, CHK_Status = 'Denied' WHERE ID =%s AND IP_ADDR =%s"
      query0 = "UPDATE nmap_queue SET Sec_Status = 'F' WHERE ID = %s AND IP_ADDR = %s"
      cur3.execute(query0, (sid, sip))
   else:
      
      grantaccess(sip)
      
      query2 = "UPDATE nmap_queue SET Sec_Status = 'T' WHERE ID = %s AND IP_ADDR = %s"
   
      cur3.execute(query2, (sid, sip))     
   file.close()

   print query
   cur3.execute(query, (file_content,sid,sip))

   conn.commit()
cur3.close()
conn.close()
