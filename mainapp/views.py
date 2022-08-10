from django.shortcuts import render,redirect
import random
from django.contrib import messages
from users.models import  Mail
from .models import RandUser,Trade,Plan,Deposit
from django.utils import timezone
from users.models import Account
from users import functions
from django.db.models import Sum

from datetime import datetime,timedelta,date
# Create your views here.


def my_custom_error_view(request):
    return render(request,'500.html')

def page_not_found_view(request):
    return render(request,'404.html')
    
def page_restricted_view(request):
    return render(request,'403.html')

    
def home(request):
    # past_trade =Trade.objects.filter(profited = True) 
    # for i in past_trade:
    #     if i.count <30 and i.user.account.main >i.deposit.plan.min:
    #         this,that = functions.get_date()
    #         newtrade = Trade.objects.create(
    #                 user =i.user,
    #                 amount = i.amount,
    #                 deposit = Deposit.objects.get(id = i.deposit.id),
    #                 profit = functions.get_percentage(i.deposit.amount,i.deposit.plan.percentage_return),
    #                 time_now =this,
    #                 due_time = that,
    #                 count = i.count +1 
    #             )
    #         newtrade.save()
    trade = Trade.objects.filter(profited = False)
    time = timezone.now()
    for item in trade:
        if time >= item.due_time:
            item.profited = True
            #item.count += 1
            account,created = Account.objects.get_or_create(user = item.user)
            account.balance = account.balance + item.profit
            account.save()
            item.save()
            now,due = functions.get_date()
            if account.main > item.deposit.plan.min:
                new_trade = Trade.objects.create(
                    user =item.user,
                    amount = item.amount,
                    deposit = Deposit.objects.get(id = item.deposit.id),
                    profit = functions.get_percentage(item.deposit.amount,item.deposit.plan.percentage_return),
                    time_now =now,
                    due_time = due,
                    count = item.count +1 
                )
                new_trade.save()

    if request.method =='POST':
        obj = Mail(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            subject = request.POST['subject'],
            message = request.POST['message'],   
            )
        obj.save()
        messages.success(request,'Mail Sent!')
        return redirect ('/')


        
    return render(request,'mainapp/index.html')


def news(request):
    return render(request,'mainapp/news.html')

def terms(request):
    return render(request,'mainapp/terms.html')

def testimonial(request):
    return render(request,'mainapp/testimonial.html')
    
def plans(request):
    return render(request,'mainapp/plans.html')

