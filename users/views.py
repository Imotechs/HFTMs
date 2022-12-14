import json
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views import View
from mainapp.models import Plan, Trade,Deposit, UserPayEvidence
from users.forms import UserRegistrationForm
from users.models import Account, Mail, Profile, Withdrowal
from . import functions
from django.db.models import Sum

# Create your views here.

def register(request,*args,**kwargs):
    if request.method =="POST":
        
        if User.objects.filter(email = request.POST['email']):
            context = {
                'msg':{"Email":" Email already registered!"},
                'ref':kwargs.get('ref')
            }
            return render(request,'mainapp/signup.html',context)
        else:
            form = UserRegistrationForm(request.POST)
                # username = request.POST.get('username'),
                # email = request.POST.get('email'),
                # password1 = request.POST.get('password1'),
                # password2 = request.POST.get('password2'),                      
            if form.is_valid():
                referrer = request.POST.get('ref'),
                if referrer[0] != '':
                    try:
                        ref_user = Profile.objects.get(uid = referrer[0])
                        user_obj = form.save()
                        obj = Profile(
                        user = User.objects.get(id = user_obj.id), 
                        uid = functions.get_user_id(),
                        country = request.POST.get('country'),
                        referrer = ref_user.uid,
                        referred = True,
                        )
                        obj.save()
                        return redirect('login')

                    except Exception as err:
                        print('error:',err)
                        context = {
                            'msg':{'Referral':'Invalid Referral Code!'},
                            'ref':kwargs.get('ref')
                                }
                        return render(request,'mainapp/signup.html',context)
                else:
                    user_obj = form.save()
                    obj = Profile(
                    user = User.objects.get(id = user_obj.id), 
                    uid = functions.get_user_id(),
                    country = request.POST.get('country'),
                    )
                    obj.save()
                    messages.success(request,'Your account was created')
                    return redirect("login")
            else:
                context = {
                    'msg':form.errors,
                    'ref':kwargs.get('ref')
                        }
                return render(request,'mainapp/signup.html',context)
    try:
        context = {
            'ref':kwargs.get('ref')
        }
        return render(request,'mainapp/signup.html',context)
    except:
         return render(request,'mainapp/signup.html')


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return redirect('profile')
            else:
                msg = 'User records have issues, contact Admin!'
                return render(request,'mainapp/signin.html', {'msg':msg})
        elif user is None:
            context = {'msg':{'Notice':'Error in Login Credentials!'}}
                
            return render(request,'mainapp/signin.html', context)
        
    return render(request,'mainapp/signin.html')

@login_required
def profile(request):  
    try:
        trade  = Trade.objects.filter(user = request.user,profited = False).last()
        deposit = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        withdrow = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        account = Account.objects.get_or_create(user = request.user)
        profile = Profile.objects.get(user = User.objects.get(id = request.user.id))
        context = {
            'withdrow':withdrow,
            'deposit':deposit,
            'profile':profile,
            'account':account,
            'trade':trade,
        }
        return render(request,'users/index.html',context)

    except Exception as err:
        print('error:',err)
        deposit = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        withdrow = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        account = Account.objects.get_or_create(user = request.user)

        context = {
            'withdrow':withdrow,
            'deposit':deposit,
            'account':account[0],
        }
        return render(request,'users/index.html',context)
       

def deposit(request):
    wallet = 'xadwqweewtrlwrtretewqrtert'

    if request.method =='POST':
        if float(request.POST['amount']) >9.9:
            try:
                obj = Deposit(
                    user = request.user,
                    amount = request.POST['amount'],
                    plan = Plan.objects.get(id =request.POST['plan']),
                    option = request.POST['method'],
                    date_ = timezone.now(),
                    )

                obj.save()
                messages.success(request,'Make your payment Using the Copied Wallet Address')
                return redirect('profile')
            except Exception as err:
                pass
        else:
            messages.success(request,'Deposit must be aabove 10 USDT')
            return redirect('deposit')

    context = {
        'wallet':wallet,
    }
    return render(request,'users/deposit.html',context)

def depositplans(request):

    return render(request,'users/depositplans.html')

def basic(request):
    min = 10
    max = 500
    if request.method =='POST':
        amount = request.POST['amount']
        print(amount)
        if int(amount) <= max and int(amount) >= min:
            obj = Deposit.objects.create(
                amount = int(amount),
                user = request.user,
                plan = Plan.objects.get(name = 'Basic')
            )
            obj.save()
            return render(request,'users/confirm.html',{'obj':obj})
        else:
            messages.info(request,'Consider the min and max cost for this Plan')
            return redirect('basic')


    context = {
        'min':min,
        'max':max,
    }
    return render(request,'users/amount.html',context)

def regular(request):
    min = 501
    max = 2000
    if request.method =='POST':
        amount = request.POST['amount']
        if int(amount) <= max and int(amount) >= min:
            obj = Deposit.objects.create(
                amount = int(amount),
                user = request.user,
                plan = Plan.objects.get(name = 'Regular')
            )
            obj.save()
            return render(request,'users/confirm.html',{'obj':obj})
        else:
            messages.info(request,'Consider the min and max cost for this Plan')
            return redirect('regular')
    context = {
        'min':min,
        'max':max,
    }
    return render(request,'users/amount.html',context)

