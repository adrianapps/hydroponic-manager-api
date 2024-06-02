# Hydroponic System Manager
Simple API build with Django and DRF for managing hydroponic systems

## How to run the application
- create a virtual environment and run  
    ```
    pip install -r requirements.txt
    ```
- enter postgresql shell  
    ```
    sudo -u postgres psql
    ```
- setup your postgresql database
    ```sql
    CREATE DATABASE your_db_name;
    CREATE USER your_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
    ```
- create .env file containing postgresql settings
    ```env
    POSTGRES_DB='your_db_name'
    POSTGRES_USER='your_user'
    POSTGRES_PASSWORD='your_password'
    POSTGRES_HOST='localhost'
    POSTGRES_PORT='5432'
    ```
- run the application with  
    ```
    python manage.py runserver
    ```
  
## Directories
- `config`  
    main project directory
- `systems`  
    app responsible for CRUD operations on hydroponic systems and measurements

## Endpoints
- ### `api/` 
    - `/`
         - GET : api root
    - `register/`
         - POST : create a user   
    - `hydroponic-systems/`
        - GET : list of user's systems
        - POST : create a system
    - `hydroponic-systems/<slug:slug>/`
        - GET : the details of user's hydroponic system
        - PUT : update your hydroponic system
        - DELETE : delete your hydroponic system
    - `measurements/`
        - GET : list of user's measurements
        - POST : create a measurement for your system
    - `measurements/<int:pk>/`
        - GET : the details of user's measurement
        - PUT : update your measurement
        - DELETE : delete your measurement
- ### Other Endpoints
    - `/admin/`
        - Django Admin Interface
    - `/api-auth/`
        - DRF Authentication Interface
