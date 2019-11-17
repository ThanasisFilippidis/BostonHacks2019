from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say

from .models import Pill, PillConsumption, GrandParent
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import register

import datetime


class Index(View):
    template_name = '../templates/index.html'

    def get(self, request):
        if not user_session_check(request):
            return render(request, self.template_name, context={'user': ""})
        return render(request, self.template_name, context={'user': request.session['user_name']})

    @method_decorator(csrf_protect)
    def post(self, request):
        print("ELA MWRE")
        # post request for Login existing user
        if request.POST['button'] == "Login":
            user_email = request.POST.get('user_email', '')
            user_password = request.POST.get('user_password', '')
            print('user_email = ' + user_email)
            print('user_password = ' + user_password)
            # authenticate user account.
            user = auth.authenticate(request, username=user_email, password=user_password)
            if user is not None:
                # login user account.
                auth.login(request, user)
                # response = HttpResponseRedirect('https://www.google.com/maps')
                # set cookie to transfer user name to login success page.
                # response.set_cookie('user_name', user_name, 3600)
                request.session['user_name'] = user.username
                content = {'message': 'Hello, World!'}
                print("EDW")
                print(user)
                user_name = auth.get_user(request).username
                request.session['user_name'] = user_name
                # print(type(user_name))
                return render(request, self.template_name, {'user': user_name})
                # return HttpResponse(user.get_id())
            else:
                error_json = {'error_message': 'User name or password is not correct.'}
                # return render(request, 'https://www.facebook.com/', error_json)
                # content = {'message': 'Wrong password!'}
                return render('index', context={'user': ""})
        # post request for Registering a new user
        elif request.POST['button'] == "Register":
            print("ELA MWRE2")
            user_name = request.POST.get('user_name', '')
            user_password = request.POST.get('user_password', '')
            user_email = request.POST.get('user_email', '')
            if len(user_name) > 0 and len(user_password) > 0 and len(user_email) > 0:
                print("ELA MWRE3")
                # check whether user account exist or not.
                user = auth.authenticate(request, username=user_name, password=user_password)
                # if user account do not exist.
                if user is None:
                    print("ELA MWRE4")
                    # create user account and return the user object.
                    user = get_user_model().objects.create_user(username=user_name, password=user_password,
                                                                email=user_email)
                    # update user object staff field value and save to db.
                    if user is not None:
                        # user.is_staff = True
                        # save user properties in sqlite auth_user table.
                        user.save()
                    # redirect web page to register success page.
                    # response = HttpResponseRedirect('/user/register_success/')
                    # response = HttpResponse('https://www.google.com/maps')
                    # set user name, pasword and email value in session.
                    request.session['user_name'] = user_name
                    request.session['user_password'] = user_password
                    request.session['user_email'] = user_email
                    # return HttpResponse(user.get_id())
                    return redirect('index')
                    # return HttpResponse(user.get_id())
                else:
                    error_json = {'error_message': 'User account exist, please register another one.'}
                    # return render(request, 'https://www.facebook.com/', error_json)
                    # return HttpResponse('User account exist, please register another one.')
        elif request.POST['button'] == "send sms":
            # Your Account SID from twilio.com/console
            account_sid = "ACd4f1564dcc6d85a1d13a45a50c35d8ae"
            # Your Auth Token from twilio.com/console
            auth_token = "1e270dfee30da4e41982fc38d7cb125f"

            client = Client(account_sid, auth_token)

            # message = client.messages.create(
            #     to="+18574729477",
            #     from_="+12029154283",
            #     body="Gamiesai pou den irthes")
            # call = client.calls.create(
            #     url='http://a5570db5.ngrok.io/remempill/dynamic_call_creator/1',
            #     to='+18572874360',
            #     from_='+12029154283'
            # )
            print("EEEEEEEEEE")
            min_time = timezone.now()
            max_time = min_time + datetime.timedelta(hours=0, minutes=59, seconds=59)
            print(min_time)
            print(max_time)
            if PillConsumption.objects.get(pk=2).time_to_consume >= min_time and PillConsumption.objects.get(
                    pk=2).time_to_consume <= max_time:
                print("prepei")
            else:
                print("den prepei")
            # print(str(PillConsumption.objects.get(pk=1).time_to_consume.day) + str(curr_time))

            # print(call.sid)
            return HttpResponse('User account exist, please register another one.')


