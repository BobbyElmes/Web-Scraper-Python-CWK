import requests
from bs4 import BeautifulSoup
import time

homeurl = "http://example.webscraping.com/"

#reads individual words off the given web page
def parser(url):
    x = requests.get(url)
    soup = BeautifulSoup(x.content,"html.parser")
    links = []
    wordIndex = []
    word = ""
    words = soup.get_text("|")
    for element in words:
        if(element != ' ' and element != '\n' and element != ":" and element != "|"):
            word += element
        else:
            if(len(word) != 0):
                alreadyOnPage = False
                for i in range(0,len(wordIndex)):
                    if(wordIndex[i][0] == word):
                        wordIndex[i][1] += 1
                        alreadyOnPage = True
                if(alreadyOnPage == False):
                    wordIndex.append([word,1])
                word = ""
    for link in soup.findAll('a'):
        if(link.get('href') != "#"):
            links.append(link.get('href'))
    print(wordIndex)
    return wordIndex, links

#crawls web pages, given the frontier url until there are no more pages to crawl in
#the first in first out queue
def crawler(frontier):
    done = False
    webPages = []
    alreadyParsed = []
    invertedIndex = []
    webQueue = []
    webQueue.append(frontier)
    first = True
    x = 0
    while(len(webQueue) > 0):
        if(first == True):
            url = webQueue[0]
            alreadyParsed.append(frontier + "/places/default/index/1")
            first = False
        else:
            url = frontier + webQueue[0]
            print(url)
            
        currentWords, urls = parser(url)
        webQueue.pop(0)
        for i in range(0,len(currentWords)):
            add = True
            for c in range(0,len(invertedIndex)):
                if(currentWords[i][0] == invertedIndex[c][0]):
                    invertedIndex[c].append(currentWords[i][1])
                    invertedIndex[c].append(url)
                    add = False
            if(add == True):
                invertedIndex.append([currentWords[i][0], currentWords[i][1],url])
             
            
        length = len(urls)
        for i in range(0,length):
            add = True
            if ("edit" in urls[i]):
                add = False
            for n in range(0,len(urls[i])):
                if(urls[i][n] == '?'):
                    urls[i] = (urls[i][0:n])
                    break
                    
            for c in range(0,len(alreadyParsed)):
                if(alreadyParsed[c] == urls[i]):
                   add = False
            if(add == True):
                webQueue.append(urls[i])
                alreadyParsed.append(urls[i])
        x += 1
        time.sleep(5)

    with open("output.txt", "w") as txt_file:
        for i in range(0,len(invertedIndex)):
            for c in range(0,len(invertedIndex[i])):
                temp = invertedIndex[i][c]
                txt_file.write(str(temp) + " ")
            txt_file.write('\n')
      
#loads the file which stores the inverted index
def load(file):
    f = open(file, "r")
    line = f.readline()
    invertedIndex = []
    
    while(line != ""):
        x = 0
        append = True
        temp = []
        for i in range(0,len(line)):
            if(line[i] == " " or line[i] == '\n'):
                x += 1
                append = True
            else:
                if(append == True):
                    temp.append(line[i])
                    append = False
                else:
                    temp[x] += line[i]
        invertedIndex.append(temp)
        line = f.readline()
    return invertedIndex

#prints an inverted index for a particular word
def printIndex(index, choice):
    word = ""
    add = False
    for i in range(0,len(choice)):
        if(choice[i] == " "):
            add = True
        else:
            if(add == True):
                word += choice[i]     
    for i in range(0,len(index)):
        if(index[i][0] == word):
            print(index[i])

#returns a list of all pages which contain one or more words
def findIndex(index, choice):
    words = []
    add = 0
    firstAdd = False
    pages = []
    for i in range(0,len(choice)):
        if(choice[i] == " "):
            add += 1
            firstAdd = True
        else:
            if(add > 0):
                if(firstAdd == True):
                    words.append(choice[i])
                    firstAdd = False
                else:
                    words[add-1] += choice[i]
    print(words)
    for c in range(0,len(words)):
        for i in range(0,len(index)):
            if(index[i][0] == words[c]):
                for x in range(0,len(index[i])):
                    if(x > 1):
                        if((x % 2) == 0):
                            addPage = True
                            for l in range(0,len(pages)):
                                if(pages[l][0] == index[i][x]):
                                    pages[l][1] += 1
                                    pages[l][2] += index[i][x-1]
                                    addPage = False
                            if(addPage == True):
                                pages.append([index[i][x],1, index[i][x-1]])

    ordered = []
    
    for i in range(0,len(pages)):
        if(pages[i][1] == add):
            done = False
            for c in range(0,len(ordered)):
                if(ordered[c][1] < pages[i][2]):
                    ordered.insert(c, [pages[i][0], pages[i][2]])
                    done= True
                    break
            if(done == False):
                ordered.append([pages[i][0], pages[i][2]])
    for i in range(0,len(ordered)):
        print(ordered[i][0])
    
                
#menu
choice = ""
index = []
while(choice != "quit"):
    choice = input()

    if(choice == "build"):
        crawler("http://example.webscraping.com")
        
    if(choice == "load"):
        index = load("output.txt")

    if(choice.startswith("print")):
        printIndex(index,choice)

    if(choice.startswith("find")):
        findIndex(index,choice)
        

        
