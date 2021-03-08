from django.http import HttpResponse, HttpResponseBadRequest
from .models import Period, Spending, Transaction
import json
import time

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.exceptions import APIException
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import generics, viewsets, request, status
from django.contrib import messages
from django.db.models import Q
from .serializer import TransactionSerializer
from .models import Period, Transaction


class HomeLandingData(APIView):
    def get(self, request, format=None):
        active_period = Period.objects.filter(completed=0).first()
        if active_period is None:
            data = {
                'status': -1,
                'message': 'Period not found'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        # period_id = active_period['id']
        transaction = Transaction.objects.filter(period=active_period).count()
        data = {
            'period': active_period.period_date,
            'transaction': transaction
        }
        return Response({'message': 'success', 'status': 1, 'data': data})


class TransactionApi(APIView):
    def get(self, request, format=None):
        active_period = Period.objects.filter(completed=0).first()
        if active_period is None:
            data = {
                'status': -1,
                'message': 'Period not found'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        # period_id = active_period['id']
        transaction = Transaction.objects.filter(period=active_period)
        serializer = TransactionSerializer(transaction, many=True)
        response = Response({'data': serializer.data})
        return response
        # data_tmp = []
        # for trans in transaction:
        #     spend_name = trans.spending.name
        #     data_tmp.append(spend_name)

        # data = {
        #     'period': active_period.period_date,
        #     'data_tmp': data_tmp
        # }
        # return Response({'message': 'success', 'status': 1, 'data': data})

    # def post(self, request, format=None):
    #     active_period = Period.objects.filter(completed=0).first()
    #     if active_period is None:
    #         data = {
    #             'status': -1,
    #             'message': 'Event not found'
    #         }
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     active_transaction = Transaction.objects.all()
    #     if active_transaction is None:
    #         data = {
    #             'status': -1,
    #             'message': 'Transactiont not found'
    #         }
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     data_event = TransactionSerializer(active_transaction, many=True)
    #     return Response({'message': 'success', 'status': 1, 'data': data_event.data}, status=status.HTTP_200_OK)

    # def put(self, request, format=None):
    #     json_data = request.read()
    #     requestdata = json.loads(json_data)
    #     active_period = Period.objects.filter(
    #         id=requestdata['period_id']).first()
    #     if active_period is None:
    #         data = {
    #             'status': -1,
    #             'message': 'Active period not found'
    #         }
    #         return response(data, status=status.HTTP_204_NO_CONTENT)
    #     transaction_done = []
    #     for data in requestdata["data"]:
    #         transaction = Transaction.objects.filter(
    #             id=data['orderid'], period=active_period).first()
    #         if transaction is not None:
    #             if 'item' in data:
    #                 transaction.item = str(data["item"])
    #             if 'price' in data:
    #                 transaction.price = int(data["price"])
    #             transaction.update_date = int(time.time())

    #             transaction.save()
    #             transaction_done.append(data['orderid'])
    #     data = {
    #         'status': 1,
    #         'message': 'sucess insert',
    #         'data': transaction_done
    #     }
    #     return Response(data, status=status.HTTP_200_OK)


class TransactionDetailApi(APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise CustomValidation(
                'Transaction not found', 'message', status_code=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        transaction = self.get_object(pk)

        serializer = TransactionSerializer(transaction)
        response = Response({'data': serializer.data})
        return response

    def put(self, request, pk):
        if 'item' not in request.POST:
            raise CustomValidation(
                'Missing atribute item', 'message', status_code=status.HTTP_400_BAD_REQUEST)
        if 'price' not in request.POST:
            raise CustomValidation(
                'Missing atribute price', 'message', status_code=status.HTTP_400_BAD_REQUEST)
        transaction = self.get_object(pk)

        item = request.POST['item']
        price = request.POST['price']
        update_date = int(time.time())
        created_date = int(time.time())

        data = {
            'item': item,
            'price': price,
            'created_date': created_date,
            'update_date': update_date,
        }
        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else:
            self.detail = {'detail': force_text(self.default_detail)}
