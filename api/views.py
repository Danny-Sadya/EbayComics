import json
from django.shortcuts import render
from rest_framework.views import APIView
from .gocollect_data_scraper import get_title_values_and_grades_img
from rest_framework.response import Response
from rest_framework import status


class GenerateGoCollectDataView(APIView):
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('link', None)
        title, values_and_grades, img = get_title_values_and_grades_img(url)
        if title and values_and_grades and img:
            response = {'title': title,
                        'values_and_grades': values_and_grades,
                        'img': img,
                        }
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
