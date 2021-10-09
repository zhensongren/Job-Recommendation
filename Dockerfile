# Use latest Python runtime as a parent image
FROM python:3.7-slim-buster

# Meta-data
LABEL maintainer="Zhensong Ren <zhensong.ren@gmail.com>" \
      description="Indeed job description classification API\
      This image contains a pickled version of the predictive model\
      that can be accessed using a REST API (created in Flask).\
      Fitting and pickling was done at another point in the process"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt into the container at /app
COPY ./requirements.txt /app/tmp/

# pip install
RUN pip --no-cache-dir install -r /app/tmp/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port available to the world outside this container
EXPOSE 5000

VOLUME /app

# ENTRYPOINT allows us to specify the default executible
ENTRYPOINT ["python"]

# CMD sets default arguments to executable which may be overwritten when using docker run
CMD ["app.py"]

### docker build -t indeed-job-flask .
### docker run -p 5000:5000 --name indeed-job-flask indeed-job-flask
