from random import randint
from flask import request
from flask_restful import Resource, Api
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from datetime import datetime, date
from project.models import Post, PostSchema
from project.models import db
import bcrypt, hashlib, jwt
from project.config.config import Config

post_schema = PostSchema()

post_api = Blueprint("post_api", __name__, url_prefix="/posts")
api = Api(post_api)

# /posts

def createPost(userId, routeId, plannedStartDate, plannedEndDate):
    
    if(userId is None):
        return {"error": True, "message": "No hay usuario identificado"}
    
    if(routeId is None):
        return {"error": True, "message": "No hay ruta identificada"}
    
    if(plannedStartDate is None):
        return {"error": True, "message": "No hay fecha inicial"}
    
    if(plannedEndDate is None):
        return {"error": True, "message": "No hay fecha inicial"}

    nuevo_post = Post(routeId=routeId, plannedStartDate=plannedStartDate, plannedEndDate=plannedEndDate, userId=userId)
    db.session.add(nuevo_post)
    db.session.commit()
    return {'id': nuevo_post.id, "userId": nuevo_post.userId, "createdAt": nuevo_post.createdAt.strftime('%Y-%m-%dT%H:%M:%S. %f%z')}

class PostResource(Resource):


    def get(self):

        token_header = request.headers.get('Authorization', None)

        if not token_header:

            return {"message": "Bearer token is missing in request",
                    "status": "fail"
                    }, 400

        token = token_header.split(" ")[1]

        try:
            userId = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])['sub']
        except (jwt.exceptions.InvalidTokenError, KeyError):
            return {
                    "message": "Token not valid", 
                    "status": "fail"
                    }, 401

        startDateFilter = request.args.get('when')
        routeId = request.args.get('route')
        isFilter = request.args.get('filter')

        if(all(v is None for v in [startDateFilter,routeId,isFilter])):
            return [post_schema.dump(posts) for posts in Post.query.all()]
        
        queryPosts = Post.query.filter()

        if isFilter is not None:
            if (isFilter.upper() == "ME"):
                queryPosts = queryPosts.filter(Post.userId == userId)
        
        if startDateFilter is not None:
            startDatePost = datetime.strptime(startDateFilter,'%Y-%m-%d')
            queryPosts = queryPosts.filter(Post.plannedStartDate == startDatePost)

        if routeId is not None:    
            queryPosts = queryPosts.filter(Post.routeId == routeId)
        
        return [post_schema.dump(post) for post in queryPosts.all()]
          
    
    def post(self):
        #userId = 1
        
        token_header = request.headers.get('Authorization', None)

        if not token_header:
            
            return {"message": "Bearer token is missing in request",
                    "status": "fail"
                    }, 400
        
        token = token_header.split(" ")[1]

        try:
            userId = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])['sub']
        except (jwt.exceptions.InvalidTokenError, KeyError):
            return {
                    "message": "Token not valid", 
                    "status": "fail"
                    }, 401
        

        if 'routeId' not in request.json or 'plannedStartDate' not in request.json or 'plannedEndDate' not in request.json:
            return {
                    "message": "All fields are required", 
                    "status": "fail"
                    }, 400
        
        routeId = request.json["routeId"]
        plannedStartDate = request.json["plannedStartDate"]
        plannedEndDate = request.json["plannedEndDate"]

        if not all([routeId, plannedStartDate, plannedEndDate]):
            return {
                    "message": "All fields are required", 
                    "status": "fail"
                    }, 400

        try:
            date.fromisoformat(request.json["plannedStartDate"])
        except ValueError:
            return {'message': 'Fecha plannedStartDate Invalida'}, 412

        try:
            date.fromisoformat(request.json["plannedEndDate"])
        except ValueError:
            return {'message': 'Fecha plannedEndDate Invalida'}, 412


        startDate = datetime.strptime(plannedStartDate,'%Y-%m-%d')
        endDate = datetime.strptime(plannedEndDate,'%Y-%m-%d')
        nuevo_post = Post(routeId=routeId,userId=userId,
                                 plannedStartDate=startDate,
                                 plannedEndDate=endDate)
        db.session.add(nuevo_post)
        db.session.commit()
        return {"id": nuevo_post.id, "userId": nuevo_post.userId, "createdAt": nuevo_post.createdAt.strftime('%Y-%m-%dT%H:%M:%S. %f%z')},201
                                     

# /posts/<int:id_post>
class ViewPost(Resource):
    def get(self, id_post):
        return post_schema.dump(Post.query.get_or_404(id_post))


# /posts/ping
class PingPostResource(Resource):

    def get(self):
        return {"message": "pong", "status": "success"}


class TokenPostExample(Resource):

    def get(self):
        return {"token": create_access_token(randint(0,100))} 
    
api.add_resource(PostResource, '/')
api.add_resource(PingPostResource, '/ping')
api.add_resource(TokenPostExample, '/getToken')
api.add_resource(ViewPost, '/<int:id_post>')

#api.add_resource(PostResource, '/posts')
#api.add_resource(PingPostResource, '/posts/ping')
#api.add_resource(ViewPost, '/posts/<int:id_post>')