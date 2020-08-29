from django.shortcuts import render
from django.http import HttpResponse
from Diary.models import AnimePersonal
from Diary.models import AnimeInfoPersonal
from WikiScraper.models import AnimeGlobal

# Create your views here.

def viewAnimeList(animes):
    episodes = []
    for anime in animes: # get number of episodes in each anime
        if anime.animeGlobalId != None:
            episodes.append(AnimeGlobal.objects.filter(id=anime.animeGlobalId).first().episodes)
        else:
            episodes.append(0)
    aniEpiList = zip(animes,episodes)
    return aniEpiList

def home(request):
    return render(request, 'index.html')

def anime(request):
    return render(request, 'anime.html')

def animeList(request):
    animes = AnimePersonal.objects.all().order_by('title')
    aniEpiList = viewAnimeList(animes)
    return render(request, 'animeList.html',{'aniEpiList': aniEpiList})

def animeAdd(request):   
            
    if request.method == 'POST':
        title = request.POST['personalTitle']
        status = request.POST['status']
        finishedEpisodes = request.POST['finishedEpisodes']
        endDate = request.POST['endDate']
        rating = request.POST['rating']
        comment = request.POST['comment']
        animeId = request.POST['animeId']
        animeInfoGlobalId = request.POST['animeInfoGlobalId']
        animeInfoPersonalId = request.POST['animeInfoPersonalId']

        if animeInfoGlobalId == -1:         # something was changed in Info category (scraping doesnt count)
            animeGlobal = None
            if animeInfoPersonalId == "":   # there is no entry in Personal anime Info table
                animeInfoPersonal = AnimeInfoPersonal()
            else:                           # there is an entry in Personal anime info table, update it
                animeInfoPersonal = AnimeInfoPersonal.objects.filter(id = animeInfoPersonalId)

            animeInfoPersonal.title            = request.POST['globalTitle']
            animeInfoPersonal.directedBy       = request.POST['directedBy']
            animeInfoPersonal.producedBy       = request.POST['producedBy']
            animeInfoPersonal.writtenBy        = request.POST['writtenBy']
            animeInfoPersonal.musicBy          = request.POST['musicBy']
            animeInfoPersonal.studio           = request.POST['studio']
            animeInfoPersonal.licensedBy       = request.POST['licensedBy']
            animeInfoPersonal.originalNetwork  = request.POST['originalNetwork']
            animeInfoPersonal.originalRun      = request.POST['originalRun']
            animeInfoPersonal.episodes         = request.POST['episodes']
            animeInfoPersonal.save()       #update

            if animeId == "":   # there is no entry in personal anime table
                anime = AnimePersonal.objects.create(title=title,status=status,finishedEpisodes=finishedEpisodes,endDate=endDate, rating=rating, comment = comment,animeInfoPersonalId=animeInfoPersonal.id, animeGlobalId=None)
            else:               # there is an entry in table, update it
                anime = AnimePersonal.objects.filter(animeId=animeId).first()
                anime.title = title
                anime.status = status
                anime.finishedEpisodes = finishedEpisodes
                anime.endDate = endDate
                anime.rating = rating
                anime.comment = comment
                anime.animeInfoPersonalId = animeInfoPersonal.id
                anime.animeGlobalId = None
                anime.save()    # update
        else:                               # no changes in info category
            animeInfoPersonal = None
            # animeInfoGlobal added to table in WikiScraper, id of it is in animeInfoGlobalId
            animeGlobal = AnimeGlobal.objects.filter(id = animeInfoGlobalId).first()
            if animeId == "":   # there is no entry in personal anime table
                anime = AnimePersonal.objects.create(title=title,status=status,finishedEpisodes=finishedEpisodes,endDate=endDate, rating=rating, comment = comment,animeInfoPersonalId=None, animeGlobalId=animeInfoGlobalId)
            else:               # there is an entry in table, update it
                anime = AnimePersonal.objects.filter(animeId=animeId).first()
                anime.title = title
                anime.status = status
                anime.finishedEpisodes = finishedEpisodes
                anime.endDate = endDate
                anime.rating = rating
                anime.comment = comment
                anime.animeInfoPersonalId = None
                anime.animeGlobalId = animeInfoGlobalId
                anime.save()    # update


        # TODO data validation

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
            

    return render(request, 'animeAdd.html',{'anime': anime, 'animeInfoPersonal': animeInfo, 'animeGlobal': animeGlobal})

def listModify(request):   

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


def sortStatus(request):    # make new query and order by sth TODO performence upgrade -> sort already downloaded data
    animes = AnimePersonal.objects.all().order_by('status')
    return render(request, 'animeList.html',{'animes': animes})

def sortTitle(request):    # make new query and order by sth TODO performence upgrade -> sort already downloaded data
    animes = AnimePersonal.objects.all().order_by('title')
    return render(request, 'animeList.html',{'animes': animes})

def sortEndDate(request):    # make new query and order by sth TODO performence upgrade -> sort already downloaded data
    animes = AnimePersonal.objects.all().order_by('finishedDate')
    return render(request, 'animeList.html',{'animes': animes})

def sortPremiered(request):    # make new query and order by sth TODO performence upgrade -> sort already downloaded data
    animes =AnimePersonal.objects.all().order_by('premiered')
    return render(request, 'animeList.html',{'animes': animes})

def index(request):
    return render(request, 'index.html')

def animeInfo(request):
    animeId = request.GET['animeId']
    print("XD", animeId)
    animeInfoId = request.GET['animeInfoId']
    animeGlobalId = request.GET['animeGlobalId']
    if animeGlobalId == "None":
        anime = AnimeGlobal('none','none','none','none','none','none','none','none','none',episodes=0)
    else:
        anime = AnimeGlobal.objects.filter(id=animeGlobalId).first()
    return render(request, 'animeInfo.html',{'anime': anime, 'animeId':animeId, 'animeInfoId': animeInfoId, 'animeGlobalId': animeGlobalId})


def animeDelete(request):
    animePersonalId = request.GET['animeId']
    AnimePersonal.objects.filter(id=animePersonalId).delete()
    animes = AnimePersonal.objects.all().order_by('title')
    return render(request, 'animeList.html',{'animes': animes})
