#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:45:34 2020
@author: jzeisler
"""
#import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import date
import dns
import tkinter as tk


#create Mongo client with a connection to the Atlas cluster
client = MongoClient('mongodb+srv://notes_user:OkSRSGccxwZi1fUn@cluster0.r41mv.mongodb.net')
#select notes database from the Mongo cluster
db = client.notes
#select scraps Collection from the notes database
scraps = db.scraps

def list_scraps():
    results = scraps.find()
    
    if daily_view.get():
        show_daily_view(results)
    else:
        show_full_view(results)

            
def filter_scraps(event):
    results = scraps.find()
    
    filters = []
    filters = tag_filter.get().split()
    filtered_results = []
    
    if len(filters):
        for document in results:
            for f in filters:
                if f in document['tags']:
                    filtered_results.append(document)
    else:
        filtered_results = results
                    
    if daily_view.get():
        show_daily_view(filtered_results)
    else:
        show_full_view(filtered_results)

    
    
def show_daily_view(results):
    for document in results:
        if document['ts'].date() == date.today():                        
            if ts_view.get():
                txt_display.insert(tk.END, str(document['ts']) + '\n')
            else:
                txt_display.insert(tk.END, '**************************\n')
            txt_display.insert(tk.END, document['text'] + '\n')  
            
def show_full_view(results):
    for document in results:
        if ts_view.get():
            txt_display.insert(tk.END, str(document['ts']) + '\n')
        else:
            txt_display.insert(tk.END, '**************************\n')
        txt_display.insert(tk.END, document['text'] + '\n')
        
def save():
    tags = []
    text = txt_edit.get(1.0, tk.END)
    tags = tags_edit.get().split()
    timestamp = datetime.now()
    
    scrap_data = {
        'ts': timestamp,
        'text': text,
        'tags': tags
        }
        
    result = scraps.insert_one(scrap_data).inserted_id
    print(result)
    
    txt_edit.delete(1.0, tk.END)
    tags_edit.delete(0, tk.END)
    list_scraps()
    
    
def save_return(event):
    tags = []
    text = txt_edit.get(1.0, tk.END)
    #print("text " + text)
    tags = tags_edit.get().split()
    timestamp = datetime.now()
    
    if text.strip():
        scrap_data = {
            'ts': timestamp,
            'text': text,
            'tags': tags
            }
        result = scraps.insert_one(scrap_data)
    
    txt_edit.delete(1.0, tk.END)
    tags_edit.delete(0, tk.END)
    list_scraps()
  
"""    
def show_tags():
    tag_list = []
    results = scraps.find()
    for document in results:
        for tag in document['tags']:
            if tag not in tag_list:
                tag_list.append(tag)
            
    for t in tag_list:
        cbutton = 
"""        
            
window = tk.Tk()
window.title("NoteZ")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
fr_input = tk.Frame(window, relief=tk.RAISED, bd=2)
#fr_tags = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_save = tk.Button(fr_buttons, text="Save", command=save)
btn_filter = tk.Button(fr_buttons, text="Filter", command=list_scraps)
#btn_filter = tk.Button(fr_buttons, text="Filter", command=list_scraps)

daily_view = tk.IntVar()
ts_view = tk.IntVar()
dv_box = tk.Checkbutton(fr_buttons, text='Daily View',variable=daily_view, 
                        onvalue=1, offvalue=0, command=list_scraps)
ts_box = tk.Checkbutton(fr_buttons, text='Show Timestamps',variable=ts_view, 
                        onvalue=1, offvalue=0, command=list_scraps)

btn_save.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
btn_filter.grid(row=1, column=0, sticky="ew", padx=10)
dv_box.grid(row=2, column=0, sticky="ew", padx=10)
ts_box.grid(row=3, column=0, sticky="ew", padx=10)

txt_edit = tk.Text(fr_input, height=50, relief=tk.RAISED, bd=2)
tags_edit = tk.Entry(fr_input, relief=tk.RAISED, bd=2)
tags_edit.bind("<Return>", save_return)
txt_display = tk.Text(fr_input, relief=tk.RAISED, bd=2)
tag_filter = tk.Entry(fr_input, relief=tk.RAISED, bd=2)
tag_filter.bind("<Return>", filter_scraps)

txt_edit.grid(row=0, column=0)
tags_edit.grid(row=1, column=0, sticky="new")
#txt_display.grid(row=0, column=1, rowspan=2, sticky="nsew")
txt_display.grid(row=0, column=1, sticky="nsew")
tag_filter.grid(row=1, column=1, sticky="new")

fr_buttons.grid(row=0, column=0, sticky="ns")
fr_input.grid(row=0, column=1, sticky="ns")

list_scraps()

window.mainloop()
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
