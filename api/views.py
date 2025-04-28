from forms.models import created_forms
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User #dont create own user table!
from forms.serializers import FormsSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import AccessToken

import json

# main api code here!

@api_view(["GET", "POST", "PUT","DELETE"])
def forms(request, id):
    """ /api/forms/id function """
    try:
        if request.method == "GET":
            model_data = created_forms.objects.get(pk=id)
            data={}
            if model_data:
                data = FormsSerializer(model_data).data

        elif request.method == "POST":
            #curl --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1ODI5MjI5LCJpYXQiOjE3NDU4Mjc0MjksImp0aSI6IjMzM2FjODQ1YjMzMzRlMzJhMmFiMDAxNjMxYjU3ZjkwIiwidXNlcl9pZCI6MX0.v822Z5kGunt5G2pzwR7eg4_2VYMGberJraSyozLphiA' -d '{"title": "a44444dmin", "content": "admi44444n"}' http://localhost:8000/api/forms/5554
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            # print(access_token['user_id']) // realy return user!
            user = User.objects.get(pk=access_token['user_id'])
            form = created_forms(id = id, owner=user, title=data['title'], content=data['content'])
            form.save()
            print("post!")

        elif request.method == "PUT":
            #curl --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1ODI5MjI5LCJpYXQiOjE3NDU4Mjc0MjksImp0aSI6IjMzM2FjODQ1YjMzMzRlMzJhMmFiMDAxNjMxYjU3ZjkwIiwidXNlcl9pZCI6MX0.v822Z5kGunt5G2pzwR7eg4_2VYMGberJraSyozLphiA' -d '{"title": "a44444dmin", "content": "admi44444n"}' http://localhost:8000/api/forms/5554
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            user = User.objects.get(pk=access_token['user_id'])
            form = created_forms(id = id, owner=user, title=data['title'], content=data['content'])
            form.save()
            print("edit post!")
        
        elif request.method == "DELETE":
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            if access_token['user_id'] == created_forms.objects.filter(id=id).values()[0]['owner_id']:
                created_forms.objects.filter(id=id).delete()
            return Response(status=200)

        return Response(data, status=200)
    except created_forms.DoesNotExist:
        return Response("NotFound 404", status=404)

@api_view(["GET", "POST", "PUT","DELETE"])
def answers(request, id):
    """ /api/answer/id function """
    try:
        if request.method == "GET":
            model_data = complited_forms.objects.get(pk=id)
            data={}
            if model_data:
                data = FormsSerializer(model_data).data

        elif request.method == "POST":
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            # print(access_token['user_id']) // realy return user!
            user = User.objects.get(pk=access_token['user_id'])
            form = complited_forms(id = id, respondent=user, answer=data['answer'])
            form.save()
            print("post!")

        elif request.method == "PUT":
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            # print(access_token['user_id']) // realy return user!
            user = User.objects.get(pk=access_token['user_id'])
            form = complited_forms(id = id, respondent=user, answer=data['answer'])
            form.save()
            print("edit post!")
        
        elif request.method == "DELETE":
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            if access_token['user_id'] == complited_forms.objects.filter(id=id).values()[0]['owner_id']:
                complited_forms.objects.filter(id=id).delete()
            return Response(status=200)

        return Response(data, status=200)
    except complited_forms.DoesNotExist:
        return Response("NotFound 404", status=404)


@api_view(["POST",])
def users_create(request):

    """ /api/users/create function """

    data = json.loads(request.body)
    User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
    return Response(status=201) # 201 - created

@api_view(["GET",])
def user_get_all(request):
    """users/get_all"""
    data = json.loads(request.body)
    token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
    access_token = AccessToken(token_str)
    res=created_forms.objects.filter(owner_id=access_token['user_id']).values()[:]
    return Response(res)