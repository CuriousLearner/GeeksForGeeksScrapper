class Article(object):
    """ This Class Contains the title and the content of the article.
    The title can be use as key to the article link for the navigation purpose. """

    def __init__(self, title, content):
        self.title = title
        self.content = content
