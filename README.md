# Ironport Automation

This is a script that utilizes the AsyncOS API of Cisco Web Security Appliances to 
retrieve the URL Categories, add URLs to an already existing URL Category, retrieve 
the Web Proxy Bypass List, and add URLs to the Web Proxy Bypass List. This prototype 
was written for AsyncOS version 12.5. 

## Overview
This repository contains a Python script and Ansible playbook that each perform the 
same actions. The Python script has a commented out function that will allow the 
user to retrieve the Identification Profiles from the Web Security Appliance, 
but this API call is not compatible with version 12.5 AsyncOS. To use this function, 
the Web Security Appliance must be version 14.0 or newer.

## Contacts
* Danielle Stacy (dastacy@cisco.com)

## Solution Components
* Cisco WSA
* AsyncOS API 12.5
* Python 3.9
* Ansible

## Prerequisites
- **WSA Setup**:
    - **Enable AsyncOS API**: To enable the AsyncOS API on a Web Security Appliance, follow [these steps](https://www.cisco.com/c/en/us/td/docs/security/wsa/wsa_12-5/api_guide/b_WSA_API_12-5_Guide/b_WSA_API_Guide_chapter_011.html#ariaid-title3). 
    - **WSA Credentials**: To use the APIs, it is necessary to know the IP address/hostname, username, and password of the WSA. Make note of these credentials.
    - **URL Categories**: If the script is going to be used for adding URLs to a URL Category, make note of the name of the URL Category that URLs will be added to and which URLs are going to be added to the category.
    - **Web Proxy Bypass List**: If the script is going to be used for adding URLs to a Web Proxy Bypass List, make note of the URLs that are going to be added to the list.

## Installation/Configuration

1. Clone this repository with `git clone <this repo>` and open the directory of the root repository.

2. Open the **`wsa_cred.yml`** file, and with the information collected in the [Prerequisites section](##Prerequisites), fill in the values for the variables listed in the file. These include the `url`, `username`, and `password` of the web security appliance.

3. (Optional) If the script is being used to add URLs to a URL Category, open the **`add_urls.yml`** file. With the information collected in the [Prerequisites section](##Prerequisites), fill in the values for the variables listed in the file. These include the `category_name` and `sites`. To add more items to the list of sites, follow the YAML format. To learn more about YAML, follow [this tutorial](https://www.tutorialspoint.com/yaml/yaml_basics.htm). It is important to note that the list of sites in the YAML file will completely replace the sites currently in the URL Category that is being changed. If the goal is to keep the existing sites in the cateogory and add some new sites, be sure to include the existing sites in the list in the add_urls.yml file.

4. (Optional) If the script is being used to add URLs to the Web Proxy Bypass List, open the **`add_bypass.yml`** file. With the information collected in the [Prerequisites section](##Prerequisites), fill in the values for the variables listed in the file. This includes the `bypass_list`, which is simply the list of URLs and IP addresses that are to be added to the Web Proxy Bypass List. To add more timed to the list of sites, follow the YAML format. To learn more about YAML, follow [this tutorial](https://www.tutorialspoint.com/yaml/yaml_basics.htm). It is important to note that the list of sites in the YAML file will completely replace the sites currently in the Web Proxy Bypass List. If the goal is to keep the existing sites in the list and add some new sites, be sure to include the existing sites in the list in the add_bypass.yml file.

5. Create a Python virtual environment and activate it (find instructions to do that [here](https://docs.python.org/3/tutorial/venv.html)).

6. Install the requirements with `pip install -r requirements.txt`.

## Usage

### Python Script
The python script requires command line arguments to specify which functions to run. The options are getURLCategories, addURLCategories, getBypassProxy, and addBypassProxy. If the Web Security Appliance is version 14.0 or later, another option can be added to run the getIDProfiles function. To add this option, uncomment the code in wsa.py from lines 129-134 and lines 164-165. At least one option must be specified to run the script. If a combination of options is specified, then the functions will run in the order of the the listed options.

To run the Python script:
```
$ python3 wsa.py [getURLCategories | addURLCategories | getBypassProxy | addBypassProxy]
```

If the program is attempted to run without any options specified, the program will exit, and this error message will be displayed:
```
Script requires at least one argument from list: getURLCategories, addURLCategories, getBypassProxy, addBypassProxy
```

If an option is specified that isn't included in this list, the program will exit, and an error message will be displayed. For example, if the option c is specified, this error message will be displayed:
```
$ python3 wsa.py c 
Invalid argument: c. Provide argument from the following: getURLCategories, addURLCategories, getBypassProxy, addBypassProxy
```

The output of the getURLCategories and getBypassProxy functions will be printed to the files url_categories.txt and bypass_list.txt files respectively. 

### Ansible Playbook
The Ansible playbook can be run without specifying which tasks to run. If no tags are specified, then the Ansible playbook will get the authentication token, get the URL Categories (print them to screen and write them to a file), add URL Categories specified in the add_urls.yml file, get the Web Proxy Bypass list (print the results to screen and write them to a file), and add the URLs specified in the add_bypass.yml file to the Web Proxy Bypass list. If only a subset of these tasks should be done, then specify which tasks should be run by adding the tags argument to the command. The possible tags that can be used are token, get-url-categories, add-url-categories, get-bypass-list, and add-bypass-list. Multiple tags can be specified, but if multiple tags are specified, the playbook will run in this order: token, get-url-categories, add-url-categories, get-bypass-list, add-bypass-list. If specifying which tasks to run with the ansible playbook, always specify to run the tasks associated with the "token" tag.

To run the Ansible playbook with all tasks:
```
$ ansible-playbook wsa.yml
```

To run the Ansible playbook with specific tasks:
```
$ ansible-playbook wsa.yml --tags "token,[get-url-categories | add-url-categories | get-bypass-list | add-bypass-list]"
```

## Further Documentation
To learn more about the possible API features of the WSA, view the documentation found in the [APIDOCUMENTS](/APIDOCUMENTS/) directory. There is separate documentation for [version 12.5](/APIDOCUMENTS/wsa_12-5_api_addendum.xlsx) and [version 14.0](/APIDOCUMENTS/wsa_14-0_api_addendum.pdf)

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

add_urls.yml content
![/IMAGES/add-urls-content.png](/IMAGES/add-urls-content.png)

add_bypass.yml content
![/IMAGES/add-bypass-content.png](/IMAGES/add-bypass-content.png)

Ansible command to add urls to URL Categories and Web Proxy Bypass List
![/IMAGES/ansible-add-commands.png](/IMAGES/ansible-add-commands.png)

Python command to add sites to URL Categories and Web Proxy Bypass List
![/IMAGES/python-add-commands.png](/IMAGES/python-add-commands.png)

Add URLs to URL Categories result on WSA GUI
![/IMAGES/url-categories-gui.png](/IMAGES/url-categories-gui.png)

Add URLs to Web Proxy Bypass List result on WSA GUI
![/IMAGES/bypass-list-gui.png](/IMAGES/bypass-list-gui.png)

Ansible command to get urls from URL Categories and Web Proxy Bypass List
![/IMAGES/ansible-get-commands.png](/IMAGES/ansible-get-commands.png)

Python command to get urls from URL Categories and Web Proxy Bypass List
![/IMAGES/python-add-commands.png](/IMAGES/python-add-commands.png)

Contents of url_categories_formatted.txt after get command
![/IMAGES/url-categories-formatted-content.txt](/IMAGES/url-categories-formatted-content.png)

Contents of bypass_list_categories_formatted.txt after get command
![/IMAGES/bypass-list-categories-formatted-content.txt](/IMAGES/bypass-list-categories-formatted-content.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
