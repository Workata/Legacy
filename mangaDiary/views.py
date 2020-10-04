from django.shortcuts import render, redirect
from django.http import HttpResponse
from mangaDiary.models import MangaPersonal      
from mangaDiary.models import MangaInfoPersonal  
from mangaScraper.models import MangaGlobal

# Create your views here.

# zip mangas personal data with number of volumes in each (global data or manga info personal)
def viewMangasList(mangas):
    volumes = []
    for manga in mangas:                        # get number of volumes in each manga
        if manga.mangaGlobalId != None:         # firstly check in global data
            volumes.append(MangaGlobal.objects.filter(id=manga.mangaGlobalId).first().volumes)
        elif manga.mangaInfoPersonalId != None: # then check in personal information about this manga
            volumes.append(MangaInfoPersonal.objects.filter(id=manga.mangaInfoPersonalId).first().volumes)
        else:                                   # if there is no information about number of volumes just push 0
            volumes.append(0)
    mangasVolumesList = zip(mangas, volumes)
    return mangasVolumesList


def mangaList(request):

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    sortBy = request.GET['by']
    order = request.GET['order']
    if order == "desc": 
        order = "-"
    else:   # asc
        order = ""
    mangas = MangaPersonal.objects.filter(userId=user.id).order_by(order+sortBy)
    mangasVolumesList = viewMangasList(mangas)
    return render(request, 'mangaList.html',{'mangasVolumesList': mangasVolumesList})

def mangaAdd(request):
    
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
            
    if request.method == 'POST':
        manga               = MangaPersonal()
        manga.title         = request.POST['personalTitle']
        manga.status        = request.POST['status']         
        manga.finishedVolumes = request.POST['finishedVolumes']
        manga.endDate       = request.POST['endDate']
        manga.rating        = request.POST['rating']
        manga.comment       = request.POST['comment']
        mangaId             = request.POST['mangaId']
        mangaInfoGlobalId   = request.POST['mangaInfoGlobalId']
        mangaInfoPersonalId = request.POST['mangaInfoPersonalId']

        mangaInfoPersonal = MangaInfoPersonal()
        mangaInfoPersonal.title            = request.POST['globalTitle']
        mangaInfoPersonal.writtenBy        = request.POST['writtenBy']
        mangaInfoPersonal.illustratedBy    = request.POST['illustratedBy']
        mangaInfoPersonal.publishedBy      = request.POST['publishedBy']
        mangaInfoPersonal.englishPublisher = request.POST['englishPublisher']
        mangaInfoPersonal.imprint          = request.POST['imprint']
        mangaInfoPersonal.magazine         = request.POST['magazine']
        mangaInfoPersonal.demographic      = request.POST['demographic']
        mangaInfoPersonal.originalRun      = request.POST['originalRun']
        mangaInfoPersonal.volumes          = request.POST['globalVolumes']

        # data validation - start
        if manga.title == "": 
            return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo':  mangaInfoPersonal, 'mangaGlobal': None, 'wrongTitle': True})

        if manga.status != "Reading" and manga.status != "Want to read" and manga.status != "Finished" and manga.status != "Abandoned":
            return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo':  mangaInfoPersonal, 'mangaGlobal': None, 'wrongStatus': True})

        if manga.finishedVolumes == "":
            return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo':  mangaInfoPersonal, 'mangaGlobal': None, 'wrongVolumes': True})

        if manga.endDate == "":
            return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo': mangaInfoPersonal, 'mangaGlobal': None, 'wrongDate': True})

        if manga.rating == "": 
            rating = 0  # 0 -> rating not defined

        if int(manga.rating) < 0 or int(manga.rating) > 10: # validation of number being integer is already done (by browser? type=integer in html)
            return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo': None, 'mangaGlobal': None, 'wrongRatingRange': True})
        # data validation end        

        if mangaInfoGlobalId == -1:         # something was changed in Info category (scraping doesnt count)
            mangaGlobal = None
            if mangaInfoPersonalId == "":   # there is no entry in Personal manga Info table
                mangaInfoPersonalNew = MangaInfoPersonal()
            else:                           # there is an entry in Personal manga info table, update it
                mangaInfoPersonalNew = MangaInfoPersonal.objects.filter(id = mangaInfoPersonalId).first()

            mangaInfoPersonalNew.title             = mangaInfoPersonal.title
            mangaInfoPersonalNew.writtenBy         = mangaInfoPersonal.writtenBy
            mangaInfoPersonalNew.illustratedBy     = mangaInfoPersonal.illustratedBy 
            mangaInfoPersonalNew.publishedBy       = mangaInfoPersonal.publishedBy
            mangaInfoPersonalNew.englishPublisher  = mangaInfoPersonal.englishPublisher 
            mangaInfoPersonalNew.imprint           = mangaInfoPersonal.imprint  
            mangaInfoPersonalNew.magazine          = mangaInfoPersonal.magazine
            mangaInfoPersonalNew.demographic       = mangaInfoPersonal.demographic
            mangaInfoPersonalNew.originalRun       = mangaInfoPersonal.originalRun 
            mangaInfoPersonalNew.volumes           = mangaInfoPersonal.volumes 
            mangaInfoPersonalNew.save()       #update

            if mangaId == "":   # there is no entry in personal manga table
                mangaNew = MangaPersonal() # .objects.create(title=manga.title,status=manga.status,finishedVolumes=manga.finishedVolumes,endDate=manga.endDate, rating=manga.rating, comment = manga.comment,mangaInfoPersonalId=mangaInfoPersonal.id, mangaGlobalId=None)
            else:               # there is an entry in table, update it
                mangaNew = MangaPersonal.objects.filter(id=mangaId).first()

            mangaNew.title = manga.title
            mangaNew.status = manga.status
            mangaNew.finishedVolumes = manga.finishedVolumes
            mangaNew.endDate = manga.endDate
            mangaNew.rating = manga.rating
            mangaNew.comment = manga.comment
            mangaNew.mangaInfoPersonalId = mangaInfoPersonal.id
            mangaNew.mangaGlobalId = None
            mangaNew.userId = user.id
            mangaNew.save()    # update
            manga = mangaNew
        else:                               # no changes in info category
            mangaInfoPersonal = None        # set manga info personal to none
            
            # mangaInfoGlobal added to table in WikiScraper, id of it is in mangaInfoGlobalId
            if mangaInfoGlobalId != "":
                mangaGlobal = MangaGlobal.objects.filter(id = mangaInfoGlobalId).first()
            else:   # there are no personal nor global informations about this manga
                mangaGlobal = None
                mangaInfoGlobalId = None

            if mangaId == "" or mangaId == None or mangaId =="None":   # there is no entry in personal manga table
                mangaNew = MangaPersonal()
            else:               # there is an entry in table, update it
                mangaNew = MangaPersonal.objects.filter(id=mangaId).first()
            mangaNew.title = manga.title
            mangaNew.status = manga.status
            mangaNew.finishedVolumes = manga.finishedVolumes
            mangaNew.endDate = manga.endDate
            mangaNew.rating = manga.rating
            mangaNew.comment = manga.comment
            mangaNew.mangaInfoPersonalId = None
            mangaNew.mangaGlobalId = mangaInfoGlobalId
            mangaNew.userId = user.id
            mangaNew.save()    # update
            manga = mangaNew

    if request.method == 'GET':
        mangaId = request.GET['mangaId']
        if mangaId == "None" or mangaId=="":
            manga = None
        else:
            manga = MangaPersonal.objects.filter(id=mangaId).first()

        mangaInfoId = request.GET['mangaInfoId']
        if mangaInfoId == "None" or mangaInfoId == "":
           mangaInfoPersonal = None
        else:
            mangaInfoPersonal = MangaInfoPersonal.objects.filter(id=mangaInfoId).first()

        mangaGlobalId = request.GET['mangaGlobalId']
        if mangaGlobalId == "None" or mangaGlobalId == "":
            mangaGlobal = None
        else:
            mangaGlobal = MangaGlobal.objects.filter(id=mangaGlobalId).first()
            
    return render(request, 'mangaAdd.html',{'manga': manga, 'mangaInfo': mangaInfo, 'mangaGlobal': mangaGlobal})

