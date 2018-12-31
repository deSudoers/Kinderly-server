from os import environ
from Kinderly import app

if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 5000

    app.run(host=HOST, port=PORT, debug=True)
