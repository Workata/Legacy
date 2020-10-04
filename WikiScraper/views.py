# TODO change name to animeScraper
from django.shortcuts import render
from django.http import HttpResponse
import wikipedia as wiki
import re
from WikiScraper.models import AnimeGlobal

# Create your views here.

# DESCRIPTION this function will transform list to custom string format
def makeStringFromList(list):
    listString = ""
    for i in range(len(list)):
        listString += list[i]
        if i != len(list)-1:
            listString += ", "
    return listString

# DESCRIPTION this filter assumes that full name ussualy contains one first name and one last name (two big letters), it will try to separate different persons
def simpleFilter(text):
    #text.replace(" ", "")
    upperCounter = 0
    start = 0
    data = []

    for i in range(len(text)):
        if text[i].isupper():
            upperCounter+=1
            if upperCounter == 3:
                data.append(text[start:i])
                upperCounter = 1
                start = i

        if i == (len(text) - 1):            # last one
            data.append(text[start:])             
    return data

# DESCRIPTION delete unnecessary whitespaces and separate different licensors 
def licensedByFilter(text):     
    data = []
    start = 0
    licensorLoading = False

    text = text.replace("    ", "%")
    text = text.replace("   ", "%")
    text = text.replace("  ", "%")

    for i in range(len(text)):
        if i == len(text) - 1:      # last one
            data.append(text[start:])
        elif text[i] == '%' and licensorLoading == True:
            data.append(text[start:i])
            licensorLoading = False
        elif text[i] == '%' and licensorLoading == False:
            continue
        elif text[i] != '%' and licensorLoading == False:
            licensorLoading = True
            start = i

    return data

def filtrData(data, title):
    beginning = data.find("Anime television series")
    if beginning == -1:
        return -1
    end = data.find("Episodes")
    data = data[beginning:end+10]   # +10 only when number of epi. uses double digits TODO make it work for different number of digits

    anime = AnimeGlobal()

    # Dictionary of beginning indexes in each category, English network
    indexes = {"DirectedBy":data.find("Directed&#160;by"), "ProducedBy": data.find("Produced&#160;by"),"WrittenBy": data.find("Written&#160;by"), "MusicBy": data.find("Music&#160;by"), "Studio": data.find("Studio"), "LicensedBy": data.find("Licensed&#160;by"), "OriginalNetwork": data.find("Original"), "English": data.find("English"), "OriginalRun":data.find("Original run"), "Episodes": data.find("Episodes") }
    indexesArray = [indexes["DirectedBy"], indexes["ProducedBy"], indexes["WrittenBy"], indexes["MusicBy"], indexes["Studio"], indexes["LicensedBy"], indexes["OriginalNetwork"], indexes["English"], indexes["OriginalRun"], indexes["Episodes"] ]
    offsetArray = [16, 16, 15, 13, 6, 16, 16, 15, 13, 8]
    infoArray = []

    print(indexesArray)

    # in range(10) -> <0,9>
    for i in range(10):
        if indexesArray[i] == -1:
            infoArray.append("None")
            continue
        else:
            if i == 9:  # volumes; Last one in categories
                infoArray.append(data[indexesArray[i]+offsetArray[i]:])
                break
            for j in range(i+1,10):
                if indexesArray[j] == -1:
                    continue
                else:
                    infoArray.append(data[ indexesArray[i]+offsetArray[i]:indexesArray[j] ])
                    break

    anime.title            = title
    anime.directedBy       = infoArray[0]                                         # usually its a single person
    anime.producedBy       = makeStringFromList(simpleFilter(infoArray[1]))
    anime.writtenBy        = infoArray[2]                                         # usually its a single person
    anime.musicBy          = makeStringFromList(simpleFilter(infoArray[3]))
    anime.studio           = infoArray[4]
    anime.licensedBy       = makeStringFromList(licensedByFilter(infoArray[5]))
    anime.originalNetwork  = infoArray[6]
    anime.englishNetwork   = makeStringFromList(licensedByFilter(infoArray[7]))
    anime.originalRun      = infoArray[8]
    if infoArray[9] != "None":
         anime.episodes    = int(infoArray[9])
    
    return anime




def animeScraper(request):          # TODO Add genre?

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        personalTitle = request.POST['personalTitle']
        if personalTitle == "":
            return render(request, 'animeAdd.html', {'animeGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})
        tempTitle = personalTitle + " (TV series)"
        suggestedTitles = wiki.search(tempTitle, results = 3, suggestion = True)    # two dimensional array? xd

        print(len(suggestedTitles[0]), " ", suggestedTitles[0])

        if len(suggestedTitles[0]) == 0:   # ([], None)
            suggestedTitles = wiki.search(personalTitle, results = 3, suggestion = True)
            if len(suggestedTitles[0]) == 0: # ([], None)
                return render(request, 'animeAdd.html', {'animeGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})

        # title = suggestedTitles[0][0]
        # print(suggestedTitles[0][0])

        for title in suggestedTitles[0]:
            print(title)
            if AnimeGlobal.objects.filter(title= title).exists():                         # check if this anime exists in database
                animeGlobal = AnimeGlobal.objects.filter(title=title).first()
                return render(request, 'animeAdd.html', {'animeGlobal': animeGlobal, 'personalTitle': personalTitle})
            else:
                data = str(wiki.WikipediaPage(title= title).html())
                data = re.sub('<sup style="font-style:normal;">.*?</sup>', '', data)      # remove 'NA' etc (country shortcuts from infobox)
                data = re.sub('<[^<]+?>', '', data) # remove html tags
                # print("Data: ",data,"End")
                animeGlobal = filtrData(data, title)
                if animeGlobal == -1:
                    continue
                else: 
                    # animeGlobal.save() # uncomment this (but comment when debugging)
                    return render(request, 'animeAdd.html', {'animeGlobal': animeGlobal, 'personalTitle': personalTitle})

        return render(request, 'animeAdd.html', {'animeGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True}) # , 'data': data
        # return render(request, 'animeAdd.html', {'animeGlobal': animeGlobal, 'personalTitle': personalTitle})
        # for tests: return render(request, 'animeScraper.html',{"anime": animeGlobal})

    return render(request, 'animeScraper.html')