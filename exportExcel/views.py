import io
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from Diary.models import AnimePersonal
from Diary.models import AnimeInfoPersonal
from WikiScraper.models import AnimeGlobal
import xlsxwriter as excelWriter

from Diary.views import viewAnimeList

# Create your views here.

#format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
#worksheet.write('A2', number, format2)       # 28/02/13

def exportAnime(request):

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    animes = AnimePersonal.objects.filter(userId=user.id)
    aniEpiList = viewAnimeList(animes)

    output = io.BytesIO()

    workbook = excelWriter.Workbook(output, {'in_memory': True})
    dateFormat = workbook.add_format({'num_format': 'dd/mm/yy'})    # https://xlsxwriter.readthedocs.io/working_with_dates_and_time.html
    worksheet = workbook.add_worksheet("Anime") # write (y,x)

    worksheet.write(0, 0, 'Title')      
    worksheet.write(0, 1, 'Episodes')  
    worksheet.write(0, 2, 'Status')  
    worksheet.write(0, 3, 'End date')  
    worksheet.write(0, 4, 'Rating')  
    worksheet.write(0, 5, 'Comment')      
    y = 1
    for anime, epi in aniEpiList:
        worksheet.write(y, 0, anime.title)
        worksheet.write(y, 1, str(anime.finishedEpisodes) +"/"+ str(epi))  
        worksheet.write(y, 2, anime.status)
        worksheet.write(y, 3, anime.endDate, dateFormat)
        worksheet.write(y, 4, str(anime.rating))
        worksheet.write(y, 5, anime.status)
        y += 1

    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=animeExport.xlsx"

    output.close()

    return response
