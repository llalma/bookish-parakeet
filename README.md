** Description
This repo is a solution to run a fibbonnaci number calculator using distributed processing using celery
 - There is a docker compose file which:
    - Runs fastapi on localhost:8000  running the main.py code
    - A redis instance
    - Celery running the tasks.py code
