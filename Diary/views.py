from django.shortcuts import render, redirect
from django.http import HttpResponse
from Diary.models import AnimePersonal
from Diary.models import AnimeInfoPersonal
from WikiScraper.models import AnimeGlobal

# Create your views here.

# zip animes personal data with number of episodes in each (global data or anime info personal)
def viewAnimeList(animes):
    episodes = []
    for anime in animes:                        # get number of episodes in each anime
        if anime.animeGlobalId != None:         # firstly check in global data
            episodes.append(AnimeGlobal.objects.filter(id=anime.animeGlobalId).first().episodes)
        elif anime.animeInfoPersonalId != None: # then check in personal information about this anime
            episodes.append(AnimeInfoPersonal.objects.filter(id=anime.animeInfoPersonalId).first().episodes)
        else:                                   # if there is no information about number of episodes just push 0
            episodes.append(0)
    aniEpiList = zip(animes,episodes)
    return aniEpiList

def home(request):
    return render(request, 'index.html')

def animeList(request):   

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    sortBy = request.GET['by']
    order = request.GET['order']
    if order == "desc": 
        order = "-"
    else:   # asc
        order = ""
    animes = AnimePersonal.objects.filter(userId=user.id).order_by(order+sortBy) # https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending tldr: "-title" -> desc, "title" -> asc 
    aniEpiList = viewAnimeList(animes)
    return render(request, 'animeList.html',{'aniEpiList': aniEpiList})

def animeAdd(request):   

    user = request.user
    if not user.is_authenticated:
        return redirect('login')
            
    if request.method == 'POST':
        anime = AnimePersonal()
        anime.title = request.POST['personalTitle']
        anime.status = request.POST['status']         
        anime.finishedEpisodes = request.POST['finishedEpisodes']
        anime.endDate = request.POST['endDate']
        anime.rating = request.POST['rating']
        anime.comment = request.POST['comment']
        animeId = request.POST['animeId']
        animeInfoGlobalId = request.POST['animeInfoGlobalId']
        animeInfoPersonalId = request.POST['animeInfoPersonalId']

        animeInfoPersonal = AnimeInfoPersonal()
        animeInfoPersonal.title            = request.POST['globalTitle']
        animeInfoPersonal.directedBy       = request.POST['directedBy']
        animeInfoPersonal.producedBy       = request.POST['producedBy']
        animeInfoPersonal.writtenBy        = request.POST['writtenBy']
        animeInfoPersonal.musicBy          = request.POST['musicBy']
        animeInfoPersonal.studio           = request.POST['studio']
        animeInfoPersonal.licensedBy       = request.POST['licensedBy']
        animeInfoPersonal.originalNetwork  = request.POST['originalNetwork']
        animeInfoPersonal.originalRun      = request.POST['originalRun']
        animeInfoPersonal.episodes         = request.POST['globalEpisodes']

        # data validation - start
        if anime.title == "": 
            return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo':  animeInfoPersonal, 'animeGlobal': None, 'wrongTitle': True})

        if anime.status != "Watching" and anime.status != "Want to watch" and anime.status != "Finished" and anime.status != "Abandoned":
            return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo':  animeInfoPersonal, 'animeGlobal': None, 'wrongStatus': True})

        if anime.finishedEpisodes == "":
            return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo':  animeInfoPersonal, 'animeGlobal': None, 'wrongEpisodes': True})

        if anime.endDate == "":
            return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo': animeInfoPersonal, 'animeGlobal': None, 'wrongDate': True})

        if anime.rating == "": 
            rating = 0  # 0 -> rating not defined

        if int(anime.rating) < 0 or int(anime.rating) > 10: # validation of number being integer is already done (by browser? type=integer in html)
            return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo': None, 'animeGlobal': None, 'wrongRatingRange': True})
        # data validation end        

        if animeInfoGlobalId == -1:         # something was changed in Info category (scraping doesnt count)
            animeGlobal = None
            if animeInfoPersonalId == "":   # there is no entry in Personal anime Info table
                animeInfoPersonalNew = AnimeInfoPersonal()
            else:                           # there is an entry in Personal anime info table, update it
                animeInfoPersonalNew = AnimeInfoPersonal.objects.filter(id = animeInfoPersonalId).first()

            animeInfoPersonalNew.title            = animeInfoPersonal.title
            animeInfoPersonalNew.directedBy       = animeInfoPersonal.directedBy
            animeInfoPersonalNew.producedBy       = animeInfoPersonal.producedBy 
            animeInfoPersonalNew.writtenBy        = animeInfoPersonal.writtenBy
            animeInfoPersonalNew.musicBy          = animeInfoPersonal.musicBy 
            animeInfoPersonalNew.studio           = animeInfoPersonal.studio  
            animeInfoPersonalNew.licensedBy       = animeInfoPersonal.licensedBy
            animeInfoPersonalNew.originalNetwork  = animeInfoPersonal.originalNetwork
            animeInfoPersonalNew.originalRun      = animeInfoPersonal.originalRun 
            animeInfoPersonalNew.episodes         = animeInfoPersonal.episodes 
            animeInfoPersonalNew.save()       #update

            if animeId == "":   # there is no entry in personal anime table
                animeNew = AnimePersonal() # .objects.create(title=anime.title,status=anime.status,finishedEpisodes=anime.finishedEpisodes,endDate=anime.endDate, rating=anime.rating, comment = anime.comment,animeInfoPersonalId=animeInfoPersonal.id, animeGlobalId=None)
            else:               # there is an entry in table, update it
                animeNew = AnimePersonal.objects.filter(id=animeId).first()

            animeNew.title = anime.title
            animeNew.status = anime.status
            animeNew.finishedEpisodes = anime.finishedEpisodes
            animeNew.endDate = anime.endDate
            animeNew.rating = anime.rating
            animeNew.comment = anime.comment
            animeNew.animeInfoPersonalId = animeInfoPersonal.id
            animeNew.animeGlobalId = None
            animeNew.userId = user.id
            animeNew.save()    # update
            anime = animeNew
        else:                               # no changes in info category
            animeInfoPersonal = None        # set anime info personal to none
            
            # animeInfoGlobal added to table in WikiScraper, id of it is in animeInfoGlobalId
            if animeInfoGlobalId != "":
                animeGlobal = AnimeGlobal.objects.filter(id = animeInfoGlobalId).first()
            else:   # there are no personal nor global informations about this anime
                animeGlobal = None
                animeInfoGlobalId = None

            if animeId == "":   # there is no entry in personal anime table
                animeNew = AnimePersonal()
            else:               # there is an entry in table, update it
                animeNew = AnimePersonal.objects.filter(id=animeId).first()
            animeNew.title = anime.title
            animeNew.status = anime.status
            animeNew.finishedEpisodes = anime.finishedEpisodes
            animeNew.endDate = anime.endDate
            animeNew.rating = anime.rating
            animeNew.comment = anime.comment
            animeNew.animeInfoPersonalId = None
            animeNew.animeGlobalId = animeInfoGlobalId
            animeNew.userId = user.id
            animeNew.save()    # update
            anime = animeNew

    if request.method == 'GET':
        animeId = request.GET['animeId']
        if animeId == "None" or animeId=="":
            anime = None
        else:
            anime = AnimePersonal.objects.filter(id=animeId).first()

        animeInfoId = request.GET['animeInfoId']
        if animeInfoId == "None" or animeInfoId == "":
           animeInfoPersonal = None
        else:
            animeInfoPersonal = AnimeInfoPersonal.objects.filter(id=animeInfoId).first()

        animeGlobalId = request.GET['animeGlobalId']
        if animeGlobalId == "None" or animeGlobalId == "":
            animeGlobal = None
        else:
            animeGlobal = AnimeGlobal.objects.filter(id=animeGlobalId).first()
            
    return render(request, 'animeAdd.html',{'anime': anime, 'animeInfo': animeInfo, 'animeGlobal': animeGlobal})

