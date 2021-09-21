FROM python:3.9.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for project in the container
RUN mkdir /task_TrackP

# Set the working directory to /task_Track
WORKDIR /task_TrackP

# Copy the current directory contents into the container at /task_Track
ADD . /task_TrackP/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt