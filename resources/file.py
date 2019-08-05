from flask_restful import Resource

class File(Resource):
    def get(self):
        return {"message":"Hello, World","api":"File"}

    def post(self):
        return {"message":"Hello", "api":"File"}


