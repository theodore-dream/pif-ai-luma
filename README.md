# Pif

This project is a hardware device that displays poetry that is generated through a series of API calls to gpt-3.5-turbo. 

High-level, this application gathers and displays poetry and text data. The repository provides Dockerfiles to run both the Postgres database and the client side with the application 'Poem-App'

This project uses a Raspberry Pi zero running Raspbian and a small 128x128 waveshare display. 

Project is named Pif for Poetry Friend

Poem-App python scripts explanation:
 - init-postgres-pif.py initializes the postgres database and creates a database "game" with a table "poem_game" using psycopg2 driver
 - main.py is the main script that creates game instances and writes and reads from the database to manage game state 
 - intro_vars module contains introductory text snippets that are displayed in new game instances only 
 - poem_gen.py module is the main poetry/text generation module that has a series of pipelines of API calls to gpt-3.5-turbo
 - display_write_poem.py writes to hardware display using PIL 