def mangaListModify(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    mangas = MangaPersonal.objects.filter(userId=user.id).order_by('title')

    for manga in mangas:    # check all rows (!!! :( ) and save data, TODO performence upgrade?

        manga.title = request.POST['title'+str(manga.id)]
        manga.status = request.POST['status'+str(manga.id)]
        manga.finishedVolumes = request.POST['finishedVolumes'+str(manga.id)]
        manga.endDate = request.POST['endDate'+str(manga.id)] 
        manga.rating = request.POST['rating'+str(manga.id)]
        manga.comment = request.POST['comment'+str(manga.id)]

        # TODO data validation; None here -> null in database
        if manga.endDate == "":
             manga.end = None

        manga.save()
    mangasVolumesList = viewMangasList(mangas)
    return render(request, 'mangaList.html',{'mangasVolumesList': mangasVolumesList})

def mangaInfo(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    mangaId       = request.GET['mangaId']
    mangaInfoId   = request.GET['mangaInfoId']
    mangaGlobalId = request.GET['mangaGlobalId']
    if mangaGlobalId != "None":
        manga = MangaGlobal.objects.filter(id=mangaGlobalId).first()
    elif mangaInfoId != "None":
        manga = MangaInfoPersonal.objects.filter(id = mangaInfoId).first()
    else:
        manga = MangaGlobal('none','none','none','none','none','none','none','none','none',volumes=0)
    return render(request, 'mangaInfo.html',{'manga': manga, 'mangaId':mangaId, 'mangaInfoId': mangaInfoId, 'mangaGlobalId': mangaGlobalId})

def mangaDelete(request):   # TODO check if an id of logged user is the same as an id of the user that anime is related with
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    mangaPersonalId = request.GET['mangaId']
    mangaPersonal = MangaPersonal.objects.filter(id=mangaPersonalId).first()

    if mangaPersonal.userId == user.id: # <- here
        mangaPersonal.delete()

    mangas = MangaPersonal.objects.filter(userId=user.id).order_by('title')
    mangasVolumesList = viewMangasList(mangas)

    return render(request, 'mangaList.html',{'mangasVolumesList': mangasVolumesList})
