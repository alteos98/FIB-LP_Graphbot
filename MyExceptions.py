class MyExceptions(Exception):
    pass

class LocationException(MyExceptions):
    text = 'You have to share your location with me first'

class MapRenderException(MyExceptions):
    text = 'There are no nodes and/or edges to paint with these conditions'

class NoGraphLoadedException(MyExceptions):
    text = 'There is no graph loaded or no data available, please use /start at first'