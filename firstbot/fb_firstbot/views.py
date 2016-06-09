# firstbot/fb_firstbot/views.py
import json
import requests
import re
import random

from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Tracker
from pprint import pprint

page_access = "EAAOXivbQaJoBAK3hB0NPIL08mW2BrXA1u6ZChMxdB11P2nZA08OsTQR1IKIxz9Vr1f7BuvNES90gtEaFacclAczAGgpZAkU8BEOzLjraWkzVdpDLcXrLayoSEgBwXEMZCdLFqObl5AEAC3QxpF3KUhsJAOvsdtpX6pW7scmAaQZDZD"

def post_facebook_message(fbid, recevied_message):
	# Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    response = 'a'
    # for token in tokens:
    #     if token in responses:
    #         response = random.choice(responses[token])
    #         break
    # if not response:
    #     response = "I'm sorry I didn't understand your message." 
    # if response == "What can I help you with today?":
    # 	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    # 	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'%s'%page_access}
    # 	user_details = requests.get(user_details_url, user_details_params).json()
    # 	response = "Hey " + user_details['first_name'] + "! " + response
    t = None
    try:
    	t = Tracker.objects.get(user_id=fbid)
    except ObjectDoesNotExist:
    	t = Tracker(user_id=fbid)
    message_num = t.message_num
    if message_num == 0:
    	response = "Welcome to the Roomhints designer bot. How can I help you design your space?"
    elif message_num == 1:
    	response = "Go ahead and upload a photo of your room."
    elif message_num == 2:
    	response = "What is your budget?"
    elif message_num == 3:
    	response = "Great! We we will send some design ideas your way soon."
    t.message_num += 1
    t.save()
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%page_access 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


# Create your views here.
class FirstBotView(generic.View):
    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    try:
                    	post_facebook_message(message['sender']['id'], message['message']['text']) 
                    except:
                    	pass  
        return HttpResponse()
    def get(self, request, *args, **kwargs):
    	if self.request.GET['hub.verify_token'] == '9712179':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

