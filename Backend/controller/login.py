from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from db import get_db, User
from auth import verify_password

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password):
            flash('Invalid email or password')
            return redirect(url_for('login.login'))
            
        if not user.is_verified:
            flash('Please verify your email first')
            session['email'] = email
            return redirect(url_for('auth.verify_otp'))
            
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')