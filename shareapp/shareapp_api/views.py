from django.shortcuts import render
import jwt
from django.conf import settings
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db import connection
from .models import users,company,purchase,share,bill
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Subquery, OuterRef
from .serializers import UsersSerializer,CompanySerializer,PurchaseSerializer,ShareSerializer,BillSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.timezone import localtime
import hashlib
from dateutil.relativedelta import relativedelta
from datetime import date

from django.utils import timezone
from datetime import datetime, timedelta





class ShareDetail():
    def getShareDetail(company):
        todos = share.objects.get(company=company)
        serializer = ShareSerializer(todos)
        return serializer


def md5calc(str):
    md5_hash = hashlib.md5()
    string_bytes = str.encode('utf-8')
    md5_hash.update(string_bytes)
    res = md5_hash.hexdigest()
    return res

class UsersLoginView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
             usrs=users.objects.get(phone=request.data.get('phone'),password=request.data.get('password'))
             serializer = UsersSerializer(usrs)
             payload = {'user_id': usrs.firstname,'phone': usrs.phone,}
             token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
             data = serializer.data
             data['token'] = token
             return Response(data, status=status.HTTP_200_OK)
        except users.DoesNotExist:
             return Response({"login": "Object with user phone does not exists."},status=status.HTTP_400_BAD_REQUEST)
        

class UsersListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    @csrf_exempt
 #   def get(self, request, *args, **kwargs):
   
  #      todos = users.objects.filter(phone = "0915998916")
   #     serializer = UsersSerializer(todos)
    #    return Response(serializer.phone, status=status.HTTP_200_OK)



    # 2. Create
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        '''
        Create the users with given todo data
        '''
        data = {
            'phone': request.data.get('phone'), 
            'firstname': request.data.get('firstname'), 
            'middlename': request.data.get('middlename'), 
            'lastname': request.data.get('lastname'), 
            'password': request.data.get('password'), 
            'gender': request.data.get('gender'), 
            'dob': request.data.get('dob'), 
            'city': request.data.get('city'), 
            'country': request.data.get('country'), 
            'subcity': request.data.get('subcity'), 
            'woreda': request.data.get('woreda'),
            'houseno': request.data.get('houseno'),
            'national_id': request.data.get('national_id'),
            'occupation': request.data.get('occupation'),
            'role': request.data.get('role')
        }
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class UsersDetailApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self, phone):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return users.objects.get(phone=phone)
        except users.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, phone, *args, **kwargs):
        todo_instance = self.get_object(phone)
        print(todo_instance)
        if not todo_instance:
            return Response(
                {"res": "Object with user phone does not exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UsersSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, phone, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        print(request.data)
        todo_instance = self.get_object( request.data.get('phone'))
        if not todo_instance:
            return Response(
                {"res": "Object with users id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'phone': request.data.get('phone'), 
            'firstname': request.data.get('firstname'), 
            'middlename': request.data.get('middlename'), 
            'lastname': request.data.get('lastname'), 
            'gender': request.data.get('gender'), 
            'dob': request.data.get('dob'), 
            'city': request.data.get('city'), 
            'country': request.data.get('country'), 
            'subcity': request.data.get('subcity'), 
            'woreda': request.data.get('woreda'),
            'houseno': request.data.get('houseno'),
            'national_id': request.data.get('national_id'),
            'occupation': request.data.get('occupation'),
            'role': request.data.get('role')
        }
        serializer = UsersSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"res":"done"}, status=status.HTTP_200_OK)
        return Response({"res":"Phone is not found."}, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, phone, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(phone, request.users.phone)
        if not todo_instance:
            return Response(
                {"res": "Object with users id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
        


      
class AllCompanyListView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]
    # 3. Retrieve
    def get(self, request, *args, **kwargs):
        try:         
             comp = company.objects.all()
             serializer = CompanySerializer(comp, many=True)
             return Response(serializer.data, status=status.HTTP_200_OK)
        except company.DoesNotExist:
            return  Response({"res": "No company"},status=status.HTTP_400_BAD_REQUEST)
            


class SearchCompanyListView(APIView):
    def get(self, request,name, *args, **kwargs):
        try: 
             if name!=None:
                  comp = company.objects.filter(name__icontains=name)
                  serializer = CompanySerializer(comp, many=True)
                  return Response(serializer.data, status=status.HTTP_200_OK)
             else:
                  return Response({"res": "Enter a keyword"}, status=status.HTTP_200_OK)
        except company.DoesNotExist:
            return  Response({"res": "No company"},status=status.HTTP_400_BAD_REQUEST)


class AllsharesunderCompany(APIView):
    def get(self, request,companyname, *args, **kwargs):
        try:
            print(companyname)
            sh = share.objects.get(company_id=companyname)
            serializer = ShareSerializer(sh)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except share.DoesNotExist:
            return  Response({"res": "No company"},status=status.HTTP_400_BAD_REQUEST)
      


class ShareDetailView(APIView):      
    #permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        sid=request.data.get('sharename')
        data = {'sid': sid, 'price': request.data.get('price'), 
            'minimum': request.data.get('minimum'), 'maximum': request.data.get('maximum'),
            'issued_date': request.data.get('issued_date'), 'completed': request.data.get('completed'), 'description': request.data.get('description'), 'status': request.data.get('status'), 'company': request.data.get('company')}
        serializer = ShareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class purchaseDetail(APIView):
    #permission_classes = [permissions.IsAuthenticated]
            
    def post(self, request,  *args, **kwargs):
        try:
             purchased_on=localtime().date()
             planned_date=request.data.get('planned_date')
             shd=ShareDetail.getShareDetail(request.data.get('company'))
             quantity=request.data.get('quantity')
             if quantity=="":
                  quantity=shd.data.get('minimum')     
             price=shd.data.get('price')*int(quantity)
             print(request.data)
             purchaseid=md5calc(str(request.data.get('owner_id'))+''+str(shd.data.get('sid')))      
             print(shd.data.get('sid'))
             print(shd.data)
             if planned_date=="":
                  date_string = shd.data.get('issued_date')
                  years_to_add = shd.data.get('completed')                  
                  date_val = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
                  result_date = date_val + relativedelta(years=years_to_add)
                  result_date_string = result_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                  planned_date=result_date_string                      
             today = date.today()
             if planned_date == today:
                  price=shd.data.get('price')*int(quantity)
             print("sometimes: "+str(planned_date))
             u=purchase.objects.create(purchaseid=purchaseid,price=price, purchased_on=purchased_on,quantity=quantity, planned_date=planned_date, owner_id=request.data.get('owner_id'), shareid_id=shd.data.get('sid'))
             u.save()
             return Response(purchaseid, status=status.HTTP_200_OK)
        except Exception as e :
            return  Response({"res": "On purchase: "+str(e)},status=status.HTTP_400_BAD_REQUEST)
            
            
    def get(self,request,phone,*args, **kwargs):
        try:
            purchase_ids_in_bill = bill.objects.values('purchaseid')
            purchased_rows = purchase.objects.filter(owner_id=phone).exclude(purchaseid__in=Subquery(purchase_ids_in_bill))
            serializer = PurchaseSerializer(purchased_rows,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except purchase.DoesNotExist:
            return  Response({"res": "your cart is empty"},status=status.HTTP_400_BAD_REQUEST)
            

            
class SaveBillFromCartView(APIView):
    def getPurchases(self,purchaseid):
        try:
            purchased_rows = purchase.objects.filter(purchaseid=purchaseid)
            serializer = PurchaseSerializer(purchased_rows,many=True)
            return serializer.data
        except purchase.DoesNotExist:
            return  {"res": "your cart is empty"}
            
    def getPrivousPaidAmount(self,purchaseid):
        try:
            with connection.cursor() as cursor:
                sql="SELECT p.purchaseid, SUM(b.amount) AS total_amount FROM public.shareapp_api_purchase p INNER JOIN public.shareapp_api_bill b ON p.purchaseid = b.purchaseid_id and b.purchaseid_id='"+purchaseid+"' GROUP BY p.purchaseid;"
                cursor.execute(sql)
                rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            return data
        except bill.DoesNotExist:
            return  {"res": "No bill"}
            
            
    def getShareDetail(self,sid):
        try:
            shrows = share.objects.filter(sid=sid)
            serializer = ShareSerializer(shrows,many=True)
            return serializer.data
        except share.DoesNotExist:
            return  {"res": "your cart is empty"}
    def post(self, request):           
        print(request.data)    
        counter=int(request.data.get('itemCount'))
        msg=""
        st=""
        if(counter==1):
            pdata=self.getPurchases(request.data.get('purchaseIds')[0])
            prevamount=self.getPrivousPaidAmount(request.data.get('purchaseIds')[0])
            print(prevamount[0])
            print("***"+str(request.data.get('purchaseIds')[0]))
            current_time = datetime.now()
            current_datetime =  current_time.strftime("%Y-%m-%d %H:%M")
            share=self.getShareDetail(pdata[0]['shareid'])
            bid=md5calc(str(pdata[0]['purchaseid'])+""+str(current_datetime))
            if (request.data.get('amount'))=="":
                 amt=pdata[0]['quantity']*share[0]['price']
            else:
                 amt=request.data.get('amount')
            outstanding=float(pdata[0]['price'])-(float(prevamount[0]['total_amount'])+float(amt))
            if(outstanding<0):
                  msg= {'message': 'Price is over. Your expected price is '+str(outstanding)}
                  st=status.HTTP_200_OK
                  return Response(msg,status=st)
            ds={'bid': bid, 'purchaseid': pdata[0]['purchaseid'], 'amount': amt, 'outstanding': outstanding, 'bill_date': current_datetime}
            print(ds)
            serializer = BillSerializer(data=ds)
            if serializer.is_valid():
                  serializer.save()
                  msg= {'message': 'Bill saved successfully.'}
                  st=status.HTTP_200_OK
            else:
                  msg =serializer.errors
                  st=status.HTTP_400_BAD_REQUEST  
        else:
            for cnt in range(0,counter):
                 pdata=self.getPurchases(request.data.get('purchaseIds')[cnt])
                 prevamount=self.getPrivousPaidAmount(request.data.get('purchaseIds')[cnt])
                 print("***"+str(request.data.get('purchaseIds')[cnt]))
                 current_time = datetime.now()
                 current_datetime =  current_time.strftime("%Y-%m-%d %H:%M")
                 share=self.getShareDetail(pdata[0]['shareid'])
                 bid=md5calc(str(pdata[0]['purchaseid'])+""+str(current_datetime))
                 amt=pdata[0]['quantity']*share[0]['price']
                 outstanding=float(pdata[0]['price'])-(float(prevamount[0]['total_amount'])+float(amt))
                 if(outstanding<0):
                       msg= {'message': 'Price is over. Your expected price is '+str(outstanding)}
                       st=status.HTTP_200_OK
                       return Response(msg,status=st)
                 ds={'bid': bid, 'purchaseid': pdata[0]['purchaseid'], 'amount': amt, 'outstanding': outstanding, 'bill_date': current_datetime}
                 print(ds)
                 serializer = BillSerializer(data=ds)
                 if serializer.is_valid():
                     serializer.save()
                     msg= {'message': 'Bill saved successfully.'}
                     st=status.HTTP_200_OK
                 else:
                     msg =serializer.errors
                     st=status.HTTP_400_BAD_REQUEST             
        return Response(msg,status=st)
        
        
        
class GetBillHistoryView(APIView):
            
            
    def get_bills(pid):
        try:
            pdetail=bill.objects.filter(purchaseid_id=pid)
            bserializer = BillSerializer(pdetail)
            return Response(query, status=status.HTTP_200_OK)
        except purchase.DoesNotExist:
            return  Response({"res": "No history"},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,phone,*args, **kwargs):
        try:
            data={}
            with connection.cursor() as cursor:
                sql="SELECT distinct(bid), amount, outstanding, bill_date, p.purchaseid, price, purchased_on, planned_date, owner_id, shareid_id, quantity FROM public.shareapp_api_bill s, public.shareapp_api_purchase p where s.purchaseid_id=p.purchaseid and owner_id='"+phone+"';"
                cursor.execute(sql)
                rows = cursor.fetchall()
            return Response(rows, status=status.HTTP_200_OK)
        except purchase.DoesNotExist:
            return  Response({"res": "No history"},status=status.HTTP_400_BAD_REQUEST)
            
            
                    
class GetOutstandingDetails(APIView):
        
    def get(self,request,phone,*args, **kwargs):
        try:
            data={}
            with connection.cursor() as cursor:
                sql="SELECT p.purchaseid, p.price, p.purchased_on, p.planned_date, p.owner_id, p.shareid_id, p.quantity, SUM(b.amount) AS total_amount FROM public.shareapp_api_purchase p INNER JOIN public.shareapp_api_bill b ON p.purchaseid = b.purchaseid_id and owner_id='"+phone+"' and b.outstanding!=0 GROUP BY p.purchaseid, p.price, p.purchased_on, p.planned_date, p.owner_id, p.shareid_id, p.quantity;"
                cursor.execute(sql)
                rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            data = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                amt = row_dict['total_amount']
                price = row_dict['price']
                outstanding = float(price)-float(amt)
                row_dict['outstanding'] = outstanding
                data.append(row_dict)
            return Response(data, status=status.HTTP_200_OK)
        except purchase.DoesNotExist:
            return  Response({"res": "No history"},status=status.HTTP_400_BAD_REQUEST)     
            
class GetCompletedDetails(APIView):
        
    def get(self,request,phone,*args, **kwargs):
        try:
            data={}
            with connection.cursor() as cursor:
                sql="SELECT p.purchaseid, p.price, p.purchased_on, p.planned_date, p.owner_id, p.shareid_id, p.quantity, SUM(b.amount) AS total_amount FROM public.shareapp_api_purchase p INNER JOIN public.shareapp_api_bill b ON p.purchaseid = b.purchaseid_id and owner_id='"+phone+"' and b.outstanding=0 GROUP BY p.purchaseid, p.price, p.purchased_on, p.planned_date, p.owner_id, p.shareid_id, p.quantity;"
                cursor.execute(sql)
                rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            return Response(data, status=status.HTTP_200_OK)
        except purchase.DoesNotExist:
            return  Response({"res": "No history"},status=status.HTTP_400_BAD_REQUEST)