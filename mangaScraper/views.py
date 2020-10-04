from django.shortcuts import render
from django.http import HttpResponse
import wikipedia as wiki
import re
from mangaScraper.models import MangaGlobal

# Create your views here.

def makeStringFromList(list):
    listString = ""
    for i in range(len(list)):
        listString += list[i]
        if i != len(list)-1:
            listString += ", "
    return listString

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

        if i == (len(text) - 1):            # last 
            data.append(text[start:])             
    return data

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
    beginning = data.find("Manga")
    if beginning == -1:
        return -1
    end = data.find("Volumes")
    data = data[beginning:end+9]   # +10 only when number of epi. uses double digits TODO make it work for different number of digits Written&#160;by

    manga = MangaGlobal()

    # Dictionary of beginning indexes in each category                               Illustrated&#160;by                     Published&#160;by, nbsp = #160?xd
    indexes = {"WrittenBy": data.find("Written"), "IllustratedBy": data.find("Illustrated"),"PublishedBy": data.find("Published"), "EnglishPublisher": data.find("English publisher"), "Imprint": data.find("Imprint"), "Magazine": data.find("Magazine"), "Demographic": data.find("Demographic"), "OriginalRun":data.find("Original run"), "Volumes": data.find("Volumes")}
    indexesArray = [indexes["WrittenBy"], indexes["IllustratedBy"], indexes["PublishedBy"], indexes["EnglishPublisher"], indexes["Imprint"], indexes["Magazine"], indexes["Demographic"], indexes["OriginalRun"], indexes["Volumes"]]
    offsetArray = [15,19,17,17,7,8,11,12,7]
    infoArray = []

    # in range(9) -> <0,8>
    for i in range(9):
        if indexesArray[i] == -1:
            infoArray.append("None")
            continue
        else:
            if i == 8:  # volumes; Last one in categories
                infoArray.append(data[indexesArray[i]+offsetArray[i]:])
                break
            for j in range(i+1,9):
                if indexesArray[j] == -1:
                    continue
                else:
                    infoArray.append(data[ indexesArray[i]+offsetArray[i]:indexesArray[j] ])
                    break

    manga.title            = title
    manga.writtenBy        = infoArray[0]
    manga.illustratedBy    = infoArray[1]
    manga.publishedBy      = infoArray[2]
    manga.englishPublisher = infoArray[3]
    manga.imprint          = infoArray[4]
    manga.magazine         = infoArray[5]
    manga.demographic      = infoArray[6]
    manga.originalRun      = infoArray[7]
    manga.volumes          = int(infoArray[8])
 
    return manga




def mangaScraper(request):          # TODO Add genre?

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        personalTitle = request.POST['personalTitle']
        if personalTitle == "":                         # user has to input title in order to find informations about it
            return render(request, 'mangaAdd.html', {'mangaGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})

        # TODO  -----------------------------------------------------Alternative search---------------------------------------------------------------------------------
        # tempTitle = personalTitle + " (manga)" 
        # suggestedTitles = wiki.search(tempTitle, results = 3, suggestion = True)    # two dimensional array? xd

        #if len(suggestedTitles[0]) == 0:   # ([], None)
        #    suggestedTitles = wiki.search(personalTitle, results = 3, suggestion = True)
        #    if len(suggestedTitles[0]) == 0: # ([], None)
        #        return render(request, 'mangaAdd.html', {'mangaGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})

        suggestedTitles = wiki.search(personalTitle, results = 3, suggestion = True)
        if len(suggestedTitles[0]) == 0: # ([], None)
            return render(request, 'mangaAdd.html', {'mangaGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})

        for title in suggestedTitles[0]:
            if MangaGlobal.objects.filter(title= title).exists():
                mangaGlobal = MangaGlobal.objects.filter(title=title).first()
                return render(request, 'mangaAdd.html', {'mangaGlobal': mangaGlobal, 'personalTitle': personalTitle})
            else:
                data = str(wiki.WikipediaPage(title= title).html())
                data = re.sub('<sup style="font-style:normal;">.*?</sup>', '', data)      # remove 'NA' etc (country shortcuts from infobox)
                data = re.sub('<[^<]+?>', '', data) # remove html tags
                # print("Data: ",data,"End")
                mangaGlobal = filtrData(data, title)
                if mangaGlobal == -1:
                    continue
                else: 
                    # mangaGlobal.save()     #uncomment this (but comment when debugging)
                    return render(request, 'mangaAdd.html', {'mangaGlobal': mangaGlobal, 'personalTitle': personalTitle})

        return render(request, 'mangaAdd.html', {'mangaGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True}) # , 'data': data
        # return render(request, 'mangaAdd.html', {'mangaGlobal': mangaGlobal, 'personalTitle': personalTitle})
        # for tests: return render(request, 'mangaScraper.html',{"manga": mangaGlobal})

    return render(request, 'mangaScraper.html')