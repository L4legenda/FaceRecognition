import requests
import json 
import urllib.request
 

ipHost = "http://23.105.226.115/"

def dowloadFile(url, name):
    print(url + name)
    response = urllib.request.urlopen(url + name)
    image = response.read()

    with open("./image/" + name, "wb") as file:
        file.write(image)

def parseUsers():
    users = requests.post(ipHost + 'api/users')
    jsonUser = json.loads(users.text)
    arrUsers = []

    for user in jsonUser:
        if user["Photo"] == "" or not user["Group"]["Valid"]:
            continue

        arrUsers.append(user)
        dowloadFile(ipHost + "api/assets/", user["Photo"])
        
    return arrUsers
