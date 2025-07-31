import psycopg2
from flask import Flask

app = Flask(__name__)

# your Render Postgres URL
DATABASE_URL = (
    'postgresql://'
    'ex_database_user:ArMJEGHvOpN87glr90waAZ4IxjJRuaw0'
    '@dpg-d25a1sffte5s73c2bje0-a/ex_database'
)

@app.route('/')
def hello_world():
    return 'Hello, World from Joel in 3308'

@app.route('/db_test')
def db_test():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.close()
    return 'Database connection successful'

@app.route('/db_create')
def db_create():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS Basketball (
        First   VARCHAR(30),
        Last    VARCHAR(30),
        City    VARCHAR(30),
        Name    VARCHAR(30),
        Number  INT
      );
    """)
    conn.commit()
    cur.close()
    conn.close()
    return 'Basketball Table Created'

@app.route('/db_insert')
def db_insert():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO Basketball (First, Last, City, Name, Number)
      VALUES
        ('Jayson', 'Tatum',     'Boston',        'Celtics',  0),
        ('Stephen','Curry',     'San Francisco', 'Warriors', 30),
        ('Nikola',  'Jokic',     'Denver',        'Nuggets',  15),
        ('Kawhi',   'Leonard',   'Los Angeles',   'Clippers', 2);
    """)
    conn.commit()
    cur.close()
    conn.close()
    return 'Basketball Table Populated'

@app.route('/db_select')
def db_select():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Basketball;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # build a simple HTML table
    html = '<table border="1">'
    html += (
        '<tr>'
        '<th>First</th>'
        '<th>Last</th>'
        '<th>City</th>'
        '<th>Name</th>'
        '<th>Number</th>'
        '</tr>'
    )
    for first, last, city, name, number in rows:
        html += (
            '<tr>'
            f'<td>{first}</td>'
            f'<td>{last}</td>'
            f'<td>{city}</td>'
            f'<td>{name}</td>'
            f'<td>{number}</td>'
            '</tr>'
        )
    html += '</table>'
    return html

@app.route('/db_drop')
def db_drop():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Basketball;")
    conn.commit()
    cur.close()
    conn.close()
    return 'Basketball Table Dropped'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
