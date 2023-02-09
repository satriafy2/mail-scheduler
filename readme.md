## Mail Scheduler

Another mini project using python flask framework to send email using scheduler


### Installation

1. Make sure you have `python3.8` or later

2. For the database install `MySQL 8.0` or later. Then create new database named `db_email`, or you can name it something else and adjust the configuration later.

3. Make a new python environment(and activate it), then install all dependencies from `requirements.txt` using command below
```
pip install -r requirements.txt
```
4. Rename `.env.example` to `.env` and adjust it's environment value depends on your machine

5. Migrate database, run the following command
```
flask db upgrade
```
6. Go to the root project, and run the app using the following command
```
flask --app app run --host=0.0.0.0
```



### API

#### POST /save_emails
Create new email and schedule it to send at `timestamp` value

Request body:
```
{
    "email_subject": "string",
    "email_content": "string",
    "timestamp": "2023-02-09 19:39:00",
    "recipient": {
        "name": "string",
        "email": "john@email.com"
    }
}
```