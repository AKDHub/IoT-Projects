# IoT-Projects

Welcome to Ali Kristian David Chehade's Github. The projects uploaded here are either projects I've done while studying to become an Internet of Things developer or personal ones. Each project is presented bellow with a short description of their funcionality.


# Python projects

## Datastructure
These projects focus on learning tests, sorting, search and recursive functions.


## Big Data

Python program that stores and displays quotes using a Redis database. The application fetches quotes from https://dummyjson.com/quotes and stores them. Users can retrieve a random quote from the database through the program. Additionally users are able to add their own quotes, which are then saved in the database. The project is modularized into separate Python files, such as init-db.py, get_quote.py, and add_quote.py, and also includes a simple menu system for user interaction.


## System Integration
# API Gateway

In this project, our group designed and implemented a distributed system that connects multiple independent components in a data pipeline. The goal was to simulate an electronic lock from an embedded device (arduino), transmit it through MQTT, and make it available to a client application via a REST API.

The system consists of the following main components:

* Embedded Device with keypad: A program running on an embedded system that reads a keypad and publishes it to an MQTT broker.

* MQTT Broker: We used HiveMQ as the MQTT broker to handle the communication between the publisher (sensor) and the subscriber (API server).

* API Server: A Flask application that subscribes to the MQTT topics, processes incoming data, and exposes it through a RESTful API.

* API Gateway (Apache APISIX): A ready-made gateway product was used to connect the client and the API server. It was configured to handle tasks such as caching, access and rate limiting.

* Client Application: A simple client that regularly requests data from the API and displays it.

This project involved both backend and embedded development, as well as system integration and configuration of third-party services. The result is a functional end-to-end system for an electronical lock.
