import datetime
import re


class BlogPost:
    def __init__(self, title="", date="", post_content="", slug=""):
        self.title = title
        self.date = date
        self.post_content = post_content
        self.slug = slug

    # getters and setters of instance variables
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title.strip()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def post_content(self):
        return self._post_content

    @post_content.setter
    def post_content(self, post_content):
        self._post_content = post_content.strip()

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, slug):
        self._slug = slug

    # instance methods of the class
    def get_date(self) -> datetime.date:
        self.date = datetime.date.today()
        return self.date

    def build_slug(self) -> str:
        self.slug = self.title.lower().strip()
        self.slug = self.slug.replace(" ", "-")
        self.slug = re.sub(r"[\.,\?\:\+!'\"]", "", self.slug)
        return self.slug

    def edit_post(self, post_id, edit, read_post, data_model):
        self.post_id = post_id
        self.edit = edit
        self.read_post = read_post
        self.data_model = data_model

        post = self.read_post(self.post_id)
        post = post.model_dump()
        post_model = self.data_model(**post)
        data_to_update = self.edit.model_dump(exclude_unset=True)
        new_slug = ""
        for data in data_to_update:
            if "title" == data:
                new_slug = self.update_slug(data_to_update[data])
        data_to_update.update({"slug": new_slug})
        return post_model.model_copy(update=data_to_update)

    def update_slug(self, new_title):
        self.new_title = new_title
        self.title = self.new_title
        new_slug = self.build_slug()
        return new_slug
