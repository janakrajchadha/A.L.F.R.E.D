from django.views import generic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, requests, random, re
from chat.models import Question, Answer
import os
import sys
# Create your views here.

questions = Question.objects.all()
VERIFY_TOKEN = os.environ['HUB_VERIFY_TOKEN']
ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']

class AlfredView(generic.View):

    def get(self, request, **kwargs):
        if self.request.GET['hub.verify_token'] == str(VERIFY_TOKEN):
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print(incoming_message)
        for messages in incoming_message['entry']:
            for message in messages['messaging']:
                if 'message' in message and 'is_echo' not in message['message']:
                    reply_to_facebook(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def reply_to_facebook(facebook_id, received_message):
    get_info_uri = f"https://graph.facebook.com/v2.10/{facebook_id}?fields=first_name,last_name,profile_pic&access_token={ACCESS_TOKEN}"
    user_info = requests.get(get_info_uri, headers={'Content-Type': 'application/json'}).json()
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', received_message).lower().split()
    response = f"Terribly sorry, Master {user_info['first_name']}. I didn't get that."

    for token in tokens:
        for quest in questions:
            if token in quest.question_text:
                response = quest.answer.answer_text
                break

    post_uri = f'https://graph.facebook.com/v2.10/me/messages?access_token={ACCESS_TOKEN}'
    response_message = json.dumps({'recipient' : {'id' : facebook_id}, 'message':{'text' : response}})
    status = requests.post(post_uri, headers={'Content-Type': 'application/json'}, data=response_message)
