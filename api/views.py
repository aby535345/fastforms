from forms.models import created_forms, complited_forms
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User #dont create own user table!
from forms.serializers import FormsSerializer, AnswerSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import AccessToken

import json

# main api code here!

@api_view(["GET"])
def forms_get(request, id):
    try:
        model_data = created_forms.objects.get(pk=id)
        data={"Error!":"not found"}
        if model_data:
            data = FormsSerializer(model_data).data
        return Response(data, status=200)
    except:
        return Response(status=500)

@api_view(["POST"])
def forms_post(request):
        try:
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            # print(access_token['user_id']) // realy return user!
            user = User.objects.get(pk=access_token['user_id'])
            form = created_forms(owner=user, title=data['title'], content=data['content'])
            form.save()
            print("post!")
            return Response("success!", status=201)
        except:
            return Response(status=500)

@api_view(["PUT"])
def forms_edit(request, id):
        try:
            data = json.loads(request.body)
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            user = User.objects.get(pk=access_token['user_id'])
    
            if access_token['user_id'] == created_forms.objects.filter(id=id).values()[0]['owner_id']:
                form = created_forms(id = id, owner=user, title=data['title'], content=data['content'])
                form.save()
            print("edit post!")
            return Response("success",status=201)
        except:
            return Response(status=500)

@api_view(["DELETE"])
def forms_delete(request, id):
        try:
            token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
            access_token = AccessToken(token_str)
            if access_token['user_id'] == created_forms.objects.filter(id=id).values()[0]['owner_id']:
                created_forms.objects.filter(id=id).delete()
            return Response("success",status=200)
        except:
            return Response(status=500)




@api_view(["GET"])
def answers_get(request, id):
    model_data = complited_forms.objects.filter(form=id).values()
    #data={"Error!":"not found"}
    #awful django model add _id to my fields :(
    #if model_data:
     #   print(model_data)
     #   for i in model_data:
     #       data = AnswerSerializer(model_data[:]).data
     #   print(data)
    return Response(model_data, status=200)

@api_view(["POST"])
def answers_post(request, id):
    data = json.loads(request.body)
    token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
    access_token = AccessToken(token_str)
    user = User.objects.get(pk=access_token['user_id'])
    answer = complited_forms(form=created_forms.objects.get(pk=id), respondent=user, answer=data["answer"])
    answer.save()
    print("post!")
    return Response("success!", status=201)

@api_view(["PUT"])
def answers_edit(request,id,answer_id):
    data = json.loads(request.body)
    token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
    access_token = AccessToken(token_str)
    user = User.objects.get(pk=access_token['user_id'])
    if access_token['user_id'] == created_forms.objects.filter(id=id).values()[0]['owner_id']:
        answer = complited_forms(id=answer_id, form=created_forms.objects.get(pk=id), respondent=user, answer=data['answer'])
        answer.save()
        print("edit answer!")
    return Response("success!", status=201)

@api_view(["DELETE"])
def answers_delete(request, id, answer_id):
    token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
    access_token = AccessToken(token_str)
    if access_token['user_id'] == complited_forms.objects.filter(id=answer_id).values()[0]['respondent_id']:
        complited_forms.objects.filter(id=answer_id).delete()
        return Response("success",status=200)
    else:
        return Response(status=403)




@api_view(["POST"])
def users_create(request):
    try:
        data = json.loads(request.body)
        User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return Response(status=201) # 201 - created
    except:
        return Response(status=500)

@api_view(["GET"])
def user_get_all(request):
    token_str = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ","")
    access_token = AccessToken(token_str)
    res=created_forms.objects.filter(owner_id=access_token['user_id']).values()[:]
    return Response(res)

@api_view(["GET"])
def about(request):
    api_content=""" 
    (POST) /api/token and /api/token/refresh:
        get JWT tokens.
    curl command:
        curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/token/

     
    (GET) /api/forms/get/<id>:
        get form by id.
    curl command:
        curl -X GET http://localhost:8000/api/forms/get/1

    (POST) /api/forms/create:
        create form.
    headers:
        Authorization: Bearer <access_token>
    body:
        {"title":"form title","content":"description of checkbox radio etc"}
    curl:
        curl -X POST --header 'Authorization: Bearer <access_token>' -d '{"title": "a44444dmin", "content": "admi44444n"}' http://localhost:8000/api/forms/create/1
    
    (PUT) /api/forms/edit/<id>:
        edit (overwrite) form 
    headers:
        Authorization: Bearer <access_token>
    body:
        {"title":"form title","content":"description of checkbox radio etc"}
    curl:
        curl -X PUT --header 'Authorization: Bearer <access_token>' -d '{"title": "a44444dmin", "content": "admi44444n"}' http://localhost:8000/api/forms/edit/1
    
    (DELETE) /api/forms/delete/<id>:
        delete form
    headers:
        Authorization: Bearer <access_token>
    curl:
        curl -X PUT --header 'Authorization: Bearer <access_token>' http://localhost:8000/api/forms/delete/1
    
    (POST) /api/users/create:
        create new user
    body:
        {"username":"user", "email":"mail", "password":"qwerty"}
    curl:
   
    
    (GET) /api/answers/get/<id>:
        get answer by form id.
    curl command:
        curl -X GET http://localhost:8000/api/answers/get/1

    (POST) /api/answers/create/<id>:
        create answer on form.
    headers:
        Authorization: Bearer <access_token>
    body:
        {"answer":"description of checkbox radio etc"}
    curl:
        curl -X POST --header 'Authorization: Bearer <access_token>' -d '{"answer": "admi44444n"}' http://localhost:8000/api/answers/create/1
    
    (PUT) /api/forms/edit/<id>:
        edit (overwrite) form 
    headers:
        Authorization: Bearer <access_token>
    body:
        {"title":"form title","content":"description of checkbox radio etc"}
    curl:
        curl -X PUT --header 'Authorization: Bearer <access_token>' -d '{"answer": "admi44444n"}' http://localhost:8000/api/answers/edit/1
    
    (DELETE) /api/forms/delete/<id>:
        delete form
    headers:
        Authorization: Bearer <access_token>
    curl:
        curl -X PUT --header 'Authorization: Bearer <access_token>' http://localhost:8000/api/answers/delete/1
    

    (GET) /api/users/get_all:
        get all user forms 
    headers:
        Authorization: Bearer <access_token>
    curl:
        curl -X PUT --header 'Authorization: Bearer <access_token>' http://localhost:8000/api/users/get_all
   
    """
    return Response(api_content, headers={"Content-type": "text/plain; charset=us-ascii"} ,status=200)
