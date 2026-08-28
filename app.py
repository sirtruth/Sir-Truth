from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, datetime TEXT, notes TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events ORDER BY datetime ASC")
    events = c.fetchall()
    conn.close()
    
    html = '''
    <html>
    <head><title>College & Life Tracker</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family:sans-serif; padding:20px; background:#121212; color:#fff;">
        <h2>My Schedule & Tracker</h2>
        <form action="/add" method="POST" style="margin-bottom:20px;">
            <input type="text" name="title" placeholder="Event / Repair Name" required style="padding:8px; margin:5px;">
            <select name="category" style="padding:8px; margin:5px;">
                <option>Class</option><option>Work</option><option>Boxing</option><option>Workout</option><option>Phone Repair</option>
            </select>
            <input type="datetime-local" name="datetime" required style="padding:8px; margin:5px;">
            <input type="text" name="notes" placeholder="Notes (e.g. iPhone 13 Screen)" style="padding:8px; margin:5px;">
            <button type="submit" style="padding:8px 15px; background:#007bff; color:#fff; border:none;">Add Event</button>
        </form>
        <table border="1" style="width:100%; border-collapse:collapse; border-color:#444;">
            <tr style="background:#222;"><th>Time</th><th>Category</th><th>Title</th><th>Notes</th></tr>
            {% for e in events %}
            <tr><td>{{ e[3] }}</td><td><b>{{ e[2] }}</b></td><td>{{ e[1] }}</td><td>{{ e[4] }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, events=events)

@app.route('/add', methods=['POST'])
def add():
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (title, category, datetime, notes) VALUES (?, ?, ?, ?)",
              (request.form['title'], request.form['category'], request.form['datetime'], request.form['notes']))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
