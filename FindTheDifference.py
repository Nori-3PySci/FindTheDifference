# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import random
import json
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import datetime
import tweepy
import os

def output_char_list(question_json, cell_min=10, cell_max=20):
    with open(question_json, 'r') as f_in:
        question_list = json.load(f_in)

    char_list = question_list[random.choice(list(question_list))]

    vertical = random.randint(cell_min, cell_max)
    horizontal = random.randint(cell_min, cell_max)
    num_char = vertical*horizontal
    diff_char_no = random.randint(1, num_char)

    output_list = []

    for num in range(1, num_char+1):
        if num == diff_char_no:
            output_list.append(char_list[1])
        else:
            output_list.append(char_list[0])

    return vertical, horizontal, output_list

def question_fig(fonts_json, vertical, horizontal, output_list, fig_dir, fontsize, promotion_text, promotion_fontsize):

    timenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    with open(fonts_json, 'r') as f_in:
        fonts_list = json.load(f_in)

    font_path = fonts_list[random.choice(list(fonts_list))]

    fp = fm.FontProperties(fname=font_path)
    
    fig = plt.figure(figsize=(vertical,horizontal))
    plt.clf()

    i = 0
    for x in range(1, vertical+1):
        for y in range(1, horizontal+1):
            plt.text((x-1)/vertical, (y-1)/horizontal, output_list[i], fontsize=fontsize, fontproperties=fp)
            i = i + 1

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

    plt.xlabel(promotion_text, fontsize=promotion_fontsize, fontproperties=fp)

    plt.savefig(f'{fig_dir}/{timenow}.png', bbox_inches='tight', pad_inches = 0.1)
    
def applytotwitter(settings_json, fig_dir, tweet_text):
    png_files = []
    for file in os.listdir(fig_dir):
        if file[-4:] == '.png':
            png_files.append(file)

    upload_png = sorted(png_files)[-1]
    
    with open(settings_json, 'r') as f_in:
        settings = json.load(f_in)

    auth = tweepy.OAuthHandler(settings['consumer_key'], settings['consumer_secret'])
    auth.set_access_token(settings['access_token'], settings['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit = True)

    text = tweet_text

    api.update_with_media(status = text, filename = f'{fig_dir}/{upload_png}')


# -

def main():
    question_json = './question.json'
    fonts_json = './fonts.json'
    settings_json = './settings.json'
    
    fig_dir = './fig'
    fontsize = 55
    
    tweet_text = 'この中に一つだけ違う文字があります😁\n#見つけたらRT'
    
    promotion_text = '3PySci https://3pysci.com' 
    promotion_fontsize = 30
    
    vertical, horizontal, output_list = output_char_list(question_json)
    question_fig(fonts_json, vertical, horizontal, output_list, fig_dir, fontsize, promotion_text, promotion_fontsize)
    applytotwitter(settings_json, fig_dir, tweet_text)


if __name__ == '__main__':
    main()


