from django.http import HttpResponse
from channels.sessions import channel_session
from channels.handler import AsgiHandler
from channels import Group
import pickle
import logging

log = logging.getLogger(__name__)

def http_request(message):
    response = HttpResponse("Hello world from a consumer!")
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

@channel_session
def ws_connect(msg):
    print("CONNECT ---------------------------- START")
    print(msg.__dict__)

    try:
        prefix, label = msg['path'].strip('/').split('/')
        if prefix is not 'chat':
            log.debug('invalid ws path=%s', msg['path'])
            return
        #room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', msg['path'])
        return
    #except Room.DoesNotExist:
    #    log.debug('ws room does not exist label=%s', label)
    #    return
    else:
        return

    msg.reply_channel.send({'accept': True})
    Group('custom_broadcast').add(msg.reply_channel)
    print("CONNECT ------------------------------ END")

@channel_session
def ws_disconnect(msg):
    print("DISCONNECT ---------------------------- START")
    print(msg.__dict__)
    Group('custom_broadcast').discard(msg.reply_channel)
    print("DISCONNECT ------------------------------ END")

@channel_session
def ws_receive(msg):
    print("RECEIVE ---------------------------- START")
    print(msg.__dict__)
    Group('custom_broadcast').send({
        'text': msg.content['text']
    })
    print("RECEIVE ------------------------------ END")

#{'reply_channel': <channels.channel.Channel object at 0x7f8eb00ae358>, 'content': {'server': ['172.20.0.4', 8000], 'query_string': '', 'headers': [[b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits'], [b'sec-websocket-key', b'P96y2sHxK81p+TlkoQuUZg=='], [b'pragma', b'no-cache'], [b'sec-websocket-version', b'13'], [b'accept-encoding', b'gzip, deflate, sdch, br'], [b'dnt', b'1'], [b'cache-control', b'no-cache'], [b'accept-language', b'en-US,en;q=0.8'], [b'host', b'127.0.0.1:8000'], [b'user-agent', b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'], [b'upgrade', b'websocket'], [b'connection', b'Upgrade'], [b'origin', b'http://127.0.0.1:8000']], 'path': '/socket', 'reply_channel': 'daphne.response.JwhetSkDmr!LWLYhnpgYa', 'order': 0, 'client': ['172.20.0.1', 35030]}, 'channel': <channels.channel.Channel object at 0x7f8eb00ae2e8>, 'channel_layer': <channels.asgi.ChannelLayerWrapper object at 0x7f8eb1c96c88>, 'channel_session': <django.contrib.sessions.backends.db.SessionStore object at 0x7f8eb0102e80>}



