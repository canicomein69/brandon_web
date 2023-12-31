
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state,web
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient



@component
def MyCrud():
    ## Creating state
    alltodo = use_state([])
    full_name, set_full_name = use_state("")
    age, set_age = use_state("")
    postal_code, set_postal_code = use_state("")
    password, set_password = use_state("")
    is_edit = use_state(False)
    full_nameedit, set_full_nameedit = use_state("")
    ageedit, set_ageedit = use_state("")
    postal_codeedit, set_postal_codeedit = use_state("")
    passwordedit, set_passwordedit = use_state("")
    id_edit = use_state(0)
    edittodo =  use_state([])
    mui = web.module_from_template(
    "react",
    "@mui/material"
    
    )
    #using react UI components to better style
    Button = web.export(mui,"Button")
    Card = web.export(mui,"Card")
    CardConetent = web.export(mui,"CardContent")
    Typography = web.export(mui,"Typography")
    
    def mysubmit(event):
        newtodo = {"full_name": full_name, "age":age , "postal_code":postal_code , "password": password}
        # push this to alltodo

        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data
       # looping data from alltodo to show on web

    #creating delete and edit function to make adjustment in submited data
    def deletebtn(b):
        is_edit.set_value(True)
        for i,x in  enumerate(alltodo.value):
            if i == b:
                x['full_name'] = full_nameedit
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
                set_full_nameedit(x['full_name'])
                set_ageedit(x['age'])
                set_postal_codeedit(x['postal_code'])
                set_passwordedit(x['password'])
                id_edit.set_value(b)
    def savedata(event):
        for i,x in enumerate(alltodo.value):
            if i == id_edit.value:
                x['full_name'] = full_nameedit
                x['age'] = ageedit
                x['postal_code']= postal_codeedit
                x['password'] = passwordedit
        is_edit.set_value(False)    
        set_full_nameedit("")
        set_ageedit("")
        set_postal_codeedit("")
        set_passwordedit("")

        updatetodo = {"updatefull_name": full_nameedit, "updateage": ageedit, "updatepostal_code":postal_codeedit, "updatepassword" : passwordedit}
        edittodo.set_value(edittodo.value + [updatetodo])
        update(updatetodo)#function call to update function using the updated data
        # getting updated data from edittodo to show on web

    #making adjustment with submited data
    list = [
        html.li(
            {
              "key":b,
              "style":{"font-size": "25px","font-family":"Copperplate","background-color":"white"},
            },
            f"{b} => {i['full_name']} ; {i['age'] }; {i['postal_code'] }; {i['password']}, ",
        Button({
            "color":"secondary",
            "variant":"contained",
            "on_click":lambda event, b=b:deletebtn(b)
            },"delete"),
        html.br(),
        Button({
            "color":"secondary",
            "variant":"contained",
            "on_click":lambda event, b=b:editbtn(b)
            },"edit"),
            )
            for b, i in enumerate(alltodo.value)
            
    ]
    def handle_event(event):
        print(event)
    
    return html.div(
        {"style": 
         {  
            "padding":"15px",
            "background-repeat":"no-repeat",
            "background-attachment":"fixed",
            "background-size":"cover",
            "flex-wrap": "wrap",
            "background_image":"url(https://brandonleon.neocities.org/17169622.png)",
            
           }
           },
        
        ## creating form for submission
    
        html.form(
          html.b(html.h1(
                    {"style": {"font-family": "	Copperplate",
                                "font-size": "40px",
                                "letter-spacing":"4px",
                                "text-shadow":"0 0 3px black",
                                "border":"8.5px Black",
                                "border-radius": "20px",
                                "opcaity":"50%",
                                "flex-wrap": "wrap",
                                "background-color":"hsla(120, 100%, 25%, 0.3)",
                                "background-opacity":"50%",
                                "padding": "15px 25px",
                                "border-style": "outset",
                                "box-sizing": "border-box",
                                "color":"white"}}
                    ,"Welcome to Anime World",)),
                html.br(),
            
            html.p(Card({"style": {"padding": "10px 15px","opacity":"70%","font-size": "50px","background-color":"rgba(255, 0, 0, 50)","box-shadow":"5px 10px","font-weight":"900"}},
                        CardConetent(
                            Typography({
                                       "variant":"h5",
                                       "color":"Black",
                                       
                    
                },"Anime has become a global phenomenon, and its popularity has skyrocketed in recent years. No matter how old you are or what background you grew up with, you can always find a good anime to watch.With 36% of viewers worldwide enjoying watching anime in 2021, according to Ampere Consumer data, free anime websites are snowballing as a result. Some are created to quench your thirst for anime, and some are there to break both your heart and bank account. Every anime enthusiast knows the pain of searching for safe and free anime websites to watch. We know it too, and we created Kaido to end it all.Welcome to Anime World"),
            ))),
           
            html.input(
                {
                    "type": "test",
                    "placeholder": "full_name",
                    "style": {"padding": "10px","margin":"1rem", "border-radius": "15px"},
                    "on_change": lambda event: set_full_name(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "age",
                    "style": {"padding": "10px","margin":"1rem", "border-radius": "15px"},
                    "on_change": lambda event: set_age(event["target"]["value"]),
                }
            ),
            html.br(),
            html.input(
                {
                    "type": "test",
                    "placeholder": "postal_code",
                    "style": {"padding": "10px","margin":"1rem", "border-radius": "15px"},
                    "on_change": lambda event: set_postal_code(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "password",
                    "style": {"padding": "10px","margin":"1rem", "border-radius": "15px"},
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            Button(
                { 
                    "type": "join",
                    "size":"medium",
                    "style": {"padding": "10px"},
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
                    "value":full_nameedit,
                    "style":{"padding": "10px","margin":"1rem","display":"none" if is_edit.value == False else "block", "border-radius": "15px"},
                    "placeholder": "updatefull_name",
                    "on_change": lambda event: set_full_nameedit(event["target"]["value"]),
                    
                },
               
            ),
            html.input(
                {
                    "type": "test",
                    "value":ageedit,
                    "style":{"padding": "10px","margin":"1rem","display":"none" if is_edit.value == False else "block", "border-radius": "15px"},
                    "placeholder": "updateage",
                    "on_change": lambda event: set_ageedit(event["target"]["value"]),
                    
                },
               
            ),
            
            html.input(
                {
                    "type": "test",
                    "value":postal_codeedit,
                    "placeholder": "updatepostal_code",
                    "style":{"padding": "10px","margin":"1rem","display":"none" if is_edit.value == False else "block", "border-radius": "15px"},
                    "on_change": lambda event: set_postal_codeedit(event["target"]["value"]),
                    
                },
               
            ),
            html.input(
                {
                    "type": "test",
                    "value":passwordedit,
                    "style":{"padding": "10px","margin":"1rem","display":"none" if is_edit.value == False else "block", "border-radius": "15px"},
                    "placeholder": "updatepassword",
                    "on_change": lambda event: set_passwordedit(event["target"]["value"]),
                    
                },
               
            ),
            
            Button(
                {
                    "type": "Update Guys",
                    "size":"small",
                    "style":{"padding": "10px","display":"none" if is_edit.value == False else "block"},
                    "color":"primary",
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


#copy and paste the mongo DB URI 
uri="mongodb+srv://Brandonweb:brandon123@cluster0.miqe39j.mongodb.net/?retryWrites=true&w=majority"
client= MongoClient (uri, server_api=ServerApi("1"))  #camel case

#defining the Db name

db= client ["web"]
collection=db["anime"]

#checking the connection
try:
    client.admin.command("Ping")
    print("Successfully Connected MongoDB")
except Exception as e:
    print(e)

def login(
    login_data: dict,

 ): # removed async, since await makes code  execution pause for the promise to resolve anyway. doesnt
    
    username = login_data["full_name"]
    age = login_data["age"]
    postal_code = login_data["postal_code"]
    password = login_data["password"]
    # Create a document to insert into the collection

    document = {"full_name":username, "age":age, "postal_code":postal_code,"password": password}
    # logger.info("sample log messege")
    print(document)
    #Insert the docoument into the collection

    post_id = collection.insert_one(document).inserted_id #insert document
    print(post_id)
    print({"Login successful"})

    #creating update statement to make appear the updated data
def update(
    update_data: dict,

 ): # removed async, since await makes code  execution pause for the promise to resolve anyway. doesnt
    usernameedit = update_data["updatefull_name"]
    ageedit = update_data["updateage"]
    postal_codeedit = update_data["updatepostal_code"]
    passwordedit = update_data["updatepassword"]
    # Create a updatedocument to insert into the collection

    updatedocument = {"updatefull_name":usernameedit, "updateage":ageedit, "updatepostal_code":postal_codeedit,"udpatepassword": passwordedit}
    # logger.info("sample log messege")
    print(updatedocument)

    #Insert the updatedocoument into the collection
    updatepost_id = collection.insert_one(updatedocument).inserted_id #insert document
    print(updatepost_id)

    print({"Updated successful"}) 

configure(app, MyCrud)
