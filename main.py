from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state
import reactpy as rp
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


@component
def MyCrud():
    ## Creating state
    alltodo = use_state([])
    name, set_name = use_state("")
    age, set_age = use_state(0)
    password, set_password = use_state(0)

    def mysubmit(event):
        newtodo = {"name": name, "age":age , "password": password}

        # push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data

    # looping data from alltodo to show on web

    list = [
        html.li(
            {
              
            },
            f"{b} => {i['name']} ; {i['age'] }; {i['password']} ",
        )
        for b, i in enumerate(alltodo.value)
    ]

    def handle_event(event):
        print(event)

    return html.div(
        {"style": {"padding": "10px"}},
        ## creating form for submission\
        html.form(
            {"onsubmit": mysubmit},
            html.h1("Login Form - ReactPy & Mongodb"),
            html.input(
                {
                    "type": "test",
                    "placeholder": "name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
             html.input(
                {
                    "type": "test",
                    "placeholder": "age",
                    "on_change": lambda event: set_age(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            # creating submit button on form
            html.button(
                {
                    "type": "submit",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                },
                "submit",
            ),
        ),
        html.ul(list),
    )


app = FastAPI()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
app = FastAPI()

#copy and paste the mongo DB URI 
uri="mongodb+srv://Brandonweb:brandon123@cluster0.miqe39j.mongodb.net/?retryWrites=true&w=majority"
client= MongoClient (uri, server_api=ServerApi("1"))  #camel case

#defining the Db name
db= client ["web"]
collection=db["base"]

#checking the connection
try:
    client.admin.command("Ping")
    print("Successfully Connected MongoDB")

except Exception as e:
    print(e)

def login(
    login_data: dict,
 ): # removed async, since await makes code  execution pause for the promise to resolve anyway. doesnt
    username = login_data["name"]
    age = login_data
    password = login_data

    # Create a document to insert into the collection
    document = {"name":username, "age":age, "password": password}
    # logger.info("sample log messege")
    print(document)

    #Insert the docoument into the collection
    post_id = collection.insert_one(document).inserted_id #insert document
    print(post_id)

    return {"messege": "Login successful"}

configure(app, MyCrud)
