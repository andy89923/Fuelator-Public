from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Linebot library
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
#from linebot.models import MessageEvent, TextMessage, TextSendMessage

# User's models
from echobot.models import ServiceHandler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    
    serv = ServiceHandler()
    replyMess = serv.cmd(event)

    if event.message.text == "p" or event.message.text == "P" or event.message.text == "C" or event.message.text == 'c':
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url = replyMess, preview_image_url = replyMess)
        )
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = replyMess)
    )
    

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'Currently Not Support None This kind of Message')
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'Add record: (\'92\', \'95\', \'98\', \'d\') liter(l) milage(km)')
    )

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