class Pillcase(View):
    template_name = '../templates/pillcase.html'

    def get(self, request, elder_id):
        pills = GrandParent.get_pills(elder_id)
        print(pills)
        toBeConsumed = []
        for item in pills:
            print(item.name)
            toBeConsumed.append(PillConsumption.objects.filter(pill=item))

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday ', 'Saturday', 'Sunday']
        times = ['06:00', '07:00', '08:00', '09:00', '10:00', '12:00', '12:00', '13:00', '14:00', '15:00', '16:00',
                 '17:00', '18:00', '19:00' '20:00', '21:00', '22:00', '23:00', '00:00']

        for day in days:
            for hour in hours:
                for pill in toBeConsumed:
                    print(pill.time_to_consume)

        elder = GrandParent.objects.get(id=elder_id)
        print(elder)

        return render(request, '../templates/pillcase.html',
                      {'user': elder,
                       'days': days,
                       'times': ['Morning', 'Noon', 'Afternoon', 'Before Bed'], 'pills': pills,
                       'pillsPerDay': [{'Monday': {'Noon': ['1', '1'], 'Morning': ['1', '1'],
                                                   'Afternoon': [], 'Before Bed': []}}],
                       'hours': {'Morning': ['06:00', '07:00', '08:00', '09:00', '10:00', '12:00'],
                                 'Noon': ['12:00', '13:00', '14:00'],
                                 'Afternoon': ['15:00', '16:00', '17:00', '18:00', '19:00'],
                                 'Before Bed': ['20:00', '21:00', '22:00', '23:00', '00:00']}, 'exactTimes': times})
        # print(elder_id)

    def post(self, request, elder_id):

        print(request.POST.get('button'))
        # print(request.POST.get('name'))
        print(request.POST.get('button')[len("addToTime"):])

        name = request.POST.get('name')
        size = request.POST.get('size')
        color = request.POST.get('color')
        shape = request.POST.get('shape')

        print(auth.get_user(request))

        print(name, size, color, shape)
        newPill = Pill(name=name, size=size, color=color, shape=shape, remaining=10,
                       owner=GrandParent.objects.get(id=elder_id))
        print(newPill)
        newPill.save()

        days = request.POST.get('days')
        times = request.POST.get('times')

        target = "/pillcase/" + str(elder_id)

        return redirect(target)


@csrf_exempt
def dynamic_call_creator(request, consumption_id):
    resp = VoiceResponse()

    # Start our <Gather> verb
    action = "http://a5570db5.ngrok.io/remempill/callresponse/" + consumption_id
    gather = Gather(num_digits=1, actionOnEmptyResult="true", action=action, timeout=10)
    consumption = PillConsumption.objects.get(pk=int(consumption_id))
    pill = consumption.pill
    saying = 'Hey grandpa! Please press five after taking your ' + pill.name + ' pill. Just to help you remember, this is a '
    saying += pill.color + ' pill that has a ' + pill.size + ' size ' + ' and its shape is ' + pill.shape
    gather.say(saying)
    resp.append(gather)
    say = Say("I see that you did not take your pill. I will call you back soon")
    resp.append(say)

    print(resp)
    # return HttpResponse('User account exist, please register another one.')

    return HttpResponse(resp)


@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return []
    # print(dictionary)
    return dictionary.get(key)


@register.filter
def get_times(dictionary, key):
    # print(key)
    # print("key is ", key)
    print(dictionary.get(key))
    return dictionary.get(key)


hours = []


# def pillcase(request):
#
# def pillcase(request, elder_id):
#     if request.method == 'POST':
#         print("hahshahshsa")
#     else:
#         print('ajdjajad')
#
#     return render(request, '../templates/pillcase.html',
#                   {'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday ', 'Saturday', 'Sunday'],
#                    'times': ['Morning', 'Noon', 'Afternoon', 'Before Bed'], 'pills': ['pill1', 'pill2'],
#                    'pillsPerDay': [{'Monday': {'Noon': ['pill1', 'pill2'], 'Morning': ['pill1', 'pill2'],
#                                                'Afternoon': [], 'Before Bed': []}}],
#                    'hours': {'Morning': ['06:00', '07:00', '08:00', '09:00', '10:00', '12:00'],
#                              'Noon': ['12:00', '13:00', '14:00'],
#                              'Afternoon': ['15:00', '16:00', '17:00', '18:00', '19:00'],
#                              'Before Bed': ['20:00', '21:00', '22:00', '23:00', '00:00']}})
#

@csrf_exempt
def callresponse(request, consumption_id):
    # print("ELA RE MALAKA")
    # print(request.POST['Digits'])
    if len(request.POST['Digits']) > 0:
        consumption = PillConsumption.objects.get(pk=consumption_id)
        consumption.set_consumed()
        return HttpResponse(
            '<Response><Say>I see you took your pill. Thats great, I will call you again soon!</Say></Response>')
    return HttpResponse(
        '<Response><Say>I see that you did not take your pill. I will call you back soon</Say></Response>')


def addPill(request):
    print(request)

    return HttpResponseRedirect("pillcase")


def profiles(request):
    caretaker = auth.get_user(request)
    print("jajaja")
    result = caretaker.get_elders()
    print(result)

    return render(request, "../templates/profiles.html", {'profiles': result})


def goToPillcase(request):
    elderId = request.POST.get('button')
    print(elderId)
    id = 1
    target = "/pillcase/" + str(elderId)

    return redirect(target)


def addElderly(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    phone = request.POST.get('phone')
    greeting = request.POST.get('greeting')
    caretaker = auth.get_user(request)

    elderly = GrandParent(name=name, surname=surname, phone=phone, greeting_message=greeting, care_taker=caretaker)
    elderly.save()

    return redirect("profiles", request)


@csrf_exempt
def mylogout(request):
    template_name = '../templates/index.html'
    request.session['user_name'] = ""
    auth.logout(request)
    return redirect('index')
    # return HttpResponseRedirect('/remempill')
    # return render(request, template_name, context={'user': ""})
    # return HttpResponseRedirect(reverse('index'))


def user_session_check(request):
    # get current user's details and check if he is logged in indeed
    try:
        return request.session['user_name']
    except KeyError:
        return None
