from django.views import generic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, requests, random, re
# Create your views here.

replies = {
            'universe' : '42',
            'up' : 'For you Master Wayne, always.',
            'defeat' : "Because some men aren't looking for something logical, like money. They can't be bought, bullied, reasoned or negotiated with. Some men just want to watch the world burn.",
            'tired' :   'Why do we fall, sir? So that we can learn to pick ourselves up.'
}

class AlfredView(generic.View):

    def get(self, request, **kwargs):
        if self.request.GET['hub.verify_token'] == '*add verify token here*':
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
        for messages in incoming_message['entry']:
            for message in messages['messaging']:
                if 'message' in message:
                    reply_to_facebook(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def reply_to_facebook(facebook_id, recevied_message):
    post_uri = 'https://graph.facebook.com/v2.6/me/messages?access_token=*add post token here*'
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    response = ''

    for token in tokens:
        if token in replies:
            response = replies[token]
            break
    if not response:
        response = "Terribly sorry, Master Wayne. I didn't get that."

    response_message = json.dumps({'recipient' : {'id' : facebook_id}, 'message':{'text' : response}})
    status = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=response_message)
    print(status.json())
