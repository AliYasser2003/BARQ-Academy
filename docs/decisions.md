# Technical Decisions

This file explains some of the main choices I made while working on the BARQ project.

## 1. Using Docker Compose

I used Docker Compose to run the application, NGINX, PostgreSQL, and Redis together.

This made it easier to start and manage all the services from one place instead of running each container manually.

## 2. Using NGINX

I used NGINX as the entry point for the application.

Instead of accessing each Flask application directly, requests go through NGINX, which forwards them to the application instances.

This also allowed me to test what happens when one application instance stops working.

## 3. Separating the networks

I separated the frontend and backend networks.

NGINX and the application containers use the frontend network, while PostgreSQL and Redis are kept on the backend network.

I also removed the host ports for PostgreSQL and Redis because they do not need to be accessed directly from outside the Docker environment.

## 4. Keeping PostgreSQL data persistent

I used a named Docker volume for PostgreSQL data.

This was important because I needed the database records to remain available after recreating the PostgreSQL container.

I tested this by creating a record, recreating the containers, and checking that the record was still there.

## 5. Adding backup and restore scripts

I created `backup.sh` to create a database backup and check that the backup file was valid.

I also created `restore.sh` to restore a backup into a separate test database.

This allowed me to test the restore process without replacing the original database.

## 6. Using environment variables

I moved the database and Redis connection settings into environment variables.

I used a local `.env` file and added `.env.example` so the required settings could be understood without sharing the actual values.

The local `.env` file is excluded from Git.

## 7. Adding health checks and resource limits

I added health checks for the application and database services so I could check whether they were ready.

I also configured CPU and memory limits for the containers.

These settings helped me test the environment more reliably and avoid leaving the services without resource limits.

## 8. Adding GitHub Actions

I added a GitHub Actions workflow to validate the project.

The workflow checks out the repository, validates the Docker Compose configuration, builds and starts the services, and runs the validation script.

I checked that the workflow completed successfully.

## Limitations

This project runs on one host using Docker Compose. It helped me practise containerization, networking, persistence, testing, and CI, but it does not provide full production high availability.
