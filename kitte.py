import os.path

from flask import Flask
from flask_restful import Api, Resource, reqparse

import werkzeug

from subprocess import Popen

#from playsound import playsound

class Kitte(Resource):

    FILES_DIR = "/var/www/kitte/media"
    PLAYER = "/usr/bin/play"

    def get(self, name):
        if not name:
            return "No file specified", 400
    
        path = os.path.join(Kitte.FILES_DIR, name + ".mp3")
        print(path)
        if not os.path.isfile(path):
            return "File not found", 400

        #playsound(path)

        p = Popen([Kitte.PLAYER, path])

        return "OK", 200

    def post(self, name):
        if not name:
            return "No file specified", 400

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        
        args = parse.parse_args()
        audioFile = args['file']
        
        if not audioFile:
            return "No file to upload", 400

        audioFile.save(os.path.join(Kitte.FILES_DIR, name + ".mp3"))

        return "OK", 201

    pass

app = Flask(__name__)
api = Api(app)
api.add_resource(Kitte, "/kitte/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)
