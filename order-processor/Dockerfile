# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 5001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./order-processor/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
RUN pwd
RUN echo "$PWD"
ENV FLASK_APP=order-processor/app.py
#CMD ["python", "./order-processor/app.py"]
#CMD [ "python", "app.py", "flask", "run", "-h", "0.0.0.0", "-p", "5001" ]
CMD [ "flask", "run", "-h", "0.0.0.0", "-p", "5001" ]