def standard(request):
    min = 2001
    max = 5000
    if request.method =='POST':
        amount = request.POST['amount']
        print(amount)
        if int(amount) <= max and int(amount) >= min:
            obj = Deposit.objects.create(
                amount = int(amount),
                user = request.user,
                plan = Plan.objects.get(name = 'Standard')
            )
            obj.save()
            return render(request,'users/confirm.html',{'obj':obj})
        else:
            messages.info(request,'Consider the min and max cost for this Plan')
            return redirect('standard')
    context = {
        'min':min,
        'max':max,
    }
    return render(request,'users/amount.html',context)

def premium(request):
    min = 5001
    max = 10000000
    if request.method =='POST':
        amount = request.POST['amount']
        print(amount)
        if int(amount) <= max and int(amount) >= min:
            obj = Deposit.objects.create(
                amount = int(amount),
                user = request.user,
                plan = Plan.objects.get(name = 'Premium')
            )
            obj.save()
            return render(request,'users/confirm.html',{'obj':obj})
        else:
            messages.info(request,'Consider the min and max cost for this Plan')
            return redirect('premium')

    context = {
        'min':min,
        'max':max,
    }
    return render(request,'users/amount.html',context)


def confirm_trade(request,*args,**kwargs):
    id = kwargs.get('pk')
    if request.method =='POST':
        return redirect('profile')

    return render(request,'users/copy.html')

def contact(request):
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
        return redirect ('profile')

    return render(request,'mainapp/contact.html')

class WithdrawView(View):
    template_name = 'users/withdraw.html'
    #queryset = Withdrowal.objects.all()
    def get(self,*args,**kwargs):
        return render(self.request,'users/withdraw.html')
    def post(self,*args,**kwargs):
        request = self.request
        account,created= Account.objects.get_or_create(user = request.user)
        if int(request.POST['amount']) <= account.balance:
            obj = Withdrowal.objects.create(
                amount = request.POST['amount'],
                user = request.user,
                wallet_address = request.POST['wallet'],

            )
            obj.save()
            account.balance = account.balance -float(request.POST['amount'])
            account.save()
            messages.success(request,'Withdrawal request sent, please wait for approval shortly!')
            return redirect('profile')
        messages.info(request,'Your profit balance is insufficient ')
        return redirect('profile')


def uploadEvidence(request):
    if request.method =='POST':
        obj = UserPayEvidence.objects.create(
            evidence = request.FILES['file'],
            user = request.user,
        )
        obj.save()
        messages.success(request,'Uploaded!')
        return redirect('profile')
    return render(request,'users/upload.html')

def transactions(request):
    trade = Trade.objects.filter(user = request.user).order_by('?')
    ctrade = Trade.objects.filter(user = request.user,profited = False).order_by('-time_now')
    ptrade = Trade.objects.filter(user = request.user,profited = True).order_by('-time_now')
    context = {
        'trade':trade,
        'ctrade':ctrade,
        'ptrade':ptrade,
    }
    return render(request,'users/transactions.html',context)

def history(request):
    withdraws = Withdrowal.objects.filter(user = request.user,approved =True,cancel = False)
    c_withdraw = Withdrowal.objects.filter(user = request.user,approved =False,cancel = True)
    p_withdraws = Withdrowal.objects.filter(user = request.user,approved =False,cancel = False)
    context ={
        'c_withdraws':c_withdraw,
        'withdraws':withdraws,
        'p_withdraws':p_withdraws,
    }
    return render(request,'users/approved.html',context)


def settings(request):
    if request.method =='POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            country = request.POST['country']
            #wallet_address = request.POST['wallet_address']
            #wallet_type = request.POST['wallet_type']
            user = User.objects.get(id = request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            profile = Profile.objects.get(user = request.user)
            profile.phone = phone
            profile.country =country
            #profile.wallet_address = wallet_address
            #profile.wallet_type = wallet_type
            user.save()
            profile.save()
            messages.success(request,'Your profile was updated succesfully!')
            return redirect('my_profile')
        except Exception as err:
            return redirect('my_profile')



def my_profile(request):

    return render(request,'users/profile.html')

@login_required
def game1(request):
    account,created = Account.objects.get_or_create(user =request.user)

    if request.method =='POST':
        data = json.loads(request.body.decode('utf-8'))
        #data = json.loads(data_b)
        print(data)
        if data['status'] == 'failed':
            if int(data['amount']) <=account.main:
                account.main -=  int(data['amount'])
                account.save()
            pass
            #return redirect('game1')
        if data['status'] == 'success':
            account.main += int(data['amount'])*2
            account.save()

    if account.main >0:
        return render(request,'users/game.html')
    messages.info(request,'Your account is too low to play games')
    return redirect('profile')