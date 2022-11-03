#! python3
# Scrapes data from our team forum and count team members attendace on practices
# use https://curlconverter.com/ and copy bash cURL for getting login cookies
# login through headers and cookies because other approach does not work 

import requests, re

#open and convert files with headers and cookies
cookies = eval(open('cookies.txt').read())
headers = eval(open('headers.txt').read())

# TODO set params for practice part of forum; f is practice forum t is for threads - part of the loop

params = {
    'f': '11', 
    't': '1272',
}

#params=params

# TODO create loop for going throug all practice pages and append it to file
page = requests.get('https://forum.brno-ultimate.cz/domains/forum.brno-ultimate.cz/viewtopic.php?', params=params, cookies=cookies, headers=headers)

#print(page.text)
file = open("scraped.txt", "w")
file.write(page.text)


# TODO go through the file and count attendace (create dictionary)

membersInAnoRegex = re.compile(r'(poll_vote_notice.+)(Ano.+)(Ne</label>)', re.DOTALL)
file = open("scraped.txt", "r")
correctPart = membersInAnoRegex.search(file.read()).group()
namesRegex = re.compile(r'''class="username">(.+?)</a>''')
attendants = namesRegex.findall(correctPart)
evidence = {}
for at in attendants:
    evidence.setdefault(at,0)
    evidence[at] += 1
print(evidence)


# TODO save attendace to some nice format for sheet

#file.close()