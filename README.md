# FASTAPI APP
FastAPI STARTUP

## Setup APPLICATION

1. Create a virtual environment.
 ```sh
    python -m venv env
 ```
2. Activate virtual environment.
```sh
    source /path/to/venv/bin/activate`
```
3. Install project dependencies `pip install -r requirements.txt`


4. Start server.
 ```sh
 python management.py runserver 
```
 you could also specify the host and port to run 
 ```sh
 python management.py runserver ${host} ${port}
 ```

## **DATABASE SETUP**


**Starting the database**
run
```sh
python management.py makemigrations
```
run on cloning the repository and after making changes to the models also create a revision folder if it does not exist in the alembic directory

```

**review table data**

```bash
python management.py Hello

```


**Adding new tables and columns to models**

After creating new tables, or adding new models make sure to import the models in the alembic/env file then run python management.py makemigrations






