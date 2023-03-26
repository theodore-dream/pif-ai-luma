import os
import datetime
import random
import string

## create a function that generates a random string made of 10 letters and numbers

def random_string():
    letters_and_numbers = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_numbers) for i in range(10))
    return random_string

## create a function that writes a text file to the new directory with the current date and time as the filename 
## and the random string as the contents 

def write_file(string):
    now = datetime.datetime.now()
    new_file = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(new_file)
    with open(file_path, "w") as f:
        f.write(random_string())



create_txt()