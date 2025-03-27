# Use the official Python image from the Docker Hub
FROM python:3.11-alpine

# Set environment variables
ENV MCQUERY_API_URL=${MCQUERY_API_URL}
ENV MCQUERY_API_KEY=${MCQUERY_API_KEY}
ENV MCQUERY_API_KEY_HEADER=${MCQUERY_API_KEY_HEADER}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=server.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]