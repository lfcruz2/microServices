#!/bin/sh

echo "Waiting for users_db..."

while ! nc -z users_db 5432; do
  sleep 0.1
done

echo "PostgreSQL for users_db started"

flask run