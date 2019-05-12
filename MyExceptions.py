class MyExceptions(Exception):
    pass

class LocationException(MyExceptions):
    text = 'You have to share your location with me first'