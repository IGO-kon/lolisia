import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = "sunabaco"
# @app.route("/temptest")
# def temptest():

#     name = "びしょうじょ"
#     age = 18
#     address = "ひみつ♡"
#     return render_template("index.html", name=name, age=age, address=address)

# @app.route("/weather")
# def weather():

#     weather = "はれ"
#     return render_template("weather.html", weather=weather)

# @app.route("/dbtest")
# def dbtest():
#     conn = sqlite3.connect("flasktest.db")

#     c = conn.cursor()

#     c.execute("select name, age, address from users where id =2")

#     user_info = c.fetchone()

#     c.close()
#     print(user_info)

#     return render_template("dbtest.html" , user_info=user_info)

# @app.route("/dbtest2")
# def dbtest2():
#     conn = sqlite3.connect("flaskapp.db")

#     c = conn.cursor()

#     c.execute("select name, age, profile from users where id =1")

#     user_info = c.fetchone()

#     c.close()
#     print(user_info)

#     return render_template("dbtest.html" , user_info=user_info)

@app.route("/add", methods=["GET"])
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/login")
@app.route("/add", methods=["POST"])
def add_post():
    if "user_id" in session:
       
        user_id = session["user_id"]
        task = request.form.get('task')
        conn = sqlite3.connect("flasktest.db")

        c = conn.cursor()

        c.execute("insert into task values (null, ?, ?)", (task, user_id))

        conn.commit()

        c.close()

        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/list")
def task_list():
    if "user_id" in session:

        user_id = session["user_id"]
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select name from user where id = ?", (user_id,))
        user_name = c.fetchone()[0]
        
        c.execute("SELECT id, task from task where user_id = ?", (user_id,))
        task_list= []

        for row in c.fetchall():
            task_list.append({"id" : row[0], "task" : row[1]})

        conn.commit()

        c.close()
        return render_template("task_list.html", user_name = user_name, task_list = task_list)
    else:
        return redirect("/login")

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" in session:

        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()

        c.execute("SELECT id, task from task where id = ?", (id,))
        task= c.fetchone()
        c.close()

        if task is not None:
            task = task[1]
        else:
            return "たすくがないよ"
        
        item = {"id": id, "task":task}
        return render_template("edit.html", task = item)
    else:
        return redirect("/login")
 
@app.route("/edit",methods=["POST"])
def update_task():
    if "user_id" in session:

        item_id = request.form.get("task_id")
        item_id = int(item_id)
        
        
        task = request.form.get("task")

        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("update task set task = ? where id = ?", (task, item_id))
        conn.commit()
        c.close()

        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/delete/<int:id>")
def delete_task(id):
    if "user_id" in session:

        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("delete from task where id = ?", (id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

@app.route("/regist", methods = ["GET"])
def regist_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("regist.html")

@app.route("/regist", methods = ["POST"])
def regist_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into user values(null, ?, ?)", (name, password))
    conn.commit()
    conn.close()
    return "とうろくできましたー"

@app.route("/login", methods = ["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select id from user where name = ? and password = ?", (name, password))
    user_id = c.fetchone()
    c.close()

    if user_id is None:
        return render_template("login.html")
    else:
        session["user_id"]= user_id[0]
        return redirect("/list")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

@app.errorhandler(404)
def notfound(code):
    return render_template("notfound.html")

@app.route("/")
def helloworld():
    return "Hello,World"

if __name__ == "__main__":
    app.run(debug=True)



    # チーム分け
    # A01　まっちょ　美保子さん　さいとうさん
    # A02  大金さん　田尻さん　HMさん　ケイさん

    # チーム分け
    # H01　mocoさん　にしださん　
    # H02  橋本さん　平安座さん　たむ