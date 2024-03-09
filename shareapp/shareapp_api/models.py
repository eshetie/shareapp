from django.db import models

# Create your models here.
class users(models.Model):
    phone = models.CharField(max_length = 10,primary_key=True)
    firstname=models.CharField(max_length=255,default = False)
    middlename=models.CharField(max_length=255,default = False)
    lastname=models.CharField(max_length=255,default = False)
    role =models.CharField(max_length=255,default = False)
    password = models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    gender=models.CharField(max_length=5)
    dob=models.DateField()
    country=models.CharField(max_length=100)
    national_id=models.CharField(max_length=100)
    subcity=models.CharField(max_length=100)
    woreda=models.CharField(max_length=100)
    houseno=models.CharField(max_length=100)
    occupation=models.CharField(max_length=100)
    
    

    def __str__(self):
        return self.phone
        
        

# Create your models here.
class company(models.Model):
    name = models.CharField(max_length = 255,primary_key=True)
    contact=models.CharField(max_length=255,default = False)
    email=models.CharField(max_length=255,default = False)
    description=models.CharField(max_length=255,default = False)
    logo =models.CharField(max_length=255,default = False)
    reg_date =models.DateField()
    category=models.CharField(max_length=100)
    owner=models.ForeignKey(users, related_name="owner_company", on_delete=models.CASCADE)
    
    

    def __str__(self):
        return self.name
        
        

# Create your models here.
class share(models.Model):
    stat = ((0, 'closed'),    (1, 'open'),)
    sid = models.CharField(max_length = 255,primary_key=True)
    company=models.ForeignKey(company, related_name="company_name", on_delete=models.CASCADE)
    price=models.FloatField()
    minimum=models.IntegerField(default=0)
    maximum=models.IntegerField(default=0)
    issued_date =models.DateTimeField()
    completed =models.IntegerField()
    description=models.CharField(max_length=1000)
    status=models.CharField(max_length=1, choices=stat)
    
    

    def __str__(self):
        return self.sid
        
        
# Create your models here.
class purchase(models.Model):
    purchaseid = models.CharField(max_length = 255,primary_key=True)
    shareid = models.ForeignKey(share, related_name="shareid", on_delete=models.CASCADE)
    owner=models.ForeignKey(users, related_name="user_phone", on_delete=models.CASCADE)
    #owner=models.CharField(max_length = 255)
    quantity=models.IntegerField(default=1)
    price=models.FloatField()
    purchased_on =models.DateTimeField()
    planned_date =models.DateTimeField()
    
    

    def __str__(self):
        return self.pid
        
        
class bill(models.Model):
    bid = models.CharField(max_length = 255,primary_key=True)
    purchaseid = models.ForeignKey(purchase, related_name="pid", on_delete=models.CASCADE)
    amount=models.FloatField()
    outstanding=models.FloatField()
    bill_date =models.DateTimeField()
    
    

    def __str__(self):
        return self.bid
        
        
