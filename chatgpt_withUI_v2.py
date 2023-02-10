import openai
import re
import tkinter as tk
from tkinter import *


root = tk.Tk()
root.title("ChatBot")

api_key_label = Label(root, text = "Api key:",width=7)
api_key_label.grid(row=0, column=0,sticky=E)
api_key_field = Entry(root,width=40)
api_key_field.grid(row=0, column=1,sticky=W)

def check_api_key():
    openai.api_key = api_key_field.get()
    if not re.match('^sk-[A-Za-z0-9-]{48}$', openai.api_key): 
        text_field.insert(END, "Please provide your API key \n\n") 
        entry_field.config(state="disabled") 
        send_btn.config(state="disabled")
        api_key_field.config(state="normal")
    else:
        entry_field.config(state="normal") 
        send_btn.config(state="normal")
        text_field.config(state="normal")
        check_btn.config(state="disabled")
        api_key_field.config(state="disabled")

check_btn = Button(root, text="input your api-key",width=15, command=check_api_key)
check_btn.grid(row=0, column=1,sticky=E,padx=10) 

entry_field = Entry(root, width=80,state="disabled",textvariable="")
entry_field.grid(row=2, column=0, columnspan=2, padx=5, pady=5) 

def send_message(): 
    openai.api_key = api_key_field.get() 
    prompt = entry_field.get() 
    if prompt == "bye": 
        root.destroy()
    else:
        try: 
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )
            if response['choices']:  
                
                
                text_field.tag_configure("green",foreground="green")
                text_field.insert(END, "Me: " + prompt + "\n\n","green")
                text_field.tag_configure("blue",foreground="blue")
                text_field.insert(END, "Bot: " + response['choices'][0]['text'].strip() + "\n\n","blue")
                text_field.see(END)
                
            else:
                text_field.insert(END, "Bot: Sorry, I don't understand \n\n")
        except openai.error.RateLimitError: 
            text_field.tag_configure("red",foreground="red")
            text_field.insert(END, "Bot: Network error, please send message again \n\n", "red")
        

send_btn = Button(root, text="Send", command=send_message,state="disabled")

send_btn.grid(row=3,columnspan=2,padx=2, pady=2)

text_field = Text(root, height=30, width=80,state=NORMAL)
text_field.grid(row=4, column=0, columnspan=2,padx=10, pady=10,ipadx=5,ipady=5)

root.mainloop()
