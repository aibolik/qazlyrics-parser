    # coding: utf-8
from grab import Grab
from grab.spider import Spider, Task
from time import sleep
from datetime import datetime
from time import strftime, gmtime
from hashlib import md5
import db
import model
import imghdr
import os
import logging
import html2text # надо установить
import urllib
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
global check

def giveRegionId(name):
    if u'Кокшетау' in name:
        return 11
    if u'Акмол' in name:
        return 11

    if u'Актюб' in name:
        return 15
    if u'Актоб' in name:
        return 15

    if u'Западно' in name:
        return 27
    if u'ЗКО' in name:
        return 27
    if u'Уральск' in name:
        return 27

    if u'Алматинская область' in name:
        return 19
        
    if u'Атырау' in name:
        return 23
    
    if u'Тараз' in name:
        return 31
    if u'Жамбыл' in name:
        return 31

    if u'Караган' in name:
        return 35

    if u'Кызылорд' in name:
        return 43

    if u'Костанай' in name:
        return 39
    if u'Рудный' in name:
        return 39
    if u'Житикара' in name:
        return 39

    if u'Южно-Казахстанская' in name:
        return 51
    if u'Шымкент' in name:
        return 51
    if u'Сузак' in name:
        return 51
    if u'ЮКО' in name:
        return 51
    
    if u'Мангистау' in name:
        return 47
    if u'Актау' in name:
        return 47
    
    if u'Петропавлск' in name:
        return 59
    if u'СКО' in name:
        return 59
    if u'Северо-Казахстанская' in name:
        return 59

    if u'Павлодар' in name:
        return 55

    if u'ВКО' in name:
        return 63 
    if u'Восточно-Казахстанская' in name:
        return 63
    if u'Семей' in name:
        return 63
    if u'Усть-Каменогорск' in name:
        return 63


    if u'Астана' in name:
        return 71

    if u'Алматы' in name:
        return 75
    if u'Бостандыкский' in name:
        return 75
    if u'Медеуский' in name:
        return 75
    if u'Алмалинский' in name:
        return 75

    return None

