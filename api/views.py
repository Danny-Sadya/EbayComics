import json
from django.shortcuts import render
from rest_framework.views import APIView
from .gocollect_data_scraper import get_title_values_and_grades_img
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages


class GenerateGoCollectDataView(APIView):
    def get(self, request, *args, **kwargs):
        url = request.query_params.get('link', None)
        title, values_and_grades, img = get_title_values_and_grades_img(url)
        if title and values_and_grades and img:
            response = {'status': 'ok',
                        'title': title,
                        'values_and_grades': values_and_grades,
                        'img': img,
                        }
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        elif title and not values_and_grades:
            messages.error(request, "Gocollect is not providing enough data for this comics, you can’t add this right now")
        elif not title and not values_and_grades:
            messages.error(request, "You have entered incorrect link")
        return Response(status=status.HTTP_404_NOT_FOUND)