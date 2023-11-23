# Validate input
            if not class_no or not rows or not columns:
                flash('Please enter all details', 'danger')
                return redirect(url_for('admin'))

            # Convert input to integers
            try:
                class_no = int(class_no)
                rows = int(rows)
                columns = int(columns)
            except ValueError:
                flash('Invalid input. Please enter numbers for rows, columns, and class number', 'danger')
                return redirect(url_for('admin'))
             # Store class details in the database
            cursor.execute("INSERT INTO rooms (sa_no,class_no, rows, columns, totalseat) VALUES (?, ?, ?, ?, ?)", (sa_no,class_no, rows, columns, totalseat))

            conn.commit()
            
            flash(f'Class {class_no} details stored successfully', 'success')
            
            sa_no = request.form['sa_no']
            class_no=request.form['class_no']
            rows = request.form['rows']
            columns = request.form['columns']
            totalseat = rows * columns
            
    room_number = request.form['room_number']
    num_departments = int(request.form['num_departments'])
    
    department_data = []
    for department in range(1, num_departments + 1):
        start_roll = request.form[f'start_roll_{department}']
        end_roll = request.form[f'end_roll_{department}']
        department_data.append({'department': department, 'start_roll': start_roll, 'end_roll': end_roll})
    
    # Process the data as needed (e.g., store in the database)
    
    return f"Room Number: {room_number}, Departments: {num_departments}, Data: {department_data}"
