from __future__ import unicode_literals

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import codecs
import re

PYTHONIOENCODING="utf-8"


def plot_mapping(mapping, plotname="", azerty=-1, numbers=-1, letters=-1, objective="",\
                 p=-1, a=-1, f=-1, e=-1, w_p=-1,w_a=-1, w_f=-1, w_e=-1 ):
    
    if azerty == -1:
        azerty = pd.read_csv("input\\azerty.csv", index_col=1, sep="\t", encoding='utf-8', quoting=3).to_dict()["keyslot"]
    if numbers == -1:
        numbers = pd.read_csv("input\\numbers.csv", index_col=1, sep="\t", encoding='utf-8', quoting=3).to_dict()["keyslot"]
    if letters == -1:
        with codecs.open('input\\letters.txt', encoding='utf-8') as file:
            letters = file.read().splitlines()   
        
    with open('input\\all_slots.txt') as file:    
        all_slots = file.read().splitlines()    
    #box dimensions
    key_height = 4
    key_width = 4

    #keyboard specifics
    row_distance = 0.5
    column_distance = 0.5
    row_shift = {'A':0, 'B':0, 'C':key_width/2, 'D':key_width, 'E':3*key_width/2}

    #text positions
    pos_normal_x = 0.5
    pos_normal_y = 0.5
    pos_shift_x = 0.5
    pos_shift_y = key_height-0.5
    pos_alt_x = key_width-0.5
    pos_alt_y = 0.5
    pos_alt_shift_x = key_width-0.5
    pos_alt_shift_y = key_height-0.5


    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(10,4)
    row_numbers = {u"A":0, u"B":1, u"C":2, u"D":3, u"E":4}
    for slot in all_slots:
        row = row_numbers[slot[0]]
        column = int(slot[1:3])
        level = slot[4:]

        if level == "":
            height = key_height
            width = key_width
            #Space
            if row==0 and column == 3:
                width = key_width*5 + 4*row_distance

            x = (column*key_width)+column*column_distance - row_shift[slot[0]]
            y = (row*key_height) + row*row_distance

            ax.add_patch(
                patches.Rectangle(
                    (x,y),   # (x,y)
                    width,          # width
                    height,          # height
                    fill=False
                )
    )

    #Add letter annotation
    for l in letters:
        if not l == "space":
            slot = azerty[l]
            row = row_numbers[slot[0]]
            column = int(slot[1:3])
            level = slot[4:]

            if level == "":
                pos_x = pos_normal_x
                pos_y = pos_normal_y
                ha = 'left'
                va = 'bottom'
            if level == "Shift":
                pos_x = pos_shift_x
                pos_y = pos_shift_y
                ha = 'left'
                va = 'top'
            if level == "Alt":
                pos_x = pos_alt_x
                pos_y = pos_alt_y
                ha = 'right'
                va = 'bottom'
            if level == "Alt_Shift":
                pos_x = pos_alt_shift_x
                pos_y = pos_alt_shift_y
                ha = 'right'
                va = 'top'
            x = (column*key_width)+column*column_distance + pos_x - row_shift[slot[0]]
            y = (row*key_height) + row*row_distance + pos_y

            ax.text(x,y,l,            
                horizontalalignment=ha,
                verticalalignment=va,
                fontsize=10,
                color=(0.4,0.4,0.4)        
                )
            
    #Add number annotation
    for (l,slot) in numbers.iteritems():                    
        row = row_numbers[slot[0]]
        column = int(slot[1:3])
        level = slot[4:]

        if level == "":
            pos_x = pos_normal_x
            pos_y = pos_normal_y
            ha = 'left'
            va = 'bottom'
        if level == "Shift":
            pos_x = pos_shift_x
            pos_y = pos_shift_y
            ha = 'left'
            va = 'top'
        if level == "Alt":
            pos_x = pos_alt_x
            pos_y = pos_alt_y
            ha = 'right'
            va = 'bottom'
        if level == "Alt_Shift":
            pos_x = pos_alt_shift_x
            pos_y = pos_alt_shift_y
            ha = 'right'
            va = 'top'
        x = (column*key_width)+column*column_distance + pos_x - row_shift[slot[0]]
        y = (row*key_height) + row*row_distance + pos_y

        ax.text(x,y,l,            
            horizontalalignment=ha,
            verticalalignment=va,
            fontsize=10,
            color=(0.4,0.4,0.4)        
         )
           
    #Add mapping annotation
    for (l,slot) in mapping.iteritems():        
        row = row_numbers[slot[0]]
        column = int(slot[1:3])
        level = slot[4:]        

        if level == "":
            pos_x = pos_normal_x
            pos_y = pos_normal_y
            ha = 'left'
            va = 'bottom'
        if level == "Shift":
            pos_x = pos_shift_x
            pos_y = pos_shift_y
            ha = 'left'
            va = 'top'
        if level == "Alt":
            pos_x = pos_alt_x
            pos_y = pos_alt_y
            ha = 'right'
            va = 'bottom'
        if level == "Alt_Shift":
            pos_x = pos_alt_shift_x
            pos_y = pos_alt_shift_y
            ha = 'right'
            va = 'top'
        x = (column*key_width)+column*column_distance + pos_x - row_shift[slot[0]]
        y = (row*key_height) + row*row_distance + pos_y

        if u"d" in l: #dead key
            l = re.sub('d', '', l)
            c = "#C44E52"
        else:
            c = "#4C72B0"
            
        ax.text(x,y,l,            
            horizontalalignment=ha,
            verticalalignment=va,
            fontsize=12,
            color=c        
            )
    title = ""
    if not objective=="":
        #print objective values
        title = "Objective value: %.3f"%objective
    if not (a==-1 or e==-1 or f==-1 or p==-1):
        title = title+ " \n Performance: %.2f * %.3f \n Association: %.2f * %.3f \n Familiarity: %.2f * %.3f \n\
        Ergonomics: %.2f * %.3f "%(w_p, p, w_a, a, w_f, f, w_e, e)
    ax.set_title(title, horizontalalignment="right")
    ax.set_xlim([-8,58])
    ax.set_ylim([-1,26])
    plt.axis('off')
    if not plotname=="":
        fig.savefig(plotname, dpi=300, bbox_inches='tight')	    
    
def log_mapping(mapping, path):
    separator = "\t"
    df = pd.DataFrame()
    df = df.from_dict(mapping, orient="index")
    df.to_csv(path, sep=str(separator), quoting=3, encoding="utf-8")


def create_map_from_mst(path):
    path = "mappings\\solution_3.3184.mst"
    mst = codecs.open(path, 'r', encoding="utf-8")
    first_line = mst.readline()
    parts = first_line.split(" ")
    objective = float(parts[-1])
    all_lines = mst.read().splitlines()

    mapping = {}
    for line in all_lines:
        var_val = line.split(" ")
        if var_val[1] == "1":
            maps = var_val[0].split("_to_")
            mapping[maps[0]] = maps[1]
    return mapping, objective