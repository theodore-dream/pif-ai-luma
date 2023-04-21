FROM python:latest

# Set api key
ARG stability_diffusion_api_key

# install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --upgrade transformers 

# copy app script
COPY pipeline.py /app/pipeline.py

# Copy the application files
COPY run.sh /app/run.sh

# Start the application
RUN ["chmod", "+x", "/app/run.sh"]
CMD ["/app/run.sh"]

