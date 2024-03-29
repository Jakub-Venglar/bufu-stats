#! python3
# Scrapes data from our team forum and count team members attendace on practices
# use https://curlconverter.com/ and convert bash cURL from forum for getting login cookies and headers- cookies.txt and headers.txt needed in the same folder as script
# login through cookies because other approach does not work 

import requests, re, os, sys, csv

#make sure working directory is set the same as file directory
os.chdir(os.path.dirname(sys.argv[0]))

# regexes

isPracticeRegex= re.compile(r'''(Pondělí |Čtvrtek ).+?(ZAČÁTEČNÍCI|POKROČILÍ|VŠICHNI|všichni)''') #regex for making sure we are in practice page
membersInAnoRegex = re.compile(r'poll_vote_notice.+?(Ano.+?)Ne</label>', re.DOTALL) #regex for finding poll part of scraped mess where people voted as Ano - needs to be non-greedy
namesRegex = re.compile(r'''class="username">(.+?)</a>''')  #regex for finding names the result
datesRegex = re.compile(r'(([0-2]?[0-9]|3[0-1])\.([1-2]?[0-9])\.)') #find dates so we can count them later
cookiesRegex = re.compile(r"""'cookie: (.+?)' \\""") #find cookies in curl

#input for curl and extraction of cookies used for login

cookiesSent = str(input('Vlož curl bash po přihlášení - je nutné zformátovat na jeden řádek'))

cookiesFound = cookiesRegex.findall(cookiesSent)[0].replace(" ","").replace('=','\': \'').replace(';','\',\n    \'')
listOfCookies = '{\n    \''+ cookiesFound + '\',\n}'
cookies = eval(listOfCookies)

#harcoded headers 

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
}

# start and end parametr of t in url - f is for higher forum structures and actually is not needed

startT= 1238
endtT= int(input('Zadej koncový paramater url (poslední trénink)'))
listOfDates = []

#make original file with scraped pages clean
with open('scraped.txt', 'w', encoding='utf-8') as file:
        file.write('')

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
            toWrite = membersInAnoRegex.search(page.text) # now we are writing just important part
            file.write('\n\n\n   ###START   ' + page.url + '   ###   \n\n\n' + '\n\n\n   ###   ' + confirmPractice.group() + '   ###   \n\n\n' + toWrite.group() + '   ###END   \n\n\n')
            date = datesRegex.search(confirmPractice.group()) # also count dates so we now how many practices we had
            if date.group() not in listOfDates:
                listOfDates.append(date.group())

#go through the file and count attendace into a dictionary and sort it

evidence = {}

with open('scraped.txt', 'r', encoding='utf-8') as file:
    correctPart = membersInAnoRegex.findall(file.read()) #could be more elegant but it is easy to reuse it for iteration
    for training in correctPart:
        attendants = namesRegex.findall(training)
        for at in attendants:
            evidence.setdefault(at,0)
            evidence[at] += 1

sortedEvidence = dict(sorted(evidence.items(), key=lambda x:x[1], reverse=True))

# print results

print('Celkem tréninků: ' + str(len(listOfDates)) + '\n')

for k, v in sortedEvidence.items():
    print(k + ': ' + str(v))

# TODO optional save attendace to some nice format for sheet
#with open(dochazka.csv, 'w', encoding='utf-8') as doch: