#!/bin/sh

import os
import openai
import psycopg2
import psycopg2.extras
import uuid
import datetime
from datetime import datetime, timezone 

psycopg2.extras.register_uuid()
dt = datetime.now(timezone.utc)


openai.api_key = "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"

def generate_completion(model, prompt, temperature, max_tokens):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].text

generated_text = generate_completion(
    model="text-davinci-003",
    prompt="You are a highly creative poet. Make a 3 line poem",
    temperature=0.7,
    max_tokens=100
)

print("The generated poem is:")
print(generated_text)

#print(response)
#print("printed the response above, below is the completion")
#print(response.choices[0].text)



# Connect to your postgres DB
conn = psycopg2.connect("dbname=poems user=postgres host=localhost port=5432 password=raspberry")

def new_poem(generated_text):
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # set the current time
    dt = datetime.now(timezone.utc)
    # perfom an insert transaction
    insert = "INSERT INTO poetry values(uuid_generate_v4(),dt,generated_text)";
    # execute the insert on the cursor and commit it to the DB
    cur.execute(insert);
    conn.commit();


# Execute a select query
#cur.execute("SELECT * FROM poem")

# execute the insert using the new_poem function
print("now inserting the poem")
new_poem(generated_text);
print("insert successful")  

# close the connection
conn.close();