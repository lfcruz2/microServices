# user-management/Dockerfile

FROM python:3.10-slim-buster

# Install netcat and system updates
RUN apt-get update && apt-get install -y netcat

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

# Adding the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Labels
LABEL module="user-management"

# Flask environment variables
ENV PYTHONPATH="/app"
ENV FLASK_APP="app.py"
ENV RUNNING_IN_CONTAINER="True"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG="True"
ENV FLASK_TESTING="False"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="3000"

# .env variables for postgres (remove in cloud deployment)
ENV DB_NAME="monitor_users"
ENV DB_HOST="users_db"
ENV DB_PORT="5432"
ENV DB_USER="postgres"
ENV DB_PASSWORD="postgres"

# Expose the port the app will run on
EXPOSE 3000

# Run server from entrypoint script
CMD ["./entrypoint.sh"]