from flask import Flask, render_template, request, url_for, redirect, send_from_directory, send_file
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# region Database Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskwuwa'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)
# endregion

# region Config File
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp','gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<filename>')
def upload(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# endregion

# region Route
@app.route('/', methods=['GET'])
def index():
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT * FROM data')
  resonances = cursor.fetchall()
  cursor.close()
  return render_template('index.html', resonances=resonances)


@app.route('/create', methods=['POST'])
def create():
  pass
  cursor = mysql.connection.cursor()
  resonator = request.form['resonator']
  gender = request.form['gender']
  star = int(request.form['star'].replace('Star', ''))
  element = request.form['element']
  weapon = request.form['weapon']
  file = request.files['file']

  filename = file.filename
  filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(filepath)

  sql = "INSERT INTO data(resonator, gender, star, element, weapon, img) VALUES(%s, %s, %s, %s, %s, %s)"
  cursor.execute(sql, (resonator, gender, star, element, weapon, filename))
  mysql.connection.commit()
  cursor.close()
  return redirect(url_for('index'))

@app.route('/update<int:ids>', methods=['POST'])
def update(ids):
  # id_data = request.form['id']
  resonator = request.form['resonator']
  gender = request.form['gender']
  star = int(request.form['star'].replace('Star', ''))
  # rank = request.form['rank']
  element = request.form['element']
  weapon = request.form['weapon']
  file = request.files['file']

  filename = file.filename
  filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(filepath)

  cursor = mysql.connection.cursor()
  sql = """
      UPDATE data SET resonator = %s, gender = %s, star = %s, element = %s, weapon = %s, img = %s
      WHERE id = %s
  """
  cursor.execute(sql, (resonator, gender, star, element, weapon, filename, ids))
  mysql.connection.commit()
  cursor.close()
  return redirect(url_for('index'))

@app.route('/delete<int:ids>', methods=['GET'])
def delete(ids):
  cursor = mysql.connection.cursor()
  cursor.execute('DELETE FROM data WHERE id = %s', (ids,))
  mysql.connection.commit()
  cursor.close()
  return redirect(url_for('index'))
# endregion


if __name__ == '__main__':
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  app.run(debug=True)