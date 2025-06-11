# Orders API

This is a simple FastAPI-based Orders API that allows you to create, retrieve, update, delete, and convert orders between currencies. The app uses PostgreSQL as the database and supports real-time currency conversion via an external API: [text](https://currencyapi.com/docs).

## Features
- Create, read, update, and delete orders
- Store customer name, price, and currency for each order
- Convert order prices to different currencies on the fly
- OpenAPI/Swagger documentation available

## Running the App

1. Make sure you have Docker and Docker Compose installed.
2. Start the app and database with:

   ```sh
   docker compose up -d
   ```

3. The API will be available at: [http://localhost:8000](http://localhost:8000)
4. Interactive API docs are available at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (set automatically by Docker Compose)
- `EXCHANGE_API_KEY`: API key for the currency conversion service (can be set in your environment or .env file, the one used is a free API key generated for the purpose of this project)


---
