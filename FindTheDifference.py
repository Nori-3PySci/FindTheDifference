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
default_dir = './'

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

    return vertical, horizontal, diff_char_no, output_list, char_list

def font_pick(fonts_json, fonts_dir):
    
    with open(fonts_json, 'r') as f_in:
        fonts_list = json.load(f_in)
    
    font_name = random.choice(list(fonts_list))
    font_path = os.path.join(fonts_dir, fonts_list[font_name])
    
    return font_name, font_path

def question_fig(font_path, vertical, horizontal, output_list, fig_dir, timenow):

    fp = fm.FontProperties(fname=font_path)
    
    fig = plt.figure(figsize=(horizontal, vertical))
    plt.clf()

    i = 0
    for x in range(1, horizontal+1):
        for y in range(1, vertical+1):
            plt.text((x-1)/horizontal, (y-1)/vertical, output_list[i], fontsize=55, fontproperties=fp)
            i = i + 1

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

    plt.xlabel('3PySci https://3pysci.com', fontsize=30, fontproperties=fp)

    plt.savefig(f'{fig_dir}/{timenow}.png', facecolor="white", bbox_inches='tight', pad_inches = 0.1)
    
def log_write(question_log, timenow, vertical, horizontal, diff_char_num, char_list, font_name):
    with open(question_log, 'a') as f_in:
        row = f'{timenow},{vertical},{horizontal},{diff_char_num},{char_list},{font_name}\n'
        f_in.write(row)
    
def applytotwitter(settings_json, fig_dir):
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

    text = 'この中に一つだけ違う文字があります😁\n#見つけたらRT\n\n#間違い探し\n#まちがいさがし\n#脳トレ\n#アハ体験\n#クイズ\n#Python\n#プログラミング\n\nhttps://github.com/Nori-3PySci/find_the_difference'

    api.update_with_media(status = text, filename = f'{fig_dir}/{upload_png}')


# -

def main():
    
    question_json = os.path.join(default_dir, 'question.json')
    fonts_json = os.path.join(default_dir, 'fonts.json')
    settings_json = os.path.join(default_dir, 'settings.json')
    question_log = os.path.join(default_dir, 'question_log.txt')
    
    timenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    fonts_dir = os.path.join(default_dir, 'fonts')
    fig_dir = os.path.join(default_dir, 'fig')
    
    vertical, horizontal, diff_char_num, output_list, char_list = output_char_list(question_json)
    font_name, font_path = font_pick(fonts_json, fonts_dir)
    question_fig(font_path, vertical, horizontal, output_list, fig_dir, timenow)
    log_write(question_log, timenow, vertical, horizontal, diff_char_num, char_list, font_name)
    applytotwitter(settings_json, fig_dir)


if __name__ == '__main__':
    main()


