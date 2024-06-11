from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import LoginForm, RegisterForm, UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Student, Team
from .permissionmixin import AdminRequiredMixin


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'erp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

        form = LoginForm()
        return render(request, 'erp/login.html', {'form': form})


class RegisterView(AdminRequiredMixin, View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'erp/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('erp/login')

        form = RegisterForm()
        return render(request, 'erp/register.html', {'form': form})



class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        
        return render(request, 'erp/profile.html')



class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateProfileForm(instance=request.user)
        return render(request, 'erp/crud.html', context={'form': form})  

    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('erp/profile')

        return render(request, 'erp/profile.html', {'form': form})


class StudentView(LoginRequiredMixin, View):
    def get(self, request):
        form = User.objects.all()
        return render(request, 'erp/student.html', context={'form': form})

    def post(self, request):   
        form = StudentView(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('erp/student')

        return render(request, 'erp/student.html', {'form': form})

def delete(request, id):
    form = get_object_or_404(User, id=id)
    form.delete()
    return redirect('erp/student')


class TableView(View):
    def get(self, request):
        form = User.objects.all()
        return render(request, 'erp/table.html', context={"form": form})


class LogautView(View):
    def get(self,request):
        logout(request)
        return redirect("/")


class GroupsView(View):
    def get(self, request):
        teams = Team.objects.all()
        return render(request, 'erp/groups.html', {'teams': teams})


def users1(request, id):
    user_role = request.session.get('user_role')
    team = get_object_or_404(Team, id=id)
    students = team.students.all()
    return render(request, 'erp/student.html', context={'newstudent': students})