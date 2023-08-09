from getpass import getpass

client_id=getpass("Application/client id: ")#a4561365-c10c-4bfb-8023-7ba0585d23e8
client_secret=getpass("client secret: ")#gWx8Q~5_ocKN9ocKeoFm_wBJfCQM7eUXT7khlcPn




import requests
import json
import sys
from email.utils import formatdate
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def get_new_token():
    #GRAPH REST API AUTHENTICATION https://learn.microsoft.com/en-us/graph/auth-v2-service
    tenant = "98e9ba89-e1a1-4e38-9007-8bdabc25de1d"
    auth_server_url ="https://login.microsoftonline.com/98e9ba89-e1a1-4e38-9007-8bdabc25de1d/oauth2/v2.0/token"
    resource_app_uri = "https://storage.azure.com"
        
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    
    data = {"client_id": client_id,
            "response_type": "token",
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope":"https://[containername].blob.core.windows.net/.default"
            }

    tokenresp = requests.post(auth_server_url, headers=headers, data=data)
           
    if tokenresp.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server: status_code!=200 "+str(tokenresp.status_code), file=sys.stderr)
        print(str(tokenresp))
        print(str(tokenresp.text))
        sys.exit(1)
    if "We received a bad request" in tokenresp.text:
        print("Failed to obtain token from the OAuth 2.0 server: We received a bad request", file=sys.stderr)
        sys.exit(1)

    print("Successfuly obtained a new token")
    return tokenresp.json()['access_token']

print("-----GETTING NEW TOKEN-----")
token = get_new_token()
reqdate = formatdate(timeval=None, localtime=False, usegmt=True)
print (reqdate)

headers = {"Authorization": "Bearer "+str(token),
           "Date": reqdate,
           "x-ms-version": "2020-04-08"}

#blob_url = "url"
blob_url = "url"

resp = requests.get(blob_url, headers=headers)
#print(type(resp))
#print(resp.status_code)
#print(resp.text)
# soup = BeautifulSoup(resp.text,"xml")
# blob = soup.find_all('Blob')
blob_info = {}
cnt = 1
# print(blob[0])
# for  in blob:
#     # blobdata = BeautifulSoup(items,"xml")
#     # name = blobdata.Name
#     print(blob[i])
# # e = ET.ElementTree(ET.fromstring(resp.text))
# # for elt in e.Blobs.iter():
# #     print(elt.tag, elt.text)
# #print(blob)
tree = ET.ElementTree(ET.fromstring(resp.text))
root = tree.getroot()
attributes = root.attrib
for test in root.find('Blobs').findall('Blob'):
    blob_data = {}
    blob_data['name'] = test.find('Name').text
    blob_data['create_time'] = test.find('Properties').find('Creation-Time').text
    blob_data['last_modified'] = test.find('Properties').find('Last-Modified').text
    blob_info['Blob'+ str(cnt)] = blob_data
    cnt = cnt + 1
print(blob_info)