def listModify(request):   

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    animes = AnimePersonal.objects.all().order_by('title')

    for anime in animes:    # check all rows (!!! :( ) and save data, TODO performence upgrade?

        anime.title = request.POST['title'+str(anime.id)]
        anime.status = request.POST['status'+str(anime.id)]
        anime.finishedEpisodes = request.POST['finishedEpisodes'+str(anime.id)]
        anime.endDate = request.POST['endDate'+str(anime.id)] 
        anime.rating = request.POST['rating'+str(anime.id)]
        anime.comment = request.POST['comment'+str(anime.id)]

        # TODO data validation; None here -> null in database
        if anime.endDate == "":
             anime.end = None

        anime.save()
    aniEpiList = viewAnimeList(animes)
    return render(request, 'animeList.html',{'aniEpiList': aniEpiList})


def animeInfo(request):

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    animeId = request.GET['animeId']
    animeInfoId = request.GET['animeInfoId']
    animeGlobalId = request.GET['animeGlobalId']
    if animeGlobalId == "None":
        anime = AnimeGlobal('none','none','none','none','none','none','none','none','none',episodes=0)
    else:
        anime = AnimeGlobal.objects.filter(id=animeGlobalId).first()
    return render(request, 'animeInfo.html',{'anime': anime, 'animeId':animeId, 'animeInfoId': animeInfoId, 'animeGlobalId': animeGlobalId})


def animeDelete(request):

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    animePersonalId = request.GET['animeId']
    AnimePersonal.objects.filter(id=animePersonalId).delete()
    animes = AnimePersonal.objects.all().order_by('title')
    return render(request, 'animeList.html',{'animes': animes})
