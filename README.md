# Django Feeds - Backend Engineer Challenge

## Setup and running server

You must first create a dotenv file `.env` in the project directory, the file should contain following variables:

```
DJANGO_SECRET=<django_secret_key>
DEBUG=True
LIST_PER_PAGE=10
POSTGRES_DB=<postgres_db>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
DATABASE_URL=psql://<postgres_user>:<postgres_password>@db:5432/<postgres_db>
```

Either type each commands respectively in the `startserver.sh` file in the scripts folder or run the script with the following command in the project directory to setup database and start the server:

```
./scripts/startserver.sh
```

After that, you need to create a super user account to access admin dashboard by following command:

```
./scripts/compose.sh run web python manage.py createsuperuser
```

Just follow the instruction to create your own super user credentials.

That's it, you can check the server up and running in your local machine.

## Shutdown the container

Type the following command in your terminal to clean up the containers:

```
docker-compose down
```

## Usage

### 1. Grab all items in feed URLs

In order to grab all items from given feed URLs, you can use the following command:

```
./scripts/compose.sh run web python manage.py grabfeeds https://www.feedforall.com/sample-feed.xml,https://www.feedforall.com/blog-feed.xml
```

Note: The urls must be separated by a comma, the items will then be printed on the terminal.

### 2. Configure pagination value

You can easily configure the pagination value by adding the following variable in your `.env` file:

```
LIST_PER_PAGE=10
```

### 3. Items/Categories CRUD

In order to make any operations manually to items and categories, you can use the super user credentials to login the admin site `http://localhost:8000/admin` on your local machine and make actions. You can also search the items based on category title by using the search bar inside the `Items` navigation menu item.

### 4. Run Unit Tests

In order to run unit tests, you can use the following command:

```
./scripts/compose.sh run web python manage.py test feeds
```

## Troubleshooting

If you are facing any problems while running any scripts, for example a permission error, you can easily grant the permission for the script by typing the following command:

```
chmod 744 scripts/startserver.sh
```