class GosZakup(Spider):

    initial_urls = ['https://e-auction.gosreestr.kz/p/']
    def __init__(self,thread_number, num):
        self.check = True
        self.num = num
        super(GosZakup, self).__init__()

    def prepare(self):
        pass

    def task_initial(self, grab, task):
        self.check = True
        grab = Grab()
        counter = 0
        self.num = 45000
        while(self.check == True):
            url = 'https://e-auction.gosreestr.kz/p/ru/GuestViewAuction?AuctionId=' + str(self.num)
            grab.setup(url=url)
            grab.request()
            sleep(1)
            if "Ошибка исполнения" in grab.doc.select('//*[@id="title-and-local-tasks"]').text():
                counter = counter + 1

            if counter == 100:
                self.check = False

            if self.check == True:
                yield Task('take',grab=grab,num=self.num,link=url)

            self.num = self.num + 1

    def task_take(self, grab, task):
        info = {
            "name":None,           #наименование
            "number":None,         #номер аукциона
            "start_price":None,    #стартовая цена
            "type":None,           #тип торгов
            "periodicity":None,    #периодичность оплаты
            "minimum":None,        #минимальная цена
            "garanty":None,        #гарантийный взнос
            "status":None,         #статус торгов
            "start_at":None,       #начало торгов
            "rent_pay":None,       #арендный платеж
            "add_info":None,       #дополнительная информация
            "sell_price":None,     #цена продажи
            "organ":None,          #уполномоченный орган
            "object":None,         #объект продажи
            "balance":None,        #балансодержатель
            "seller":None,         #продавец
            "requisites":None,     #реквезиты
            "publication":None,    #публикация
            "method":None,         #метод проведения
            "conditions":None,     #тендерные условия
            "for_physical":None,   #для физ.лиц
            "for_juridical":None,  #для юр.лиц
            "for_individ":None,    #для ИП
            "imagePath":None,      #путь к картинкам
            "link":None,           #ссылка
            "parsed_at":None,      #when was parsed
            "region_id":None       #id of region, takes from seller
        }
        try:
            info['number'] = task.get('num')
            info['link'] = task.get('link')
        except:
            pass

        pathOfImages = []          #путь к картинкам
        try:
            temp = grab.doc.select('//*[@id="photoGallery_origSlider"]//img')
            for tem in temp:
                path = '/home/xelfer/parser/gosreestr/images/' + str(md5(tem.attr('data-lazy')).hexdigest())
                urllib.urlretrieve('https://e-auction.gosreestr.kz' + tem.attr('data-lazy'), path)
                filepath= path + "." + str(imghdr.what(path))
                os.rename(path, path + "." + str(imghdr.what(path)))
                pathOfImages.append(filepath)
        except:
            pass
        
        try:
            info['imagePath'] = pathOfImages
        except:
            pass
        
        try:
            info['name'] = grab.doc.select('//tbody/tr[1]/td[2]/div[1]').text()
        except:
            pass

        try:
            info['type'] = grab.doc.select(u'//span[text()="Тип торгов:"]/..//span[2]').text()
        except:
            pass

        try:
            info['start_price'] = grab.doc.select(u'//span[text()="Стартовая цена:"]/..//span[2]').text()
        except:
            pass

        try:
            info['periodicity'] = grab.doc.select(u'//span[text()="Периодичность оплаты:"]/..//span[2]').text()
        except:
            pass

        try:
            info['garanty'] = grab.doc.select(u'//span[text()="Гарантийный взнос:"]/..//span[2]').text()
        except:
            pass

        try:
            info['status'] = grab.doc.select(u'//span[text()="Статус торгов:"]/..//span[2]').text()
        except:
            pass

        try:
            info['start_at'] = grab.doc.select(u'//span[text()="Начало торгов:"]/..//span[2]').text()
        except:
            pass

        try:
            info['rent_pay'] = grab.doc.select(u'//span[text()="Арендный платеж:"]/..//span[2]').text()
        except:
            pass

        try:
            info['add_info'] = grab.doc.select(u'//span[text()="Дополнительная информация:"]/..//span[2]').text()
        except:
            pass

        try:
            info['minimum'] = grab.doc.select(u'//span[text()="Минимальная цена:"]/..//span[2]').text()
        except:
            pass

        try:
            info['sell_price'] = grab.doc.select(u'//span[text()="Цена продажи:"]/..//span[2]').text()
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Объект продажи':
                    info['object'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Объект аренды':
                    info['object'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Балансодержатель':
                    info['balance'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Уполномоченный орган':
                    info['organ'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Продавец':
                    info['seller'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Наймодатель':
                    info['seller'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Реквизиты для перечисления гарантийного взноса':
                    info['requisites'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Публикация':
                    info['publication'] = temp_array[z+1].text()
                z = z + 1
        except:
            pass

        try:
            temp_array = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//td')
            z = 0
            for item in temp_array:
                if item.text() == 'Метод проведения':
                    info['method'] = grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//tr['+str(z+2)+']/td//text()').text()
                    temp = html2text.html2text(grab.doc.select(u'//td[contains(@class, "auction-all-description")]//tbody//tr['+str(z+2)+']//span').attr('fulldescription'))
                    info['method'] = info['method'] + temp
                z = z + 1
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[1]').text()
            if u'Тендерные (конкурсные) условия' in x:
                info['conditions'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[1]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
            if u'Тендерные (конкурсные) условия' in x:
                info['conditions'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
            if u'Тендерные (конкурсные) условия' in x:
                info['conditions'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
            if u'Тендерные (конкурсные) условия' in x:
                info['conditions'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
        except:
            pass


        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
            if u'Требуемые файлы для физ.' in x:
                info['for_physical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
            if u'Требуемые файлы для физ.' in x:
                info['for_physical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
            if u'Требуемые файлы для физ.' in x:
                info['for_physical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
        except:
            pass


        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
            if u'Требуемые файлы для юр.' in x:
                info['for_juridical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
            if u'Требуемые файлы для юр.' in x:
                info['for_juridical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
            if u'Требуемые файлы для юр.' in x:
                info['for_juridical'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
        except:
            pass


        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
            if u'Требуемые файлы для ИП' in x:
                info['for_individ'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[2]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
            if u'Требуемые файлы для ИП' in x:
                info['for_individ'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[3]').text()
        except:
            pass

        try:
            x  = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
            if u'Требуемые файлы для ИП' in x:
                info['for_individ'] = grab.doc.select('//div[@id="auction-req-files-panel"]/div[4]').text()
        except:
            pass

        try:
            info['start_at'] = info['start_at'] + ":00"
            info['start_at'] = datetime.strptime(info['start_at'], '%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

        try:
            info['start_price'] = info['start_price'][:-3:]
            info['start_price'] = int(info['start_price'].replace(" ",""))
        except:
            pass

        try:
            info['minimum'] = info['minimum'][:-3:]
            info['minimum'] = int(info['minimum'].replace(" ",""))
        except:
            pass

        try:
            info['garanty'] = info['garanty'][:-3:]
            info['garanty'] = int(info['garanty'].replace(" ",""))
        except:
            pass

        try:
            info['sell_price'] = info['sell_price'][:-3:]
            info['sell_price'] = int(info['sell_price'].replace(" ",""))
        except:
            pass

        try:
            info['rent_pay'] = info['rent_pay'][:-3:]
            info['rent_pay'] = int(info['rent_pay'].replace(" ",""))
        except:
            pass

        try:
            info['region_id'] = giveRegionId(info['seller'])
        except:
            pass

        try:
            item1 = db.session.query(model.AuctionBase).filter(model.AuctionBase.link == str(info['link'])).first()
            if (item1 != None):
                print("done")
            else:
                new = model.AuctionBase(
                    name = info['name'],
                    number = info['number'],
                    start_price = info['start_price'],
                    typeof = info['type'],
                    periodicity = info['periodicity'],
                    minimum = info['minimum'],
                    garanty = info['garanty'],
                    status = info['status'],
                    start_at = info['start_at'],
                    rent_pay = info['rent_pay'],
                    add_info = info['add_info'],
                    sell_price = info['sell_price'],
                    organ = info['organ'],
                    obj = info['object'],
                    balance = info['balance'],
                    seller = info['seller'],
                    requisites = info['requisites'],
                    publication = info['publication'],
                    method = info['method'],
                    conditions = info['conditions'],
                    for_physical = info['for_physical'],
                    for_juridical = info['for_juridical'],
                    for_individ = info['for_individ'],
                    imagePath = info['imagePath'],
                    link = info['link']
                    parsed_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    region_id = info['region_id']
                    )

                db.session.add(new)
                db.session.commit()
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig()
    # Let's start spider with two network concurrent streams
    bot = GosZakup(thread_number=1,num=45000)
    bot.run()

