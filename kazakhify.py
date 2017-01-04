# coding: utf-8
from grab import Grab
import mymodel
from grab.spider import Spider, Task
import logging
import sys
import db
reload(sys)
sys.setdefaultencoding('utf8')

kaz_chars = [u'\u04D8', u'\u04D9', u'\u0492', u'\u0493', \
            u'\u049A', u'\u049B', u'\u04A2', u'\u04A3', \
            u'\u04E8', u'\u04E9', u'\u04B0', u'\u04B1', \
            u'\u04AE', u'\u04AF', u'\u04BA', u'\u04BB', \
            u'\u0406', u'\u0456']

logging.basicConfig(level=logging.DEBUG)

def hasKazSymbols(target):
    return any(char in kaz_chars for char in target)

class Kazakhify(Spider):

    initial_urls = ['http://sazalem.com/musician-card/1']

    def __init__(self, thread_number, link, id):
        self.link = link
        self.id = id
        super(Kazakhify, self).__init__()

    def prepare(self):
        pass

    def task_initial(self, grab, task):
        grab = Grab()
        url = self.link
        grab.setup(url=url)
        grab.request()
        song_names = grab.doc.select('//div[@class="musician_songs_item_text"]/h2/a')
        for s in song_names:
            if hasKazSymbols(s.text()):
                print self.id
                db.session.query(mymodel.Artist).filter(mymodel.Artist.id == self.id)[0].lang = "kz"
                db.session.commit()

for artist in db.session.query(mymodel.Artist).all():
    if hasKazSymbols(artist.fullname):
        artist.lang = "kz"
        db.session.commit()
    else:
        bot = Kazakhify(thread_number=1, link=artist.link, id=artist.id)
        bot.run()
