import datetime


class Comment:
    def __init__(self, date="", content=""):
        self.date = date
        self.content = content

    # getters and setters of the instance variables
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content.strip()

    # static methods
    @staticmethod  # returns a 404 error for when a post is not found
    def post_check(post_id: int, read_post, *args, exception):
        if not read_post(*args):
            raise exception(status_code=404, detail=f"Post {post_id} does not exist")

    # instance methods of the class
    def get_date(self) -> datetime.date:
        self.date = datetime.date.today()
        return self.date
