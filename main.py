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
    is_edit = use_state(False)
    nameedit, set_name = use_state("")
    ageedit, set_age = use_state(0)
    passwordedit, set_password = use_state(0)
    id_edit = use_state(0)

    @rp.event(prevent_default=True)
    def mysubmit(event):
        newtodo = {"name": name, "age": age, "password": password}

        # push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data
   
    def deletebtn(b):
        is_edit.set_value(True)
        for i,x in  enumerate(alltodo.value):
            if i == b:
                x['name'] = nameedit
                x['age'] = ageedit
                x['password'] = passwordedit
            print("you select",b)
            update_todos = [item for index,item in enumerate(alltodo.value ) if index != b]
            alltodo.set_value(update_todos)
    def editbtn(b):
        is_edit.set_value(True)
        for i,x in enumerate(alltodo.value):
            if i == b:
                x['name'] = nameedit
                x['age'] = ageedit
                x['password'] = passwordedit
                id_edit.set_value(b)

    def savedata(event):
        for i,x in enumerate(alltodo.value):
            if i == id_edit.value:
                x['name'] = nameedit
                x['age'] = ageedit
                x['password'] = passwordedit
                is_edit.set_value(False)

    # looping data from alltodo to show on web
    list = [
        html.li(
            {
              
            },
            f"{b} => {i['name']} ; {i['age']} ; {i['password']} ",
            html.button({
                "on_click":lambda event, b=b:deletebtn(b)
            },"delete"),
            html.button({
                "on_click":lambda event, b=b:editbtn(b)
            },"edit"),
        )
        for b, i in enumerate(alltodo.value)
    ]

    def handle_event(event):
        print(event)

    return html.div(
        {"style": {"padding": "10px"}},
        ## creating form for submission\
        html.form(
            {"on submit": mysubmit},
            html.h1("Welcome to Anime World"),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Age",
                    "on_change": lambda event: set_age(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Password",
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
                "Join",
            ),
        ),
        html.ul(list),
    )


app = FastAPI()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Brandonweb:brandon123@cluster0.miqe39j.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["Anime"]
collection = db["new"]
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def login(
    login_data: dict,
):  # removed async, since await makes code execution pause for the promise to resolve anyway. doesnt matter.
    username = login_data["name"]
    age      = login_data["age"]
    password = login_data["password"]

    # Create a document to insert into the collection
    document = {"name": username, "age": age, "password": password}
    # logger.info('sample log message')
    print(document)

    # Insert the document into the collection
    post_id = collection.insert_one(document).inserted_id  # insert document
    print(post_id)

    return {"message": "Login successful"}


configure(app, MyCrud)
