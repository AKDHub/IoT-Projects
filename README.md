# IoT-Projects

Welcome to Ali Kristian David Chehade's Github. The projects uploaded here are either projects I've done while studying to become an Internet of Things developer or personal ones. Each project is presented bellow with a short description of their funcionality.



## Python projects

### - Datastructure
These projects focus on learning tests, sorting, search and recursive functions.


### - Cloud
This project is designed to create a cloud-based study forum application using Python and Flask. A docker container is created and was hosted on Azure for access to the webclient.



### - Big Data

Python program that stores and displays quotes using a Redis database. The application fetches quotes from https://dummyjson.com/quotes and stores them. Users can retrieve a random quote from the database through the program. Additionally users are able to add their own quotes, which are then saved in the database.



### - System Integration
#### API Gateway

In this project, our group designed and implemented a distributed system that connects multiple independent components in a data pipeline. The goal was to simulate an electronic lock from an embedded device (arduino), transmit it through MQTT, and make it available to a client application via a REST API.

The system consists of the following main components:

* Embedded Device with keypad: A program running on an embedded system that reads a keypad and publishes it to an MQTT broker.

* MQTT Broker: We used HiveMQ as the MQTT broker to handle the communication between the publisher (sensor) and the subscriber (API server). Message are encrypted in Base64, while not exactly secure, was more to show that the option and undestanding of encryption exists.

* API Server: A Flask application that subscribes to the MQTT topics, processes incoming data, and exposes it through a RESTful API.

* API Gateway (Apache APISIX): A ready-made gateway product was used to connect the client and the API server. It was configured to handle tasks such as caching, access and rate limiting.

* Client Application: A simple GUI Client built int TKinter.

This project involved both backend and embedded development, as well as system integration and configuration of third-party services. The result is a functional end-to-end system for an electronical lock.


#### Radioguiden

The goal of this project was to learn how to interact with a JSON-based API and develop a Python program to retrieve and present data to the user.

In this assignment, a Python application was created that connects to the public Sveriges Radio API. The program allows the user to easily access information from Sveriges Radio through a simple and interactive menu system.

The user is first presented with a list of available radio channels. After selecting a channel, the program fetches and displays the current program schedule (tablå) for that channel, providing a clear overview of what's being broadcast.

This project provided hands-on experience with API consumption, JSON handling in Python, and building a basic interactive interface.



### - Service Design

This project is a simple Flask API for reviewing Swedish coffee products. It features database initialization, web scraping for coffee data, and user review functionality. The system stores product data in JSON and manages users and reviews via SQLite.



## C++ Projects

### - Inbyggda System Labb 4

A digital combination lock with servo control. This program implements a secure digital combination lock system using an Arduino. At startup, the system indicates a locked door with a red LED. When the correct 4-button combination is entered, the red LED turns off, the green LED lights up, and a servo rotates to simulate unlocking the door. After a few seconds, the system automatically relocks, reversing the servo and returning the LED state.

The program continuously monitors the last four button presses allowing the door to be unlocked regardless of previous inputs. A dedicated programming button allows the user to set a new combination which is saved in non-volatile memory, ensuring it persists even after a restart.


### - Inbyggda System Inlämning 2

A small program that sorts currencies and presents them from a .txt file.

