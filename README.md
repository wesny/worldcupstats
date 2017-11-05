# worldcupstats

#### Setup local requirements

- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`

#### Setup Local DB

- Create a local db using `createdb worldcupstats_local`
- Run `export DATABASE_URL="postgresql://localhost/worldcupstats_local"` to set the local variable
- `python manage.py db upgrade`

#### Database commands

- Whenever you make a database change, run `python manage.py db migrate` and commit.
- Then run `heroku run python manage.py db upgrade --app worldcupstats` after the commit clears.