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
            html.h1("Welcom to Anime orld"),
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
                    "type": "join",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                },
                "join",
            ),
        ),
        html.ul(list),
    )
@component
def DataList(items, filter_by_priority=None, sort_by_priority=False):
    if filter_by_priority is not None:
        items = [i for i in items if i["priority"] <= filter_by_priority]
    if sort_by_priority:
        items = sorted(items, key=lambda i: i["priority"])
    list_item_elements = [html.li(i["text"]) for i in items]
    return html.ul(list_item_elements)

@component
def TodoList():
    tasks = [
        {"text": "Make breakfast", "priority": 0},
        {"text": "Feed the dog", "priority": 0},
        {"text": "Do laundry", "priority": 2},
        {"text": "Go on a run", "priority": 1},
        {"text": "Clean the house", "priority": 2},
        {"text": "Go to the grocery store", "priority": 2},
        {"text": "Do some coding", "priority": 1},
        {"text": "Read a book", "priority": 1},
    ]
    return html.section(
        html.h1("My Todo List"),
        DataList(tasks, filter_by_priority=1, sort_by_priority=True),
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
    age = login_data["age"]
    password = login_data["password"]

    # Create a document to insert into the collection
    document = {"name":username, "age":age, "password": password}
    # logger.info("sample log messege")
    print(document)

    #Insert the docoument into the collection
    post_id = collection.insert_one(document).inserted_id #insert document
    print(post_id)

    return {"messege": "Login successful"}

configure(app, MyCrud)
