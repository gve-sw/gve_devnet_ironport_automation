#!/usr/bin/env python3
'''
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''
import requests, urllib3
import base64, sys
import json, yaml


urllib3.disable_warnings() #suppress output about insecure requests

#Each API call to the WSA must be authenticated with a token.
#This function returns a JSON web token that can then be used to authenticate future requests
def getToken(wsa, headers):
    #username and password must be specified as base64 encoded strings in the body of the token request
    username = base64.b64encode(wsa["username"].encode("utf-8"))
    password = base64.b64encode(wsa["password"].encode("utf-8"))

    login_endpoint = "/wsa/api/v2.0/login"
    body = {
        "data":
        {
            "userName": str(username, "utf-8"),
            "passphrase": str(password, "utf-8")
        }
    }

    #make POST request to WSA with login endpoint
    resp = requests.post(wsa["url"]+login_endpoint, headers=headers, json=body, verify=False)
    resp_json = json.loads(resp.text)
    token = resp_json["data"]["jwtToken"]

    return token


#Function makes an API call to the WSA to get the URL categories. The URL categories are then copied into the file url_categories.txt
def getURLCategories(wsa, headers):
    #Retrieve token to authenticate request and save it in request headers
    token = getToken(wsa, headers)
    headers["jwtToken"] = token

    url_categories_endpoint = "/wsa/api/v2.0/configure/web_security/url_categories"

    #Make GET request to WSA with url categories endpoint
    resp = requests.get(wsa["url"]+url_categories_endpoint, headers=headers, verify=False)
    resp_json = json.loads(resp.text)
    print(resp_json) #response of request prints to terminal

    #Format the response and copy it to the file url_categories.txt - will group URLs by URL categories

    url_category_file = open("url_categories.txt", "w")

    for category in resp_json["res_data"]:
        sites = category["sites"]
        category_name = category["category_name"]
        file_string = category_name + ": {}\n".format(sites)
        url_category_file.write(file_string)

    url_category_file.close()


#Function makes an API call to the WSA to add URLs from the add_urls.yml file to a specified URL Category
def addURLCategories(wsa, headers):
    #Retrieve token to authenticate request and save it in request headers
    token = getToken(wsa, headers)
    headers["jwtToken"] = token

    url_categories_endpoint = "/wsa/api/v2.0/configure/web_security/url_categories"

    #The information specified in the add_urls.yml file will be sent in the body of the request
    url_categories_body = yaml.safe_load(open("add_urls.yml"))

    #Make PUT request to WSA with url categories endpoint with the body specified in the add_urls.yml file
    resp = requests.put(wsa["url"]+url_categories_endpoint, headers=headers, json=url_categories_body, verify=False)
    resp_json = json.loads(resp.text)
    print(resp_json) #Print result of the API call


#Function makes an API call to the WSA to get the Web Proxy Bypass List. The URLs in the bypass list are then copied into the file bypass_proxy.txt
def getBypassProxy(wsa, headers):
    #Retrieve token to authenticate request and save it in request headers
    token = getToken(wsa, headers)
    headers["jwtToken"] = token

    bypass_proxy_endpoint = "/wsa/api/v2.0/configure/web_security/bypass_proxy"

    #Make GET request to WSA with bypass proxy endpoint
    resp = requests.get(wsa["url"]+bypass_proxy_endpoint, headers=headers, verify=False)
    resp_json = json.loads(resp.text)
    print(resp_json) #response of request prints to terminal

    #Format the response and copy it to the file bypass_proxy.txt - will list all Bypass Proxy URLs
    bypass_proxy_file = open("bypass_proxy.txt", "w")

    bypass_list = resp_json["res_data"]["bypass_list"]
    for entry in bypass_list:
        file_string = entry + '\n'
        bypass_proxy_file.write(file_string)

    bypass_proxy_file.close()


#Function makes an API call to the WSA to add URLs from the add_bypass.yml file to the Web Proxy Bypass list
def addBypassProxy(wsa, headers):
    #Retrieve token to authenticate request and save it in request headers
    token = getToken(wsa, headers)
    headers["jwtToken"] = token

    bypass_proxy_endpoint = "/wsa/api/v2.0/configure/web_security/bypass_proxy"

    #The information specified in the add_bypass.yml file will be sent in the body of the request
    bypass_proxy_body = yaml.safe_load(open("add_bypass.yml"))

    #Make PUT request to WSA with bypass proxy endpoint with the body specified in the add_bypass.yml file
    resp = requests.put(wsa["url"]+bypass_proxy_endpoint, headers=headers, json=bypass_proxy_body, verify=False)
    resp_json = json.loads(resp.text)
    print(resp_json) #Print result of API call


#getIDProfiles only works with version 14.0
#def getIDProfiles(wsa, headers):
    #id_profile_endpoint = "/wsa/api/v3.0/web_security/identification_profiles"

    #resp = requests.get(wsa["url"]+id_profile_endpoint, headers=headers, verify=False)
    #resp_json = json.loads(resp.text)
    #print(resp_json)


if __name__ == '__main__':
    #URL/IP address, username, and password of the WSA are all specified in the wsa_cred.yml file
    wsa = yaml.safe_load(open("wsa_cred.yml"))

    #Necessary headers for each request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    #Check to make sure a function is provided when the program is run
    n = len(sys.argv)
    if n <= 1:
        print("Script requires at least one argument from list: getURLCategories, addURLCategories, getBypassProxy, addBypassProxy")

    funcs = sys.argv[1:]

    #Check which options are specified as arguments and run the functions associated with each option. If an invalid option is provided, print out an error message
    for func in funcs:
        if str(func) == "getURLCategories":
            getURLCategories(wsa, headers)
        elif str(func) == "addURLCategories":
            addURLCategories(wsa, headers)
        elif str(func) == "getBypassProxy":
            getBypassProxy(wsa, headers)
        elif str(func) == "addBypassProxy":
            addBypassProxy(wsa, headers)
        #elif str(func) == "getIDProfiles":
            #getIDProfiles(wsa, headers)
        else:
            print("Invalid argument: {}. Provide argument from the following: getURLCategories, addURLCategories, getBypassProxy, addBypassProxy".format(str(func)))
