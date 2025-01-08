# simple link shortener

## First run

Set up environment

```sh
python -m venv env
source env/bin/activate
pip install Flask
```

To create database, run in a python shell in project directory

```py
import app
app.init_db()
```

## Running

```sh
python app.py
```

## Using

### Creating short link

```sh
curl -X "POST" localhost:5000 -d "url=https://ref.snehit.dev/packaging/what-is-packaging.html"
```

This returns the shortcode and id.

```json
{
  "id": 84407458,
  "shortcode": "nqfily",
  "url": "https://ref.snehit.dev/packaging/what-is-packaging.html"
}
```

- `id` is required to later delete the short url
- `shortcode` is the actual route
  - eg. in this case, `http://127.0.0.1:5000/nqfily` will take you to `https://ref.snehit.dev/packaging/what-is-packaging.html`

### Deleting short link

With the id you get for short links you create, run this.

```sh
curl -X "DELETE" 127.0.0.1:5000 -d "id=84407458"
```

This returns either success or failure, depending on whether the id exists.

```json
{ "msg": "successfully deleted", "status": 200 }
```

```json
{ "msg": "forbidden", "status": 403 }
```
