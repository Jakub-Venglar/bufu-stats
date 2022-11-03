#! python3
# Scrapes data from our team forum and count team members attendace on practices
# use https://curlconverter.com/ and copy bash cURL for getting login cookies
# login through headers and cookies because other approach does not work 

import requests, re, os, sys
print(os.getcwd())
os.chdir(os.path.dirname(sys.argv[0]))
print(os.getcwd())

#open and convert files with headers and cookies
cookies = eval(open('cookies.txt').read())
headers = eval(open('headers.txt').read())

# TODO set params for practice part of forum; f is practice forum t is for threads - part of the loop

# TODO create loop for going throug all practice pages and append it to file
startT= 1280
endtT= 1296

#promaze puvodni soubor
with open('scraped.txt', 'w', encoding='utf-8') as file:
        file.write('')

#TODO this is not working - need to get urls first

for p in range(startT,endtT+1):
    params = {
        'f': '11', 
        't': p,
    }
    page = requests.get('https://forum.brno-ultimate.cz/domains/forum.brno-ultimate.cz/viewtopic.php?', params=params, cookies=cookies, headers=headers)

    with open('scraped.txt', 'a', encoding='utf-8') as file:
        file.write('\n\n\n\   ###   ' + page.url + '   ###   \n\n\n' + page.text)


#go through the file and count attendace (create dictionary)

membersInAnoRegex = re.compile(r'poll_vote_notice.+?(Ano.+?)Ne</label>', re.DOTALL) #regex for finding part of scraped mess where people voted as Ano
namesRegex = re.compile(r'''class="username">(.+?)</a>''')  #regex for finding names the result
evidence = {}

with open('scraped.txt', 'r', encoding='utf-8') as file:
    correctPart = membersInAnoRegex.findall(file.read())
    for training in correctPart:
        attendants = namesRegex.findall(training)
        for at in attendants:
            evidence.setdefault(at,0)
            evidence[at] += 1
print(evidence)
#os.remove('scraped.txt')

# TODO save attendace to some nice format for sheet

#file.close() 