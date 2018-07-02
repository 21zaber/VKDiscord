#!/usr/bin/python3

from flask import Flask, request
from json import loads
from pprint import pprint
import time

from discord_hooks import Webhook

import argparse

max_post_id = 0
config = {}

app = Flask(__name__)
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, default='config.json', help='Path to config file, default: config.json')
parser.add_argument('-p', '--post', type=int, default=0, help='Ignore posts with id less or equal POST')


def proccess_new_post(post):
    global max_post_id

    # check for new post
    if int(post['id']) <= max_post_id:
        return
    max_post_id = int(post['id'])

    # search for photos in attachments
    photos = []
    for atch in post.get('attachments', []):
        if atch.get('type') == 'photo':
            photo = atch.get('photo', {})

            photo_urls = [i for i in photo.keys() if i.startswith('photo_')]
            photo_urls.sort(key=lambda x: -int(x.split('_')[-1]))

            if photo_urls and photo_urls[0]:
                photos.append(photo[photo_urls[0]])
    
    # generate text
    msg = post.get('text', '')

    # add all photos links from attachments. COMMENTED
    if False:
        msg += '\n'
        for i in photos:
            msg += '\n'+i
   
    # create Webhook object
    wh = Webhook(config['discord_webhook_url'], msg=msg)
    wh.set_footer(text='https://vk.com/wall-{}_{}'.format(config['vk_group_id'], post['id']), ts=time.time())

    # set image
    if photos:
        wh.set_image(photos[0])

    # send Webhook to discord server
    wh.post()


@app.route('/', methods=['POST'])
def callback():   
    # convert request data from JSON to Dict object
    data = loads(request.data)

    # VK API always returns type of operation
    if 'type' not in data:
        return 'fail'

    pprint(data)

    # confirmation operation
    if data['type'] == 'confirmation' and data['group_id'] == config['vk_group_id']:
        return config['vk_confirmation_code']

    # new post operation
    if data['type'] == 'wall_post_new':
        # check for non-empty object
        if data.get('object'):
            proccess_new_post(data['object'])
        return 'ok'

    return 'fail'

def run(host='0.0.0.0', port=80):
    app.run(host, port=port)

def read_config(filename):
    try:
        conf = loads(' '.join(open(filename, 'r').readlines()))
    except:
        print("ERROR: Cannot read config file: {}.".format(filename))
        raise Exception()

    if 'discord_webhook_url' not in conf:
        print("ERROR: No 'discord_webhook_url' in config file.")
        raise Exception()

    if 'vk_group_id' not in conf:
        print("ERROR: No 'vk_group_id' in config file.")
        raise Exception()

    if 'vk_confirmation_code' not in conf:
        print("ERROR: No 'vk_confirmation_code' in config file.")
        raise Exception()

    global config
    config = conf


if __name__ == '__main__':
    args = parser.parse_args()
    read_config(args.config)
    max_post_id = args.post

    run()

