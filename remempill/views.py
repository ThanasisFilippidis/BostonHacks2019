from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say

from .models import Pill, PillConsumption
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import register


class Index(View):
    template_name = '../templates/index.html'

    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(csrf_protect)
    def post(self, request):
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
                content = {'message': 'Hello, World!'}
                # return HttpResponse(user.get_id())
            else:
                error_json = {'error_message': 'User name or password is not correct.'}
                # return render(request, 'https://www.facebook.com/', error_json)
                # content = {'message': 'Wrong password!'}
                # return Response(content)
        # post request for Registering a new user
        elif request.POST['button'] == "Register":
            user_name = request.POST.get('user_name', '')
            user_password = request.POST.get('user_password', '')
            user_email = request.POST.get('user_email', '')
            if len(user_name) > 0 and len(user_password) > 0 and len(user_email) > 0:
                # check whether user account exist or not.
                user = auth.authenticate(request, username=user_name, password=user_password)
                # if user account do not exist.
                if user is None:
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
                    request.session['user_pk'] = user.id
                    return redirect('index/')
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
            call = client.calls.create(
                url='http://a5570db5.ngrok.io/remempill/dynamic_call_creator/1',
                to='+18572874360',
                from_='+12029154283'
            )

            print(call.sid)
            return HttpResponse('User account exist, please register another one.')


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
    print(dictionary)
    return dictionary.get(key)


@register.filter
def get_times(dictionary, key):
    print(key)
    print("key is ", key)
    print(dictionary.get(key))
    return dictionary.get(key)


hours = []


def pillcase(request):
    return render(request, '../templates/pillcase.html',
                  {'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday ', 'Saturday', 'Sunday'],
                   'times': ['Morning', 'Noon', 'Afternoon', 'Before Bed'], 'pills': ['pill1', 'pill2'],
                   'pillsPerDay': [{'Monday': {'Noon': ['pill1', 'pill2'], 'Morning': ['pill1', 'pill2'],
                                               'Afternoon': [], 'Before Bed': []}}],
                   'hours': {'Morning': ['06:00', '07:00', '08:00', '09:00', '10:00', '12:00'],
                             'Noon': ['12:00', '13:00', '14:00'],
                             'Afternoon': ['15:00', '16:00', '17:00', '18:00', '19:00'],
                             'Before Bed': ['20:00', '21:00', '22:00', '23:00', '00:00']}})


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
