from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todolist'

mysql = MySQL(app)

@app.route('/addCatatan', methods = ['POST'])
def addCatatan():
        #get data from request
        task = request.form['task']
        deskripsi = request.form['deskripsi']
        status = request.form['status']
        tanggal = request.form['tanggal']

        # Create connection
        conn = mysql.connect
        # Create cursor
        cur = conn.cursor()
        sql = "INSERT INTO catatan (task, deskripsi, status, tanggal) VALUES (%s,%s,%s,%s)"
        val = (task, deskripsi, status, tanggal)
        cur.execute(sql, val)

        # Commit to database
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()
        return jsonify({'message': "catatan berhasil ditambahkan"})

@app.route('/mycatatan')
def mycatatan():
    # Create connection
    cur = mysql.connect.cursor()
    
    cur.execute("SELECT * FROM catatan")

    # get colomn name from cursor.description
    column_names = [i[0] for i in cur.description]

    data = []
    for row in cur.fetchall():
        data.append(dict(zip(column_names, row)))
        
    cur.close()
    return jsonify(data)

@app.route('/detailcatatan', methods = ['GET'])
def detailtask():

    if 'id' in request.args:
         # Create connection
        conn = mysql.connect
        # Create cursor
        cur = conn.cursor()
        sql = "SELECT * FROM catatan WHERE id_task = %s"
        val = (request.args['id'],)
        cur.execute(sql, val)

        # get colomn name from cursor.description
        column_names = [i[0] for i in cur.description]

        row = cur.fetchone()

        if row:
            # Create a dictionary for the single row
            data = dict(zip(column_names, row))
            cur.close()
            return jsonify(data)
        else:
            cur.close()
            return jsonify({"error": "Data not found"}), 404
        
       

@app.route('/editcatatan', methods = ['PUT'])
def editcatatan():
    if 'id' in request.args:
        task = request.form['task']
        deskripsi = request.form['deskripsi']
        status = request.form['status']


         # Create connection
        conn = mysql.connect
        # Create cursor
        cur = conn.cursor()

        sql = "UPDATE catatan SET task=%s, deskripsi=%s, status=%s WHERE id_task = %s"
        val = (task, deskripsi, status, request.args['id'],)
        cur.execute(sql, val)
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()
        return jsonify({'message': "task berhasil diedit"})
    else:
        return jsonify({'error': "id tidak ditemukan dalam parameter"}), 400
    
@app.route('/hapusCatatan', methods = ['DELETE'])
def hapusCatatan():
    if 'id' in request.args:

         # Create connection
        conn = mysql.connect
        # Create cursor
        cur = conn.cursor()
        sql = "DELETE FROM catatan WHERE id_task = %s"
        val = (request.args['id'],)
        cur.execute(sql, val)
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()
        return jsonify({'message': "task berhasil dihapus"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)