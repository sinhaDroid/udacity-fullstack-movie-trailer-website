"""
this module contains the movie class that will be used in the
entertainment_center.py file
"""


class Movie():

    """
    Movie object is initialized below.
    title:
        should be the formal movie title as seen in IMDB
    art:
        needs to be the fully qualifed image address or url
        ex. "https://www.google.com/images/srpr/logo11w.png"
    trailer:
        needs to be the youtube watch link
        ex. "https://www.youtube.com/watch?v=u_CkKm7m6TM"
    director:
        should be a single name as listed in IMDB
    actors:
        can be list of no more than 3 actors/actresses as listed in IMDB
    release:
        must be the integer year in the following format 'yyyy'
    criterion:
        if the movie is a criterion release value should be boolen True,
        else False
    criterion_icon:
        should be set to a null object value. this will be overwritten in the
        fresh_tomatoes.py file module based on the criterion boolean value and
        will display the criterion logo next to the year attribute in the
        movie tile.
    """
    def __init__(self, title, art, trailer, director, actors, release, criterion, criterion_icon):
        self.title = title
        self.art = art
        self.trailer_url = trailer
        self.director = director
        self.actors = actors
        self.release_date = release
        self.criterion = criterion
        self.criterion_icon = criterion_icon
