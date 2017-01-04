# coding: utf-8
from grab import Grab
import mymodel
from grab.spider import Spider, Task
import logging
import sys
import db
reload(sys)
sys.setdefaultencoding('utf8')

host = "http://sazalem.com"

class Texts(Spider):

    initial_urls = ['http://sazalem.com/musician-card']

    def prepare(self):
        pass

    def task_initial(self, grab, task):
        grab = Grab()
        for artist in db.session.query(mymodel.Artist).filter(mymodel.Artist.lang == 'kz').all():
            grab.setup(url=artist.link)
            grab.request()
            yield Task('songs', grab=grab, link=artist.link, artist_id=artist.id)

    def task_songs(self, grab, task):
        link = task.get('link')
        artist_id = task.get('artist_id')
        song_links = grab.doc.select('//div[@class="musician_songs_item_text"]/h2/a/@href')
        for l in song_links:
            song_link = host + l.text()
            grab2 = Grab()
            grab2.setup(url=song_link, timeout=30)
            grab2.request()
            yield Task('lyrics', grab=grab2, link=song_link, artist_id=artist_id)

    def task_lyrics(self, grab, task):
        link = task.get('link')
        artist_id = task.get('artist_id')
        title = grab.doc.select('//div[@class="track_back_descr_text"]/h1').text()
        item = db.session.query(mymodel.Song).filter(mymodel.Song.link == link).first()
        if item != None:
            print "Done!"
        else:
            try:
                texts = grab.doc.select('//div[@class="track_inner_left_fulltext"]/text()[preceding-sibling::br]')
                text = ""
                for t in texts:
                    text = text + t.text()
                    text = text + "\n"
                new = mymodel.Song(
                    title=title,
                    artist_id=artist_id,
                    link=link,
                    text=text
                )
                db.session.add(new)
                db.session.commit()
            except:
                raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig()
    # Let's start spider with two network concurrent streams
    bot = Texts(thread_number=1)
    bot.run()
