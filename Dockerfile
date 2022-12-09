# python base image in the container from Docker Hub
FROM python:3.9

# set the working directory in the container to be /app
WORKDIR /app

# copy files to the /app folder in the container
COPY . /app

# install the packages from the Pipfile in the container
RUN pip3 install -r requirements.txt

# expose the port that uvicorn will run the app on
ENV PORT=8000
EXPOSE 8000

# execute the command python main.py (in the WORKDIR) to start the app
CMD ["python", "main.py"]