# Simple Socket Chat

Simple chat project, written in Python using sockets for college network class.

## Requirements

In order to run the project, you'll need to have Python 3.7.6 or greater, in case that you already have it you can go to next section: **Running the project**.
If you don't have it you can use [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) 
for download python and create your python environment for running the project.

I'm going to leave below a tutorial of how to configure your environment for running the project using `pyenv` with `pyenv-virtualenv`.

### Installing Python with `pyenv`

```bash
$ pyenv install 3.7.6
```

### Creating virtual environment

```bash
$ pyenv virtualenv 3.7.6 socketchat
```

### Using the virtual environment

```bash
$ pyenv activate socketchat
```

## Running the project

For running the project, you will need to have an server to receive and send messages to
clients that are connected, and at least 2 clients to see messages being broadcasted.

- Creating the server:

    If you are using Python 3.7.6 without `pyenv`, run the following command below to start 
    running server:
    ```bash
    $ python3 server.py
    ```

    If you are using `pyenv`, just run the following command to up the server:
    ```bash
    (socketchat) $ python server.py
    ```

- Creating clients:

    Now we are going to need two clients, in order to see each other message on terminal.

    If you are using Python 3.7.6 without `pyenv`, run the following command in two different
    terminals/bashes in order to create our clients and exchange messagens between them.
    ```bash
    $ python3 client.py
    ```

    Otherwise if you are using `pyenv`, simply run the following code in different terminals/bashes:
    ```bash
    (socketchat) $ python client.py
    ```

> If you are a client and want to quit from chat, simply write `quit` and you will be 
> disconnected from the chat.


### Short demo

![image](https://user-images.githubusercontent.com/73752036/160146135-bf0a6f2a-a138-40eb-9ee8-ca1dcddfc751.png)
![image](https://user-images.githubusercontent.com/73752036/160146205-7e34a7f7-7c8c-4ed3-b54e-bfcc68b56c9b.png)
![image](https://user-images.githubusercontent.com/73752036/160146258-debc879f-e484-4b0e-bb18-24ad95fc0ae1.png)
![image](https://user-images.githubusercontent.com/73752036/160146317-ad5925dc-71c4-48a1-a48d-83c3b9a8e1b0.png)
### File Uploading

![image](https://user-images.githubusercontent.com/73752036/160146416-ed6d3172-2067-43bd-a99b-5e5fcd1e06e9.png)



