# -*- coding: utf-8 -*-
import csv
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from api import serializers


# check if input member id on login page exists in .csv file
def validate_input_member_id(request):
    try:
        request.data['mem_id']
    except KeyError:
        return Response('Please, input your member id', status=status.HTTP_400_BAD_REQUEST)

    mem_id = request.data['mem_id']

    with open('mem_id.csv') as mem_id_list:
            data = csv.reader(mem_id_list)
            for row in data:
                for fields in row:
                    if str(mem_id) == fields:
                        serializer = serializers.UserSerializer(data=request.data, instance=request.user)
                        if serializer.is_valid():
                            serializer.save(is_auth=True)
                            return Response('You on!', status=status.HTTP_202_ACCEPTED)
                        return Response('Username is required field', status=status.HTTP_400_BAD_REQUEST)
