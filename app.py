from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory database substitute (for demo purposes)
users = []

# Models
class User:
    def __init__(self, first_name, last_name, profile_picture, username, email, password, address, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.user_type = user_type

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['profile_picture']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = {
            'line1': request.form['address_line1'],
            'city': request.form['city'],
            'state': request.form['state'],
            'pincode': request.form['pincode']
        }
        user_type = request.form['user_type']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        # Create new user
        new_user = User(first_name, last_name, profile_picture, username, email, password, address, user_type)
        users.append(new_user)

        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = next((u for u in users if u.username == username), None)

        if user and check_password_hash(user.password, password):
            session['user'] = username
            session['user_type'] = user.user_type
            flash('Login successful!')
            if user.user_type == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif user.user_type == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid credentials!')

    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    if 'user' not in session or session['user_type'] != 'Patient':
        return redirect(url_for('login'))
    user = next((u for u in users if u.username == session['user']), None)
    return render_template('patient_dashboard.html', user=user)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user' not in session or session['user_type'] != 'Doctor':
        return redirect(url_for('login'))
    user = next((u for u in users if u.username == session['user']), None)
    return render_template('doctor_dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_type', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
