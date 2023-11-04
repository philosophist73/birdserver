# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.6-bullseye

# Copy the source files into the container
WORKDIR /flask-docker
COPY . /flask-docker

# Install pip requirements
RUN pip3 install virtualenv
RUN python3 -m venv web-app 
RUN . web-app/bin/activate
RUN python3 -m pip install -r requirements.txt

EXPOSE 5000
ENV PORT 5000
ENV PYTHONUNBUFFERED 1

# Define the command to be run when the container is started
CMD exec gunicorn --bind :$PORT app.main:gunicorn_app --workers 1 --threads 2 --timeout 0