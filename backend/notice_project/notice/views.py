from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import CreateNoticeSerializer, CommentReactionSerializer,EditNoticeSerializer
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests


# Create your views here.

notices = [
    {
        'id': 1,
        'title': "Test",
        'text': "Basis test", 
        'photo_url': "cdn.zuri.chat",
        'video_url':"cdn2.zuri.chat",
        'audio_url':"cdn3.zuri.chat",
    },
    {
        'id': 2,
        'title': "Test2",
        'text': "Basis test", 
        'photo_url': "cdn.zuri.chat",
        'video_url':"cdn2.zuri.chat",
        'audio_url':"cdn3.zuri.chat",
    }
]

class AllNoticesView(views.APIView):

    """GET request to display/retrieve all existing notices"""
    def get(self, request):
        data= [
        {"title":"Management meeting",
        "text":"Management has updated the design scedule",
        "photo_url":"null",
        "video_url":"null",
        "audio_url":"null"},

        {"title":"Stage 5",
        "text":"Complete a ticket to move to stage 5",
        "photo_url":"null",
        "video_url":"null",
        "audio_url":"null",
        "published":"True"},

        {"title":"Individual work",
        "text":"Each intern is expected to complete at least one ticket individually",
        "photo_url":"null",
        "video_url":"null",
        "audio_url":"null"},
        ]
        
        results = CreateNoticeSerializer(data, many=True).data
        return Response(results, status=status.HTTP_200_OK)


class CreateNoticeView(views.APIView):

    def post(self, request):
        serializer = CreateNoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            payload={
                    "plugin_id": "612a3a914acf115e685df8e3",
                    "organization_id": "id",
                    "collection_name": "mycollection",
                    "bulk_write": False,
                    "object_id": "1212",
                    "filter": {},
                    "payload": serializer.data
                    }
            external_api_url = 'https://zccore.herokuapp.com/data/write'
            
            res = requests.post(external_api_url, payload)
            return Response({"post_data":payload, "server_response":res.json()}, status=status.HTTP_201_CREATED)


           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CommentReactionAPIView(views.APIView):

    def put(self, request):
        serializer = CommentReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Your have successfully updated your reaction"
            })
        return Response({
                "success": False,
                "data": serializer.data,
                "message": "Your reaction could not be updated"
            })


    def patch(self, request):
        serializer = CommentReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Your have successfully updated your reaction"
            })
        return Response({
                "success": False,
                "data": serializer.data,
                "message": "Your reaction could not be updated"
            })

def delete(request):
    data = {"message": "Your comment has been successfully deleted."}
    return JsonResponse(data, status=200)

def deleteNotice(request):
    Message = {"output":"Your notice has been successfully deleted."}

    return JsonResponse(Message, status=200)


@api_view(['PUT'])
def update_notice(request, notice_id):
    notice = None
    for tk in notices:
        if(tk['id'] == notice_id):
            notice = tk
    if(notice != None): 
        if(request.method == 'PUT'):
            serialiser = EditNoticeSerializer(notice, data=request.data)
            if(serialiser.is_valid()):
                notices.remove(notice)
                notices.append(request.data)
            return Response(request.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Notice not found'}, status=status.HTTP_404_NOT_FOUND)
            })
