from flask import Flask, redirect
import sqlite3
import random, string

from flask import request

app = Flask(__name__)


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


@app.route("/<shortcode>", methods=["GET"])
def route(shortcode):
    print(shortcode)
    with sqlite3.connect("urls.db") as conn:
        query = "SELECT redirect FROM urls WHERE shortcode = ?"
        cur = conn.cursor()
        cur.execute(query, (shortcode,))
        url = cur.fetchone()

    if url:
        return redirect(url[0], code=302)
    else:
        r = {}
        r["status"] = 404
        r["msg"] = "record not found"
        return r, 404


@app.route("/", methods=["POST", "DELETE"])
def landing():
    if request.method == "POST":
        url = request.form.get("url")
        id = random.randint(0, 99999999)
        shortcode = randomword(6)
        with sqlite3.connect("urls.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO urls (id, shortcode, redirect) VALUES (?,?,?)",
                (id, shortcode, url),
            )
            conn.commit()
        r = {}
        r["shortcode"] = shortcode
        r["id"] = id
        r["url"] = url
        return r
    elif request.method == "DELETE":
        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        id = request.form.get("id")
        query = "SELECT redirect FROM urls WHERE id=?"
        cur.execute(query, (id,))
        url = cur.fetchone()
        if url:
            cur.execute("DELETE FROM urls WHERE id=?", (id,))
            conn.commit()
            conn.close()
            r = {}
            r["status"] = 200
            r["msg"] = "successfully deleted"
            return r, 200
        else:
            conn.close()
            r = {}
            r["status"] = 403
            r["msg"] = "forbidden"
            return r, 403

    else:
        return "unknown method"


def init_db():
    conn = sqlite3.connect("urls.db")
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()


if __name__ == "__main__":
    app.run()
