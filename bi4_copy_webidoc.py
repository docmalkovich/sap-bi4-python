# python 3.7
# ouvre un doc X dans le dossier A et le copie/écrase le doc X dans le dossier B
#   permet de garder la planif ...
# copy multiple webi docs, overwrite, keep scheduling

import urllib.request
import urllib.parse
import json
import os

############################################################################################################################
# Input: logonInfo, hostUrl, locale, documentId and folderPath to suite your preferences
logonInfo = {
    'userName'    : 'user',  
    'password'    : 'password',  
    'auth'        : 'secEnterprise'  
}
hostUrl = 'http://bi4servername:6405/biprws'
locale = 'en-US'          # Format language for the WebI exporter
contentLocale = 'en-US'   # Format language for the WebI document contents
############################################################################################################################

raylightUrl = hostUrl + '/raylight/v1'
# documentUrl = raylightUrl + '/documents/' + documentIdSrc 

# Logon and retrieve the logon token to be used in subsequent RESTful calls.
headers = {
    'Content-Type'    : 'application/json',
    'Accept'          : 'application/json',
}
d=str.encode(json.dumps(logonInfo))  # le str.encode convertit le string en bytes
print("Login BI4")
result = urllib.request.urlopen(urllib.request.Request(hostUrl + "/logon/long",d,headers))
reponse=json.loads(result.read().decode('utf-8'))
logonToken=reponse['logonToken']

# copy doc
def copyDoc(IdDocSrc, IdFldTgt):
    headers = {
        'X-SAP-LogonToken' : '"'+logonToken+'"' ,
        'Accept'           : 'application/json' ,
        'Content-Type'     : 'application/json' ,
        'X-SAP-PVL'        : contentLocale
    }
    # documentUrl = raylightUrl  + '/documents?sourceId=' + IdDocSrc
    documentUrl = raylightUrl  + '/documents/' + IdDocSrc
    data = {  
      'document' : { 'folderId' : IdFldTgt }  
    }    
    d=str.encode(json.dumps(data))  # le str.encode convertit le string en bytes
    result = urllib.request.urlopen(urllib.request.Request(documentUrl,d,headers))
    reponse=json.loads(result.read().decode('utf-8'))
    print(reponse)

# copie des docs !
# copydoc(id doc src, id folder target)
copyDoc("4564418" , 3273998)
copyDoc("4564419" , 3273998)
copyDoc("4564420" , 3273998)
copyDoc("4564421" , 3273998)
copyDoc("4564422" , 3273998)
copyDoc("4564423" , 3273998)
copyDoc("4564424" , 3273998)
copyDoc("4564425" , 3273998)
copyDoc("4564448" , 3273998)
copyDoc("4564460" , 3273998)

# Log off the Session identified by the X-SAP-LogonToken HTTP Header
headers = { 
    'X-SAP-LogonToken' : '"'+logonToken+'"' ,
    'Accept'           : 'application/json' ,
    'Content-Type'     : 'application/json' 
}
urllib.request.urlopen(urllib.request.Request(hostUrl + '/logoff',b'',headers))
# le body vide b'' va simuler une requete POST
# un body vide None va simuler une requete GET


              



