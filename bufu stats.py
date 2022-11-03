#! python3
# Scrapes data from our team forum and count team members attendace on practices
# use https://curlconverter.com/ and copy bash cURL for getting login cookies
# login through headers and cookies because other approach does not work 

import requests, re, os, sys

#make sure working directory is set the same as file directory
os.chdir(os.path.dirname(sys.argv[0]))

#open and convert files with headers and cookies
cookies = eval(open('cookies.txt').read())
headers = eval(open('headers.txt').read())

# start and end parametr of t in url - f is for higher forum places and actually is not needed

startT= 1238
endtT= 1275

#make original file clean
with open('scraped.txt', 'w', encoding='utf-8') as file:
        file.write('')

isPracticeRegex= re.compile(r'''(Pondělí |Čtvrtek ).+?(ZAČÁTEČNÍCI|POKROČILÍ|VŠICHNI|všichni)''') #regex for making sure we are in practice part
membersInAnoRegex = re.compile(r'poll_vote_notice.+?(Ano.+?)Ne</label>', re.DOTALL) #regex for finding part of scraped mess where people voted as Ano

#main loop for going throug all practice pages and append scraped content to file

for p in range(startT,endtT+1):
    params = {
        'f': '11', 
        't': p,
    }
    page = requests.get('https://forum.brno-ultimate.cz/domains/forum.brno-ultimate.cz/viewtopic.php?', params=params, cookies=cookies, headers=headers)
    confirmPractice = isPracticeRegex.search(page.text)
    if confirmPractice:         #make sure we are at the right place
        with open('scraped.txt', 'a', encoding='utf-8') as file:
            file.write('\n\n\n   ###   ' + page.url + '   ###   \n\n\n' + '\n\n\n   ###   ' + confirmPractice.group() + '   ###   \n\n\n' + page.text)


#go through the file and count attendace (create dictionary)

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

# TODO save attendace to some nice format for sheet