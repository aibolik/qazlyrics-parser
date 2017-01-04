# coding: utf-8
from grab import Grab
import mymodel
from grab.spider import Spider, Task
import logging
import sys
import db
reload(sys)
sys.setdefaultencoding('utf8')

class Parser(Spider):

    initial_urls = ['http://sazalem.com/musician-card']

    def prepare(self):
        pass

    def task_initial(self, grab, task):
        grab = Grab()
        counter = 0
        num = 4300
        while(counter < num):
            url = 'http://sazalem.com/musician-card/' + str(counter)
            grab.setup(url=url)
            grab.request()
            artist_name = grab.xpath_text('//div[@class="musician_card_text"]/h1')
            if artist_name:
                print artist_name
                yield Task('take', grab=grab, link=url)

            counter = counter + 1

    def task_take(self, grab, task):
        artist = {
            "fullname": None,
            "img": None,
            "link": None
        }
        try:
            artist['link'] = task.get('link')
            print artist['link']

        except:
            pass

        try:
            artist['fullname'] = grab.xpath_text('//div[@class="musician_card_text"]/h1')
            print artist['fullname']
        except:
            pass

        try:
            item = db.session.query(mymodel.Artist).filter(mymodel.Artist.link == str(artist['link'])).first()
            if (item != None):
                print("done")
            else:
                new = mymodel.Artist(
                    fullname = artist['fullname'],
                    link = artist['link'],
                    img = None
                )
                db.session.add(new)
                db.session.commit()
        except:
            raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig()
    # Let's start spider with two network concurrent streams
    bot = Parser(thread_number=1)
    bot.run()
