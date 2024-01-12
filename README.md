# Hydrolab Flask server

A Flask server to host our Systems Integration final project: a web application
where some LoRaWAN sensors will be connected. Demo available at
[hyrdolab.ericroy.net](https://hydrolab.ericroy.net) (at least at the time
of writing this).


## Installation in a production environment

The fastest and most reliable way to set up this project is using the Dockerfile
and docker-compose.

### docker-compose file

We recommend you to write a `docker-compose.yml` file
in the parent directory that looks like this:

```
version: '3.8'

services:
  web:
    build:
      context: ./hydrolab
      dockerfile: Dockerfile
    ports:
      - "3555:5000"
      - "3556:22"
    environment:
      - PRODUCTION=True
    volumes:
      - ./hydrolab_db:/hydrolab/app/hydrolab_db
      - ./production.py:/hydrolab/app/settings/production.py
```

Port 5000 is the web server. Port 22 is a ssh to access remotely the container
(since the sysadmin doesn't want its colleagues to access the host machine
because he's afraid :P). You can disable all the SSH related stuff without
compromising the project.

### Docker volumes

As you've seen in the docker-compose file, you will need to set up the
needed keys in `production.py`. You may want to use `get_vapid_keys.py` in
order to generate vapid keys. The other keys are pretty generic and can be
easily found by googling some tutorials.

**Reminder:** If you just want the basic app services
you don't need to set up any key (mails and notifications will not work but
everything else will).

To set up the basic database you can use `db_init.py`.

### Nginx configuration

A reverse proxy is highly recommended. We used nginx. To replicate our
environment, install nginx and create a file at
`/etc/nginx/sites-available/hydrolab.ericroy.net`:

```
server {

    listen 80;
    server_name hydrolab.ericroy.net;

    location / {
        proxy_pass http://localhost:3555;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

}
```

Then create a link to sites-enabled:

```sh
ln -s /etc/nginx/sites-available/hydrolab.ericroy.net /etc/nginx/sites-enabled
```

Then test the nginx configuration with `nginx -t` and if no errors are
reported restart nginx with `systemctl reload nginx`.

### HTTPS setup with certbot

To set up https we recommend to follow
[this tutorial](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-11).
It uses Certbot and Let's Encrypt. It's pretty straightforward, try it!

### Scheduled tasks

Some notifications and tasks aren't executed in requests and must be executed
periodically. That's why we recommend setting up a `crontab` event looking like
this one:

```
0 * * * * docker exec hydrolab_web_1 python3 hourly_activity_checker.py
```

## Manual installation (for developing)

The manual installation is a little tedious due to the number of dependencies
of this project. Thus, we recommend only doing it if you really need to
contribute to this project.

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
