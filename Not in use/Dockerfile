# Use the official Ubuntu base image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl software-properties-common

# Install Node.js (including npm)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Install create-react-app globally
RUN npm install -g create-react-app

# Copy your application code to the container (assuming your application is in the current directory)
COPY . .

# Install your application's dependencies
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run your application
CMD ["npm", "start"]

