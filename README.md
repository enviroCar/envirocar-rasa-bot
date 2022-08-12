<h1 align="center">enviroCar Rasa Bot</h1>
<p align="center">A bot for <a href="https://github.com/enviroCar/enviroCar-app">enviroCar android application</a> part of Google Summer of Code 2022 project: <a href="https://summerofcode.withgoogle.com/programs/2022/projects/xXN12jAU">voice command</a>.</p>

## 👇 Prerequisites

Before installation, please make sure you have already installed the following tool:

- [``pipenv``](https://pypi.org/project/pipenv/)  
```
pip install pipenv
```
We will use pipenv to easily manage and setup a working environment. 

## 🛠️ Installation Steps
Once you have cloned the project follow these steps to install:

- Initialize a virtual environment and install dependencies via **use pipenv**

```
cd envirocar-rasa-bot
pipenv install
```

## 🧑‍💻 Training and Testing
- Train bot
```
rasa train
```
- Test bot on terminal
```
rasa shell
```
- start ``rasa server`` and test locally
```
rasa run --enable-api --port 5005
```
- start `actions` server
```
rasa run actions -p 5055
```
Once the server is up and running, test the bot directly via [``postman``](https://www.postman.com/)  
Here's a [blog to explore the ``rasa`` apis with postman](https://rasa.com/blog/explore-rasa-apis-with-postman/)

But here are some of the common apis to use:

1. Testing the bot  
Send a `POST` request to a particular channel http://localhost:5005/webhooks/<channel_name>/webhook with the body.
This project provides 2 channels.<br/>   
a. `rest` channel  
<br/>This Channel is given by the rasa itself, and we cannot add extra functionalities to it. E.g. We cannot send extra data like `metadata` in the request.<br/>    
b. `envirocar` channel  
<br/>This Channel is a custom channel created to use the extra functionalities and send extra data like `metadata` or some `credentials` in the request.<br/>  
Learn more about the [Custom Channels from here](https://www.google.com/search?q=custom+channel+rrasa&oq=custom+channel+rrasa&aqs=chrome..69i57.6391j0j1&sourceid=chrome&ie=UTF-8)
```
{
    "message": <your message>
}
```

2. Check rasa version
A `GET` request to http://localhost:5005/version without the body.

You could also explore the [apis with postman via video](https://www.youtube.com/watch?v=usHTraJTPyQ&list=PL75e0qA87dlHogEVKnBJLhqyaZKDg2f0W).  
