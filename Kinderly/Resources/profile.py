from flask_restful import Resource, reqparse, request
from werkzeug import datastructures
import os

from Kinderly.Controller.user import UserManager

UPLOAD_FOLDER = 'Kinderly/static/profile'
parser = reqparse.RequestParser()


class UserProfile(Resource):
    def get(self):
        if UserManager.is_authenticated():
            user = UserManager.current_user()
            return UserManager.info(user), 200
        return {"message": "User not logged in."}, 401

    def post(self):
        if UserManager.is_authenticated():
            photo = request.files['profile']
            if photo:
                filename = str(UserManager.current_user().user_id) + ".jpg"
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                UserManager.update_image(filename)
                return {"message": "Profile picture saved"}, 200
            else:
                return {'message':'No file found'}, 500
        return {"message": "User not logged in."}, 401
