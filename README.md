# Hydroponic System Manager
Simple API built with Django and DRF for managing hydroponic systems.

## Table of Contents
1. [How to Run the Application](#how-to-run-the-application)
2. [Directories](#directories)
3. [Endpoints](#endpoints)

## How to Run the Application

1. **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Enter PostgreSQL shell**:
    ```bash
    sudo -u postgres psql
    ```

3. **Set up your PostgreSQL database**:
    ```sql
    CREATE DATABASE your_db_name;
    CREATE USER your_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
    ```

4. **Create a `.env` file with PostgreSQL settings**:
    ```env
    POSTGRES_DB='your_db_name'
    POSTGRES_USER='your_user'
    POSTGRES_PASSWORD='your_password'
    POSTGRES_HOST='localhost'
    POSTGRES_PORT='5432'
    ```

5. **Run migrations and start the application**:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Directories

- **`config`**:
    Main project directory.
- **`systems`**:
    App responsible for CRUD operations on hydroponic systems and measurements.

## Endpoints

### `api/`

- `/`:
    - **GET**: API root.
- `register/`:
    - **POST**: Create a user.

- **`hydroponic-systems/`**:
    - **GET**: List of user's hydroponic systems.
    - **POST**: Create a  hydroponic system.

- **`hydroponic-systems/<slug:slug>/`**:
    - **GET**: Details of user's hydroponic system.
    - **PUT**: Update your hydroponic system.
    - **DELETE**: Delete your hydroponic system.

- **`measurements/`**:
    - **GET**: List of measurements for user's hydroponic systems.
    - **POST**: Create a measurement for your hydroponic system.

- **`measurements/<int:pk>/`**:
    - **GET**: Details of user's measurement.
    - **PUT**: Update your measurement.
    - **DELETE**: Delete your measurement.

### Other Endpoints

- `/admin/`:
    - Django Admin Interface.
- `/api-auth/`:
    - DRF Authentication Interface.
