# Django My Blog Site

## Stack

- Python 3.8 or above
- Django 4 framework
- SQLite 3
- Flake8 and isort for linting and formatting

## Usage

1. Start the server: `python manage.py runserver` and go to `http://127.0.0.1:8000`
2. Read articels and add them to the reading list
3. Write comments to the articles.
4. Create an admin user in Django and write posts: `http://127.0.0.1:8000/admin/`
    - Set tags, authors, description, image.
    - Manage the components in the admine pane.
    - Precreated user (username, password): `John`, `jdoe1234`

The SQLite DB is prepopulated with some posts, comments, tags and an admin user for convenience.
DEBUG is still set to True, for ease of playing with it.
