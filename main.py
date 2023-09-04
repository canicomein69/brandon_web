
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state,web
import reactpy as rp
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Union


@component
def MyCrud():
    ## Creating state
    alltodo = use_state([])
    name, set_name = use_state("")
    age, set_age = use_state("")
    postal_code, set_postal_code = use_state("")
    password, set_password = use_state("")
    is_edit = use_state(False)
    nameedit, set_nameedit = use_state("")
    ageedit, set_ageedit = use_state("")
    postal_codeedit, set_postal_codeedit = use_state("")
    passwordedit, set_passwordedit = use_state("")
    id_edit = use_state(0)
    edittodo =  use_state([])
    mui = web.module_from_template(
    "react",
    "@mui/material"
    
    )

    Button = web.export(mui,"Button")
    Card = web.export(mui,"Card")
    CardConetent = web.export(mui,"CardContent")
    Typography = web.export(mui,"Typography")
    def mysubmit(event):
        newtodo = {"name": name, "age":age , "postal_code":postal_code , "password": password}
        # push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data
       # looping data from alltodo to show on web
    def deletebtn(b):
        is_edit.set_value(True)
        for i,x in  enumerate(alltodo.value):
            if i == b:
                x['name'] = nameedit
                x['age'] = ageedit
                x['postal_code'] = postal_codeedit
                x['password'] = passwordedit
            print("you select",b)
            update_todos = [item for index,item in enumerate(alltodo.value ) if index != b]
            alltodo.set_value(update_todos)
    def editbtn(b):
        is_edit.set_value(True)
        for i,x in enumerate(alltodo.value):
            if i == b:
                set_nameedit(x['name'])
                set_ageedit(x['age'])
                set_postal_codeedit(x['postal_code'])
                set_passwordedit(x['password'])
                id_edit.set_value(b)
    def savedata(event):
        for i,x in enumerate(alltodo.value):
            if i == id_edit.value:
                x['name'] = nameedit
                x['age'] = ageedit
                x['postal_code']= postal_codeedit
                x['password'] = passwordedit
        is_edit.set_value(False)    
        set_nameedit("")
        set_ageedit("")
        set_postal_codeedit("")
        set_passwordedit("")
        updatetodo = {"updatename": nameedit, "updateage": ageedit, "updatepostal_code":postal_codeedit, "updatepassword" : passwordedit}
        edittodo.set_value(edittodo.value + [updatetodo])
        update(updatetodo)
   
    list = [
        html.br(),
        html.p(""),
        html.li(
            {
              "key":b,
             
            },
            f"{b} => {i['name']} ; {i['age'] }; {i['postal_code'] }; {i['password']} ",
        html.br(),
        html.p(""),
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
        {"style": 
         {  "padding": "50px",
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "background_image":"url(https://brandonleon.neocities.org/demon.jpg.jpg)", 
            "background-size":"cover",
            "margin": "0px",
            "min-height": "700px",
            "min-width":"700px",
           }
           },
        
        ## creating form for submission0
    
        html.form(
            {"onsubmit": mysubmit},
               Card(
               CardConetent(
                Typography({
                    "variant":"h5",
                    "color":"secondary",
                    "style": {"padding": "10px","opacity":"50%"}
                },"Welcome to Anime World"))
            ),
             Card(
               CardConetent(
                Typography({
                    "variant":"h6",
                    "color":"darkblue",
                    "style": {"padding": "10px","opacity":"80%"}
                },"Anime has become a global phenomenon, and its popularity has skyrocketed in recent years. No matter how old you are or what background you grew up with, you can always find a good anime to watch. With 36% of viewers worldwide enjoying watching anime in 2021, according to Ampere Consumer data, free anime websites are snowballing as a result. Some are created to quench your thirst for anime, and some are there to break both your heart and bank account. Every anime enthusiast knows the pain of searching for safe and free anime websites to watch. We know it too, and we created Kaido to end it all.Welcome to Anime World"))
            ),
          
            html.input(
                {
                    "type": "test",
                    "placeholder": "name",
                    "valign":"middle",
                    "style": {"padding": "10px","margin":"1rem"},
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
             html.input(
                {
                    "type": "test",
                    "placeholder": "age",
                    "style": {"padding": "10px","margin":"1rem"},
                    "on_change": lambda event: set_age(event["target"]["value"]),
                }
            ),
             html.input(
                {
                    "type": "test",
                    "placeholder": "postal_code",
                    "style": {"padding": "10px","margin":"1rem"},
                    "on_change": lambda event: set_postal_code(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "password",
                    "style": {"padding": "10px","margin":"1rem"},
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            Button(
                { 
                    "type": "join",
                    "size":"medium",
                    "style": {"padding": "10px"},
                    "bold":"70",
                    "color":"primary",
                    "variant":"contained",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                },
                "join",
        
            ),
            
            html.input(
                {
                    "type": "test",
                    "value":nameedit,
                    "style":{"padding": "10px","margin":"2rem","display":"none" if is_edit.value == False else "block"},
                    "placeholder": "updatename",
                    "on_change": lambda event: set_nameedit(event["target"]["value"]),
                    
                },
               
            ),
            html.input(
                {
                    "type": "test",
                    "value":ageedit,
                    "style":{"padding": "10px","margin":"2rem","display":"none" if is_edit.value == False else "block"},
                    "placeholder": "updateage",
                    "on_change": lambda event: set_ageedit(event["target"]["value"]),
                    
                },
               
            ),
            html.input(
                {
                    "type": "test",
                    "value":postal_codeedit,
                    "placeholder": "updatepostal_code",
                    "style":{"padding": "10px","margin":"2rem","display":"none" if is_edit.value == False else "block"},
                    "on_change": lambda event: set_postal_codeedit(event["target"]["value"]),
                    
                },
               
            ),
            html.input(
                {
                    "type": "test",
                    "value":passwordedit,
                    "style":{"padding": "10px","margin":"2rem","display":"none" if is_edit.value == False else "block"},
                    "placeholder": "updatepassword",
                    "on_change": lambda event: set_passwordedit(event["target"]["value"]),
                    
                },
               
            ),
            
            Button(
                {
                    "type": "Update Guys",
                    "size":"small",
                    "style":{"padding": "10px","display":"none" if is_edit.value == False else "block"},
                    "color":"secondary",
                    "variant":"contained",
                    "on_click": event(
                        lambda event: savedata(event), prevent_default=True),
                },
                "Update Guys",
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
collection=db["newform"]

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
    postal_code = login_data["postal_code"]
    password = login_data["password"]
    # Create a document to insert into the collection

    document = {"name":username, "age":age, "postal_code":postal_code,"password": password}
    # logger.info("sample log messege")
    print(document)
    #Insert the docoument into the collection

    post_id = collection.insert_one(document).inserted_id #insert document
    print(post_id)
    print({"Login successful"})
def update(
    update_data: dict,

 ): # removed async, since await makes code  execution pause for the promise to resolve anyway. doesnt
    usernameedit = update_data["updatename"]
    ageedit = update_data["updateage"]
    postal_codeedit = update_data["updatepostal_code"]
    passwordedit = update_data["updatepassword"]
    # Create a document to insert into the collection

    updatedocument = {"updatename":usernameedit, "updateage":ageedit, "updatepostal_code":postal_codeedit,"udpatepassword": passwordedit}
    # logger.info("sample log messege")
    print(updatedocument)

    #Insert the docoument into the collection
    updatepost_id = collection.insert_one(updatedocument).inserted_id #insert document
    print(updatepost_id)

    print({"Updated successful"}) 

configure(app, MyCrud)
