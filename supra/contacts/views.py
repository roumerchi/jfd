from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View

from contacts.forms import ContactForm
from contacts.models import Contacts


class ContactsPageView(View):
    template_name = 'contacts/contacts.html'

    def get(self, request):
        if request.user.is_authenticated:
            contacts = Contacts.objects.filter(owner=request.user).order_by('last_name')
            contact_form = ContactForm()
            login_form = None
        else:
            contacts = None
            contact_form = None
            login_form = AuthenticationForm()

        context = {
            'contacts': contacts,
            'contact_form': contact_form,
            'login_form': login_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Обработка форм логина и добавления контакта"""
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect(request.path)
            else:
                messages.error(request, 'Неверный логин или пароль')
                # Рендерим сразу с формой логина с ошибками
                return render(request, self.template_name, {
                    'contacts': None,
                    'contact_form': None,
                    'login_form': login_form,
                })

        elif 'contact_submit' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Сначала войдите в систему')
                return redirect(request.path)

            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact.owner = request.user
                contact.status_id = 1  # статус по умолчанию
                contact.save()
                messages.success(request, 'Контакт создан')
                return redirect(request.path)
            else:
                messages.error(request, 'Ошибка при создании контакта')
                contacts = Contacts.objects.filter(owner=request.user).order_by('last_name')
                # Рендерим с формой контакта с ошибками
                return render(request, self.template_name, {
                    'contacts': contacts,
                    'contact_form': contact_form,
                    'login_form': None,
                })

        return self.get(request)
