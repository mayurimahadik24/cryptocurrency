# scraper/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CryptoRequestSerializer
from .tasks import fetch_crypto_data
from celery.result import AsyncResult

# @app_view(['GET','POST']) # type: ignore
class StartScrapingView(APIView):
    def post(self, request, GET, **kwargs):
        serializer = CryptoRequestSerializer(data=request.data)
        if serializer.is_valid():
            crypto_list = serializer.validated_data['cryptos']
            task = fetch_crypto_data.delay(crypto_list)
            return Response({'job_id': task.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        task_result = AsyncResult(job_id)
        if task_result.state == 'PENDING':
            response = {
                'job_id': job_id,
                'state': task_result.state,
                'status': 'Pending...'
            }
        elif task_result.state != 'FAILURE':
            response = {
                'job_id': job_id,
                'state': task_result.state,
                'result': task_result.result
            }
        else:
            response = {
                'job_id': job_id,
                'state': task_result.state,
                'status': str(task_result.info)
            }
        return Response(response)
