from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from .models import users,company,purchase,share,bill
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ["phone","firstname","middlename","lastname","role","password","city","gender","dob","country","national_id","subcity","woreda","houseno","occupation"]
        
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'
        
        
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchase
        fields = '__all__'      
        
        
class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = share
        fields = '__all__'
        
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill
        fields = '__all__'
        