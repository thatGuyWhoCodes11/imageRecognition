import json
from django.http import JsonResponse
from django.shortcuts import render
from facedb import FaceDB
import base64
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from PIL import Image
from datetime import datetime
@csrf_exempt 
def addFaces(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        image = body['image']
        id = body['id']
        decodedImage = Image.open(BytesIO(base64.b64decode(image)))
        db = FaceDB(path="../encodedDB")
        name = str(datetime.now())
        try:
            db.add(img=decodedImage,id=id,name=name)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"face not saved","isSaved":"false"})
        return JsonResponse({"message":"face saved!","isSaved":"true"})
    else:
        return JsonResponse({'error': 'Invalid request method'})
@csrf_exempt
def recognizeFaces(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        db = FaceDB(path="../encodedDB")
        image=body['image']
        decodedImage=Image.open(BytesIO(base64.b64decode(image)))
        result = db.recognize(img=decodedImage,include="name")
        return JsonResponse({'results':result})