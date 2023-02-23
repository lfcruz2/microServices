# post-management/Dockerfile

FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Set virtual environment
RUN python3 -m venv venv

# Enable venv
ENV PATH="/venv/bin:$PATH"

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Labels
LABEL module="post-management"

# Set the environment variables
ENV PYTHONPATH="/app"
ENV FLASK_APP="app.py"
ENV FLASK_APP_NAME="user-management"
ENV RUNNING_IN_CONTAINER="True"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG="True"
ENV FLASK_TESTING="False"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="3001"

# .env variables for postgres (remove in cloud deployment)
ENV DB_NAME="monitor_posts"
ENV DB_HOST="posts_db"
ENV DB_PORT="5432"
ENV DB_USER="postgres"
ENV DB_PASSWORD="postgres"

# Expose the port the app will run on
EXPOSE 3001

# Run the command to start the app
CMD ["flask", "run"]