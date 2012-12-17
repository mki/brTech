# coding: utf-8

'''
    Команда для обноваления базы

'''
from django.core.management.base import BaseCommand

import csv
import sys
import urllib2
import lxml.html
import  re
from bs4 import BeautifulSoup

from main.models import Country, City, Airport
from progressbar import ProgressBar

class Command(BaseCommand):
    def handle(self, *args, **options):
        print '\n'
        print '***DEMO OF GRAB DATA***'

        # Метод подготовки данных
        grab_data()

        print '\n'
        print '***START***'

        countreis()
        cities()
        airs()

        print '\n'
        print '***DONE***'
        print '\n'


def grab_data():
    '''
        Метод для обновления данных в CSV файле.
        Формирует новый csv файл с заполненными недостающими данными.

        В данном методе приведен пример парсера страницы и поиска необходимых данных.
        Ресурс блокирует запросы. Подделать их не получилось.

        Данный метод служит для ознакомления с логикой организации процесса парсинга.
    '''

    writer = csv.writer(open('../airbase_new.csv', 'wb'), delimiter=',',quotechar='"')
    base, prog = get_data()
    count_notfound = 0
    source_1 = 'http://www.flightstats.com/go/Airport/airportDetails.do?airportCode=%s'
    for row in base:
        for r in row:
            if not r:
                if row[5] and row[5] != '\\N':
                    opener = urllib2.build_opener()

                    # Пытаемся подделать заголовки
                    opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1'))
                    opener.addheaders.append(("Content-type", "text/html;charset=UTF-8"))
                    opener.addheaders.append(("Connection", "keep-alive"))
                    opener.addheaders.append(("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"))
                    opener.addheaders.append(("Accept-Language", "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"))
                    opener.addheaders.append(("Cache-Control", "max-age=0"))
                    opener.addheaders.append(("Cookie", "FS_tokenIQL=81132C10B894055548DA955F1BEFE5EE.web4:8009; __utma=104620247.264456425.1354120216.1354123105.1354217870.3; __utmz=104620247.1354120216.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=nanded%20airport; __qca=P0-666531997-1354120215886; s_lastvisit=1354223163573; rsi_segs=D08734_70008|D08734_70107|D08734_72015|D08734_72080|D08734_72081|D08734_70012|D08734_70033|D08734_70018|D08734_70022|D08734_70028|J06575_10396|J06575_10352; __gads=ID=88ce3dacf03fd104:T=1354120223:S=ALNI_MYywm0TBI4W-j5VWe0FFxjMUh8kGg; JSESSIONID=81132C10B894055548DA955F1BEFE5EE.web4:8009; usat_dslv=Less%20than%201%20day; __utmc=104620247; s_cc=true; s_sq=%5B%5BB%5D%5D; s_ppv=66; __utmb=104620247.30.9.1354223371136; s_pv=usat%20%3A%2Fflightstatspages"))

                    # Отправляем запрос
                    page = opener.open(source_1%('YFRT'))
                    try:
                        # Получаем ответ
                        page_content = page.read()

                        # Допустим мы получили данные со страницы
                        # Фрагмент взят из реальной страницы ресурса
                        page_content = '''<div class="airportOverviewDetailsColumn">
                                        <span class="airportOverviewLabel">Current Time / Date:</span><br>
                                        5:09 AM /
                                        Fri Nov-30-2012<br><br>
                                        <span class="airportOverviewLabel">Airport Code:</span><br>
                                        FlightStats code: FOS<br>
                                        IATA code: FOS<br>
                                        ICAO code: YFRT<br>
                                        FAA code: <br><br>
                                    </div>'''

                        # Передаем данные в парсер
                        soup = BeautifulSoup(page_content)
                    except:
                        soup = ''
                        print 'error'

                    # Ищим строку с нужными нам данными
                    iata_source = soup.find_all(text=re.compile('IATA'))[0]

                    # Получаем и обрабатываем конечное значение
                    try:
                        iata = str(iata_source).split(':')[1].strip()
                    except:
                        print '   No iata value'
                        iata = ''

                    print 'OLD CSV STRING', row

                    # Изменяем данные
                    row[4] = iata

                    # Записываем строку в новый CSV файл
                    writer.writerow(row)

                    print 'NEW CSV STRING', row

                    count_notfound += 1

        if count_notfound == 1:
            break


def get_data():
    base = csv.reader(open('../airports.dat','rb'), delimiter=",")

    count = 0
    total = 6989
    prog = ProgressBar(count, total, 70, mode='fixed', char='#')

    return base, prog


def countreis():
    print '\n'
    print 'Import/Update Country'

    base, prog = get_data()

    for row in base:

        try:
            country = Country.objects(name_eu = row[3])[0]
        except:
            country = Country(name_eu = row[3])

        country.name_ru = row[3]
        country.slug = '%s' % (str(row[3]).replace(' ','_'))
        country.save()

        prog.increment_amount()
        print prog, '\r',
        sys.stdout.flush()


def cities():
    base, prog = get_data()

    print '\n'
    print 'Import/Update City'

    for row in base:
        try:
            city = City.objects(name_eu = row[2])[0]
        except:
            city = City(name_eu = row[2])

        city.name_ru = row[2]
        city.country = Country.objects(name_eu = row[3])[0]
        city.slug = '%s' % (str(row[2]).replace(' ','_'))
        city.save()

        prog.increment_amount()
        print prog, '\r',
        sys.stdout.flush()


def airs():
    base, prog = get_data()

    print '\n'
    print 'Import/Update Airport'

    for row in base:
        try:
            city = Airport.objects(name_eu = row[1])[0]
        except:
            city = Airport(name_eu = row[1])

        city.name_ru = row[1]
        city.location = (float(row[6]),float(row[7]))
        city.altitude = row[8]
        city.timezone = float(row[9])
        city.dst = row[10]
        city.city = City.objects(name_eu = row[2])[0]
        city.slug = '%s' % (str(row[1]).replace(' ','_'))
        city.save()

        prog.increment_amount()
        print prog, '\r',
        sys.stdout.flush()