from os import environ
from Kinderly import app

if __name__ == '__main__':
    HOST = environ.get
    try:
        PORT = int(environ.get)
    except ValueError:
        PORT = 5000

    app.run(host=HOST, port=PORT, debug=True)
