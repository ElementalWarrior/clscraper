# CL Scraper
A scraper I am creating with intention to create a dataset of rental and property values by region. With impunity on the lower mainland.

## Notes

### Tests
I am trying to have the tests be independent of db state. The best way to ensure I don't have tests that accidentally use my local db that is in use when debugging, I set the project name to `clscraper_test`.

This basically creates all different containers (and maybe images) from the standard project that docker creates (based off of the folder name that `docker-compose.yml` resides in).

So I have a helper script to run tests `bin/runtests` which uses the project name when calling `docker-compose`. So if I need to clean out the volumes I need to make sure to run `docker-compose -p clscraper_test`.

### Alembic
I am storing alembic outside of the clscraper package, this makes sense to me to disconnect db state management from the scraper domain code, however by doing so if I try to run the alembic script I end up creating `__pycache__` everywhere. In order to avoid this I am using a helper script `bin/alembic` that runs `python -B`. The -B prevents cache file creation.

### ./Vendor

By creating a directory with all the python liraries inside it inside my repo folder, I can use goto definition with vscode. This is helpful because I often end up reading the source code of libraries used to understand library processes.