# lottery_app/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .models import User,Lottery,Participant,solidity
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Signup Successful! Please login.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'lottery_app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email_or_phone).first() or User.objects.filter(phone_number=email_or_phone).first()
            if user and user.check_password(password):
                login(request, user)
                return redirect('organizer')
            else:
                messages.error(request, "Invalid credentials!")
        else:
            messages.error(request, "Form not valid")
    else:
        print("NO")
        form = LoginForm()
    return render(request, 'lottery_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def forget_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            dob = form.cleaned_data['date_of_birth']
            request.session['reset_user'] = None
            user = User.objects.filter(email=email_or_phone, date_of_birth=dob).first() or User.objects.filter(phone_number=email_or_phone, date_of_birth=dob).first()
            if user:
                request.session['reset_user'] = user.User_id
                return redirect('reset_password')
            else:
                messages.error(request, "User not found!")
    else:
        form = ForgetPasswordForm()
    return render(request, 'lottery_app/forget_password.html', {'form': form})

def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            re_password = form.cleaned_data['re_password']
            if new_password != re_password:
                messages.error(request, "Passwords do not match!")
            else:
                user_id = request.session.get('reset_user')
                if user_id:
                    user = User.objects.get(User_id=user_id)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password Reset Successful!")
                    return redirect('login')
                else:
                    messages.error(request, "Session expired. Please try again.")
    else:
        form = ResetPasswordForm()
    return render(request, 'lottery_app/reset_password.html', {'form': form})


# Create your views here.


def index(request):
    return render(request, 'lottery_app/index.html')
def home(request):
    return render(request, 'lottery_app/home.html', {'lotteries': Lottery.objects.all()})
def runninglotteryview(request,lottery_id):
    lottery = get_object_or_404(Lottery, lottery_id=lottery_id)
    participants = Participant.objects.filter(lottery=lottery)
    return render(request, 'lottery_app/runninglottery.html', {'lottery': lottery, 'participants': participants})
def Buy(request, lottery_id):
    solidity_obj = solidity.objects.first()
    lottery = get_object_or_404(Lottery, lottery_id=lottery_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            mobile = data.get('mobile')
            age = data.get('age')
            wallet_address = data.get('wallet_address')

            Participant.objects.create(
                lottery=lottery,
                name=name,
                mobile_number=mobile,
                wallet_address=wallet_address,
                age=age
            )
            return JsonResponse({"message": "Data received successfully!"})
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Invalid data!"}, status=400)

    return render(request, 'lottery_app/Buy.html', {'lottery': lottery , 'solidity_obj': solidity_obj})
@login_required
def organizer(request):
    solidity_obj = solidity.objects.first()
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('lottery_name')
            address = data.get('contract_address')
            amount = data.get('entry_fee')
            image = data.get('image') or "default.png"
            description = data.get('description')

            if not name or not address or not amount:
                return JsonResponse({"error": "All fields are required!"}, status=400)

            Lottery.objects.create(
                lottery_name=name,
                contract_address=address,
                amount=amount,
                description=description,
                image_field=image,
                organizer=request.user,
                is_active=True,
                is_Deployed=True
            )
            print(contract_address)
            print("Lottery created successfully!")
            return JsonResponse({"message": "Lottery saved successfully!"})
        except Exception as e:
            print("Error in organizer POST:", e)
            return JsonResponse({"error": "Invalid data!"}, status=400)

    else:
        user = request.user
        lotteries = Lottery.objects.filter(organizer=user)
        contract_address = lotteries[0].contract_address if lotteries else None
        isDeployed = lotteries[0].is_Deployed if lotteries else False

        return render(request, 'lottery_app/organizer.html', {
            'user': user,
            'lotteries': lotteries,
            'contract_address': contract_address,
            'isDeployed': json.dumps(isDeployed),
            'solidity_obj': solidity_obj
        })
@login_required
def update_image(request):
    if request.method == 'POST':
        lottery_id = request.POST.get('lottery_id')
        image = request.FILES.get('image')
        lottery = get_object_or_404(Lottery, lottery_id=lottery_id)
        lottery.image_field = image
        lottery.save()
        messages.success(request, "Image updated successfully!")
        return JsonResponse({'message': 'Image updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def update_description(request):
    if request.method == 'POST':
            lottery_id = request.POST.get('lottery_id')
            data = request.POST.get('data')
            lottery = get_object_or_404(Lottery, lottery_id=lottery_id)
            lottery.description = data
            lottery.save()
            messages.success(request, "description updated successfully!")
            return JsonResponse({'message': 'Description updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def update_name(request):
    if request.method == 'POST':
            lottery_id = request.POST.get('lottery_id')
            data = request.POST.get('data')
            lottery = get_object_or_404(Lottery, lottery_id=lottery_id)
            lottery.lottery_name = data
            lottery.save()
            messages.success(request, "Name updated successfully!")
            return JsonResponse({'message': 'Name updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)




