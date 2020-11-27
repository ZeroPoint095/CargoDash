# CargoDash Usage Guide
This document will help you to understand to make use of CargoDash. CargoDash is written in Python code (version 3.8.5). For any questions please for free to create an issue.

## Python Requirements

    aiohttp v3.7.3
    canopen v1.1.0
    can v3.3.4
    numpy 1.19.4
    

## Introduction
CargoDash is a tool that listen to incoming messages and sets the values of these messages into user-defined nodes.  The values of these nodes can be requested with CargoDash's API.  Besides this it logs all raw incoming messages in a buffered logger. The logger can be requested to log all messages inside the buffer on command. For example, you can request the buffer on a dangerous event or when the user wants it.  

## API

#TODO: create interface for API