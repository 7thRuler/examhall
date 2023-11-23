from flask import Flask, redirect, render_template, request, url_for, flash, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('index.html')
@app.route("/About")
def about():
    return render_template("about.html")
@app.route("/login",methods=['GET','POST'])
def login():
	error = None
	if request.method=='POST':
		email = request.form['email']
		password = request.form['psw']
		if email =="admin@gmail.com" and password == "admin@123":
			return  redirect(url_for('admin'))
		else:
			error = "INVALID DETAILS"
	return render_template("login.html",error=error)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
        if request.method == 'POST':
        
            
            # Get the values from the admin
            year = request.form['year']
            dep = request.form['department']
    
            # Connect to SQLite database
            conn = sqlite3.connect('room_details.db')
            cursor = conn.cursor()

            # Retrieve room numbers for students based on year and department
            cursor.execute("SELECT room_no FROM class WHERE year=? AND dep=?", (year, dep))
            room_numbers = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return render_template('admin.html', room_numbers=room_numbers)
            
        

            

        return render_template('admin.html')
   
@app.route("/insert",methods=['GET','POST'])
def insert(): 
    if request.method == 'POST':
        sa_no = request.form['sa_no']
        class_no=request.form['class_no']
        rows = int(request.form['rows'])
        columns = int(request.form['columns'])
        totalseat = rows * columns
        
        conn = sqlite3.connect('room_details.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO rooms (sa_no,class_no, rows, columns, totalseat) VALUES (?, ?, ?, ?, ?)", (sa_no,class_no, rows, columns, totalseat))

        conn.commit()
        cursor.close()
        conn.close()
            
        flash(f'Class {class_no} details stored successfully', 'success')

            

    return render_template('admin.html')
    
@app.route("/alloc",methods=['GET','POST'])
def dropdown():
    conn = sqlite3.connect('room_details.db')
    cursor = conn.cursor()
    cursor.execute("SELECT class_no FROM rooms")
    data = cursor.fetchall()
    conn.close()
    return data

def alloc():
    if request.method== 'POST':
        # class_no = int(request.form['class_no'])
        num_departments = int(request.form['num_departments'])
        # Create lists to store starting and ending roll numbers for each department
        start_roll_numbers = []
        end_roll_numbers = []   
        
        # conn = sqlite3.connect('room_details.db')
        # cursor = conn.cursor() 
           
        # cursor.execute("SELECT DISTINCT class_no FROM rooms")
        # room_no=[row[0] for row in cursor.fetchone()]
       
        # cursor.close()
        # conn.close()
        
        
        
        # Retrieve starting and ending roll numbers for each department
        for i in range(1, num_departments + 1):
            start_roll_key = 'start_roll_' + str(i)
            end_roll_key = 'end_roll_' + str(i)

            start_roll_numbers.append(request.form.get(start_roll_key, ''))
            end_roll_numbers.append(request.form.get(end_roll_key, ''))

        # start_roll_numbers = [int(request.form[f'start{i}']) for i in range(1, int(num_departments) + 1)]
        # end_roll_numbers = [int(request.form[f'end{i}']) for i in range(1, num_departments + 1)]

        # Example matrix logic (replace with your actual logic)
        
        # return render_template('alloc.html', arrangement_table=arrangement_table)
        
    
        
        return render_template('alloc.html')
    else:
        values=dropdown()
        return render_template('alloc.html', values=values)

# Matrix Logic (matrix.py)

@app.route("/register",methods=['GET','POST'])
def register():
    return render_template("register.html")
@app.route("/attend",methods=['GET','POST'])
def attend():
    return render_template("attend.html")

@app.route("/dash",methods=['GET','POST'])
def dash():
    if request.method == 'POST':
        # Shuffle sa_no values
        shuffle_sa_no()

        # Flash a success message
        flash(f'SA Numbers shuffled successfully!', 'success')

        # Redirect to the dashboard page
        return redirect(url_for('dash'))
    
    conn = sqlite3.connect('room_details.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sa_no,class_no,rows,columns,totalseat FROM rooms ORDER BY sa_no ASC")
        data = cursor.fetchall()
    return render_template("dash.html",data=data)

def shuffle_sa_no():
    # Connect to the database
    conn = sqlite3.connect('room_details.db')
    cursor = conn.cursor()

    # Fetch all unique sa_no values
    cursor.execute("SELECT sa_no FROM rooms")
    sa_no_values = [row[0] for row in cursor.fetchall()]

    # Shuffle the sa_no values
    w=random.sample(sa_no_values, len(sa_no_values))
    # random.shuffle(sa_no_values)

    # Update sa_no values in the database
    for i, san in  enumerate(w):
        cursor.execute("UPDATE rooms SET sa_no=? WHERE id=?", (san, i+1))

    # Commit changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()
@app.route('/delete/<id>')
def delete(id):
	conn = sqlite3.connect("room_details.db")
	with conn:
		cursor = conn.cursor()
		cursor.execute("DELETE FROM rooms WHERE class_no=?",[id])
	return  redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
