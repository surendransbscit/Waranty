from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import *
from knox.models import AuthToken
from rest_framework.pagination import PageNumberPagination
from .models import details
from .serializers import DetailsSerializer
from .pagination import CustomPagination

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                _, token = AuthToken.objects.create(user)
                return Response({
                    "status":"True",
                    "message": "Login successful.",
                    "token": token,
                }, status=status.HTTP_200_OK)
            return Response({"Status":"False","error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class DetailsView(APIView):
    # GET method to retrieve paginated details
    def get(self, request):
        all_details = details.objects.all().order_by('id')  
        paginator = CustomPagination()
        paginated_details = paginator.paginate_queryset(all_details, request)
        serializer = DetailsSerializer(paginated_details, many=True)

        # Modify response structure
        paginated_response = paginator.get_paginated_response(serializer.data).data
        response_data = {
            "count": paginated_response["count"],
            "next": paginated_response["next"],
            "previous": paginated_response["previous"],
            "status": "True",
            "Message": "Success",
            "data": paginated_response["results"]
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # POST method to create a new entry
    def post(self, request):
        serializer = DetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"True","Message":"Success","Data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)



class DetailsDeleteView(APIView):
    def delete(self, request, id):
        try:
            detail = details.objects.get(id=id)
            detail.delete()
            return Response(
                {"status":"True","message": f"Record with id {id} deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except details.DoesNotExist:
            return Response(
                {"status":"False","error": f"Record with id {id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class DetailView(APIView):
    def get(self, request, id):
        try:
            detail = details.objects.get(id=id)
            serializer = DetailsSerializer(detail)
            return Response({"Status":"True","Message":"success","Data":serializer.data}, status=status.HTTP_200_OK)
        except details.DoesNotExist:
            return Response(
                {"status":"False","error": f"Record with id {id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )



class InvoiceSearchView(APIView):
    # GET method to search details by invoice
    def get(self, request):
        invoice = request.query_params.get('invoice', None)  
        
        if invoice:
            matching_details = details.objects.filter(invoice__icontains=invoice) 
            if matching_details.exists():
                serializer = DetailsSerializer(matching_details, many=True)
                return Response({"status":"Ture","message":"sucess","data":serializer.data}, status=status.HTTP_200_OK)
            return Response(
                {"status":"False","message": "No records found for the given invoice."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"status":"False","error": "Invoice query parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

