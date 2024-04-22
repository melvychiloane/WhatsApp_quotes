from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests
import random

from myapp.myquotes import *
from myapp.riddles import *
from dotenv import load_dotenv
import os


def send_message(user_number, message):
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    twilio_number = "whatsapp:+14155238886"
    client = Client(account_sid,auth_token)

    client.messages.create(
        from_ = twilio_number,
        body = message,
        to = user_number 
    )
    

def get_quote(category):
    if is_valid_category(category):
        quotes_list =get_a_Quote(category)
        
        random_quote_index = random.randint(0,len(quotes_list)-1)
        random_quote = quotes_list[random_quote_index]
        quote_ = random_quote["quote"]
        auther_ = random_quote["author"]

        return f" '{quote_}'\n ~ {auther_}"
    else:
        random_categories_list = random_categories()
        return f"Nothing was found under specified category, here are some available categories.\n {random_categories_list[0]}, {random_categories_list[1]}, {random_categories_list[2]}, {random_categories_list[3]}, {random_categories_list[4]}, etc."

@csrf_exempt
def home(request):

    if request.method == "POST":
        print(request.POST)

        user_name = request.POST.get("ProfileName")
        user_number = request.POST.get("From")
        message = request.POST.get("Body")

        message_type = message.lower().split(" ")
        print(message)
        print(message_type)

        greetings = ["hello", 'hey', "hi"]

        if message_type[0] in greetings:
            send_message(user_number, f"hello {user_name}!")
        elif message_type[0] == "riddle" or message_type[0] == "riddles" :
            riddle_list = get_riddles()

            random_riddle_index = random.randint(0,len(riddle_list)-1)
            random_riddle = riddle_list[random_riddle_index]
            the_riddle = random_riddle["question"]
            the_answer = random_riddle["answer"]
            message = f"Question: {the_riddle}\n Answer: {the_answer}"
            send_message(user_number, message)

        elif message_type[0] == "quote":
            category = message_type[1]
            message =get_quote(category)
            send_message(user_number,message)

        else:
            message = "Sorry, could not undersatnd. Try 'quote love' to recieve a love quote or 'riddle' for a random riddle."
            send_message(user_number,message)



    return render(request, "home.html")