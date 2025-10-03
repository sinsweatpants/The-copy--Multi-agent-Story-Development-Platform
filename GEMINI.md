# GEMINI.md

## Project Overview

This is a full-stack web application called "Jules" that serves as a master orchestrator for a complex story development process. The system utilizes a team of 11 specialized AI agents (powered by the Gemini Pro API) to analyze, develop, and challenge story ideas, resulting in a polished and production-ready story concept.

The project consists of two main parts:

*   **`jules-frontend`**: A React application built with Vite and written in TypeScript. It uses Zustand for state management and Tailwind CSS for styling.
*   **`jules-backend`**: A Node.js application built with Fastify and written in TypeScript. It uses Prisma as an ORM to interact with a PostgreSQL database and Redis for caching.

The entire application is containerized using Docker.

## Building and Running

The application can be run using Docker Compose.

### Backend

To run the backend and its dependencies (PostgreSQL and Redis), navigate to the `jules-backend` directory and run:

```bash
docker-compose up --build
```

### Frontend

To run the frontend, navigate to the `jules-frontend` directory and run:

```bash
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Development Conventions

### Backend

*   **Linting**: `npm run lint`
*   **Formatting**: `npm run format`
*   **Testing**: `npm run test`

### Frontend

*   **Linting**: `npm run lint`
*   **Formatting**: `npm run format`
*   **Type Checking**: `npm run type-check`
