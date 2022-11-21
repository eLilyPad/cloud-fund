from urllib.request import urlopen
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs


class BBC:
    def __init__(self, url: str):
        self.url = url
        html = urlopen(url).read().decode("utf_8")
        self.soup = bs(html, "html.parser")

    cont_class = ".e1f5wbog7"
    story_class = ".e1f5wbog0"
    metadata_class = ".ecn1o5v1"

    def _articles(self):
        return self.soup.select(BBC.cont_class)

    def parse_articles(self):
        stories = []
        articles = self._articles()

        only1 = lambda v: len(v) == 1
        for article in articles:
            story = article.select(BBC.story_class)
            metadata = article.select(BBC.metadata_class)
            if only1(story) and only1(metadata):
                try:
                    s = story[0]
                    title = s.get_text()
                    link = s.get("href")
                    tag = metadata[0].get_text()
                    stories.append({"title": title, "link": link, "tag": tag})
                except Exception as e:
                    print(e.with_traceback())
        return stories
