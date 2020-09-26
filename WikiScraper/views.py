from django.shortcuts import render
from django.http import HttpResponse
import wikipedia as wiki
# import wptools
import re
from WikiScraper.models import AnimeGlobal

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
    beginning = data.find("Anime television series")
    if beginning == -1:
        return -1
    end = data.find("Episodes")
    data = data[beginning:end+10]   # +10 only when number of epi. uses double digits TODO make it work for different number of digits

    anime = AnimeGlobal()

    # Dictionary of beginning indexes in each category
    indexes = {"DirectedBy":data.find("Directed&#160;by"), "ProducedBy": data.find("Produced&#160;by"),"WrittenBy": data.find("Written&#160;by"), "MusicBy": data.find("Music&#160;by"), "Studio": data.find("Studio"), "LicensedBy": data.find("Licensed&#160;by"), "OriginalNetwork": data.find("Original"), "OriginalRun":data.find("Original run"), "Episodes": data.find("Episodes"), "English": data.find("English") }

    print(indexes["WrittenBy"])

    anime.title = title
    if indexes['ProducedBy'] == -1: # there is no "Produced by" category on wiki
        anime.directedBy = data[indexes["DirectedBy"]+16:indexes["WrittenBy"]] 
        anime.producedBy = None
    else:
        anime.directedBy  = data[indexes["DirectedBy"]+16:indexes["ProducedBy"]]  
        anime.producedBy  =  makeStringFromList(simpleFilter(data[indexes["ProducedBy"]+16:indexes["WrittenBy"]]))      
    anime.writtenBy   = data[indexes["WrittenBy"]+15:indexes["MusicBy"]]
    anime.musicBy     = makeStringFromList(simpleFilter(data[indexes["MusicBy"]+13:indexes["Studio"]]))
    anime.studio           = data[indexes["Studio"]+6:indexes["LicensedBy"]]
    anime.licensedBy       = makeStringFromList(licensedByFilter(data[indexes["LicensedBy"]+16:indexes["OriginalNetwork"]]))
    if indexes['English'] == -1:    # no english network on wiki
        anime.originalNetwork  = data[indexes["OriginalNetwork"]+16:indexes["OriginalRun"]]
    else:
        anime.originalNetwork  = data[indexes["OriginalNetwork"]+16:indexes["English"]]        # "English" bcs english network
    anime.originalRun       = data[indexes["OriginalRun"]+13:indexes["Episodes"]]     # premiered
    anime.episodes         = data[indexes["Episodes"]+8:]

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

        print(len(suggestedTitles[0]), " ", suggestedTitles)

        if len(suggestedTitles[0]) == 0:   # ([], None)
            suggestedTitles = wiki.search(personalTitle, results = 3, suggestion = True)
            if len(suggestedTitles[0]) == 0: # ([], None)
                return render(request, 'animeAdd.html', {'animeGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True})

        # title = suggestedTitles[0][0]
        print(suggestedTitles[0][0])

        for title in suggestedTitles[0]:
            if AnimeGlobal.objects.filter(title= title).exists():
                animeGlobal = AnimeGlobal.objects.filter(title=title).first()
                break
            else:
                data = str(wiki.WikipediaPage(title= title).html())
                data = re.sub('<sup style="font-style:normal;">.*?</sup>', '', data)      # remove 'NA' etc (country shortcuts from infobox)
                data = re.sub('<[^<]+?>', '', data) # remove html tags
                # print("Data: ",data,"End")
                animeGlobal = filtrData(data, title)
                if animeGlobal == -1:
                    continue
                else: 
                    animeGlobal.save() 
                    return render(request, 'animeAdd.html', {'animeGlobal': animeGlobal, 'personalTitle': personalTitle})

        return render(request, 'animeAdd.html', {'animeGlobal': None, 'personalTitle': personalTitle, 'noDataFound': True}) # , 'data': data
        # return render(request, 'animeAdd.html', {'animeGlobal': animeGlobal, 'personalTitle': personalTitle})
        # for tests: return render(request, 'animeScraper.html',{"anime": animeGlobal})

    return render(request, 'animeScraper.html')