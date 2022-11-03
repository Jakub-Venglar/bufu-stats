#! python3
# Scrapes data from our team forum and count team members attendace on practices
# use https://curlconverter.com/ and copy bash cURL for getting login cookies
# login through headers and cookies because other approach does not work 

import requests

#open and convert files with headers and cookies
cookies = eval(open('cookies.txt').read())
headers = eval(open('headers.txt').read())

# TODO set params for practice part of forum; f is practice forum t is for threads - part of the loop

params = {
    'f': '11', 
    't': '1293',
}

#params=params

# TODO create loop for going throug all practice pages and append it to file
page = requests.get('https://forum.brno-ultimate.cz/domains/forum.brno-ultimate.cz/viewtopic.php?', params=params, cookies=cookies, headers=headers)

print(page.url)

'''
file = open("scraped.txt", "a")
file.write(page.text)
'''

# TODO go through the file and count attendace (create dictionary)
# TODO save attendace to some nice format for sheet

#file.close()