# Hydrolab Flask server


## Easy start using Docker


```
```

## Manual installation


### Prerequisites

- Python 3.6 or higher installed:

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3
```

- Node 14 or higher with npm 6.14 or higher:

```
sudo apt install nodejs npm
```

- Sqlite3
```
sudo apt install sqlite3
```

### Install dependencies

Change directory to project base path and run:

```
python3 -m pip install -r requirements.txt
npm install
```

### Set up database

Again, from the same project directory. It will create 2 test users:

- Super User: root@root
- Normal User: user@user

Both users have the same password: `root12.$`.

```
python3 db_init.py
```

### Compile CSS

Run each time you change something tailwind-related:

```
npm run create-css
```

If you want it to automatically recompile all CSS every time a file changes, run `npm run create-css-forever` instead.

### Compile translations

Every time you translate something, you need to run these two commands:

```
pybabel extract -F app/babel.cfg -o app/translations/messages.pot --input-dirs=app
pybabel update --input-file=app/translations/messages.pot --output-dir=app/translations
```

And then, in each language file, fill the missing translations. Once
done, compile them and restart the server:

```
pybabel compile -f -d app/translations
```

### Run

Simple! Just go to the project folder and type:

```
python3 app.py
```

Run `python3 app.py --listen-all` if you wish to accept TCP
connections from other IP addresses than localhost.

Have the environment variable `export PRODUCTION=True` to run in a production
server (without the debug mode, for example).
