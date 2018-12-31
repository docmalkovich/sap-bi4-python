#.Synopsis
#Exports WebI to PDF.
#.Description
#Logs onto BI Platform, retrieves PDF export of a Web Intelligence document and save to specified file.
#Modify this script to enter the logon credentials, URL to the RESTful Web Services, Language, Document SI_ID and folder path.
#.Uses
#Python 3 and SAP BI4.1 SP3+
#Tested with Portable Python 3.2.5.1 on Windows XP and BI4.1 SP3
#.source
#https://blogs.sap.com/2014/10/17/scripting-web-intelligence-the-restful-raylight-web-services-with-python-sample/

import urllib.request
import urllib.parse
import json
import os

############################################################################################################################
# Input: logonInfo, hostUrl, locale, documentId and folderPath to suite your preferences
logonInfo = {
    'userName'    : 'administrator',  
    'password'    : 'Password1',  
    'auth'        : 'secEnterprise'  
}
hostUrl = 'http://10.160.206.89:6405/biprws'
documentId = '7827'       # SI_ID for the document
locale = 'en-US'          # Format language for the WebI exporter
contentLocale = 'en-US'   # Format language for the WebI document contents
folderPath = r'C:\Users\me\Desktop\RESTful'  # Folder where PDF file will be saved.
############################################################################################################################
raylightUrl = hostUrl + '/raylight/v1'
documentUrl = raylightUrl + '/documents/' + documentId 

# Logon and retrieve the logon token to be used in subsequent RESTful calls.
headers = {
    'Content-Type'    : 'application/json',
    'Accept'          : 'application/json',
}
d=str.encode(json.dumps(logonInfo))  
result = urllib.request.urlopen(urllib.request.Request(hostUrl + "/logon/long",d,headers))
reponse=json.loads(result.read().decode('utf-8'))
logonToken=reponse['logonToken']

# Get Web Intelligence document information.
headers = {
    'X-SAP-LogonToken'  : '"'+logonToken+'"' ,  
    'Accept'            : 'application/json',
    'Content-Type'      : 'application/json',
    'Accept-Language'   : locale,
    'X-SAP-PVL'         : contentLocale
}
result = urllib.request.urlopen( urllib.request.Request(documentUrl,None,headers) )
reponse=json.loads(result.read().decode('utf-8'))
document = reponse['document']

# Refresh the document by sending empty prompts (assumes document has no prompts).
headers = {
    'X-SAP-LogonToken' : '"'+logonToken+'"' ,
    'Accept'           : 'application/json' ,
    'Content-Type'     : 'application/json' ,
    'X-SAP-PVL'        : contentLocale
}
parametersUrl = documentUrl + '/parameters'
urllib.request.urlopen( urllib.request.Request(parametersUrl,None,headers) )

# Retrieve and save PDF first ensuring the file path is valid.
filePath = os.path.join(folderPath , document['name'] + '.pdf')
if( os.access(os.path.dirname(filePath), os.W_OK) ) :
    # Get PDF and save to file
    headers = { 
        'X-SAP-LogonToken' : '"'+logonToken+'"' ,
        'Accept'           : 'application/pdf' ,
        'X-SAP-PVL'        : contentLocale
    }
    result = urllib.request.urlopen( urllib.request.Request(documentUrl + '/pages',None,headers) )
    f = open(filePath, 'wb')
    f.write(result.read())
    f.close()
else :
    print ('Invalid file path ' + filePath)

# Unload document from Raylight.
headers = { 
    'X-SAP-LogonToken' : '"'+logonToken+'"' ,
    'Accept'           : 'application/json' ,
    'Content-Type'     : 'application/json' ,
    'X-SAP-PVL'        : contentLocale
}
data = {  
  'document' : { 'state' : 'Unused' }  
}    
d=str.encode(json.dumps(data)) 
urllib.request.urlopen(urllib.request.Request(documentUrl,d,headers))

# Log off the Session identified by the X-SAP-LogonToken HTTP Header
headers = { 
    'X-SAP-LogonToken' : '"'+logonToken+'"' ,
    'Accept'           : 'application/json' ,
    'Content-Type'     : 'application/json' 
}
urllib.request.urlopen(urllib.request.Request(hostUrl + '/logoff',b'',headers))


              



