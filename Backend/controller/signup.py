from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from db import get_db, User
from auth import hash_password, generate_otp, send_otp_email
from datetime import datetime

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        
        db = next(get_db())
        
        # Check if user already exists
        if db.query(User).filter(User.email == email).first():
            flash('Email already registered')
            return redirect(url_for('signup.signup'))
        
        # Create new user
        otp = generate_otp()
        new_user = User(
            full_name=full_name,
            email=email,
            password=hash_password(password),
            otp=otp,
            otp_created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        
        # Send OTP email
        if send_otp_email(email, otp):
            session['email'] = email
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Error sending verification email')
            return redirect(url_for('signup.signup'))
            
    return render_template('signup.html')