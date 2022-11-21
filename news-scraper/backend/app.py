import api
import database as db
from news_scraper import BBC


def send_to_db(stories):
    for s in stories:
        title = s.get("title")
        link = s.get("link")
        tag = s.get("tag")

        db.send_title(title)

        id = db.get_story_id(title)

        db.send_tag(tag)

        tag_id = db.get_tag_id(tag)

        db.send_link(id, link)
        db.send_metadata(id, tag_id)


def main():
    bbc = BBC("http://bbc.co.uk")
    stories = bbc.parse_articles()
    send_to_db(stories)


if __name__ == "__main__":
    main()
    api.app.run(debug=True, host="127.0.0.1")

class Story(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key = True)
    title = db. Column(db.Text, nullable = False)
    url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable = False, default=0)

    def __repr__(self):
        return '<Story %r>' % self.title