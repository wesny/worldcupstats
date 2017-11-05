# worldcupstats


#### Database commands

- Whenever you make a database change, run `python manage.py db migrate` and commit.
- Then run `heroku run python manage.py db upgrade --app worldcupstats` after the commit clears.