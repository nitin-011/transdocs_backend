from database.db import get_connection

class User:
    @staticmethod
    def create_user(full_name, email, password):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (full_name, email, password)
                    VALUES (%s, %s, %s)
                    RETURNING id, email, full_name, is_verified
                """, (full_name, email, password))
                result = cursor.fetchone()
                conn.commit()
                return dict(zip(['id', 'email', 'full_name', 'is_verified'], result)) if result else None
            except Exception as e:
                print(f"Error creating user: {e}")
                return None
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def get_user_by_email(email):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, full_name, email, password, is_verified, otp 
                    FROM users WHERE email = %s
                """, (email,))
                result = cursor.fetchone()
                if result:
                    return dict(zip(
                        ['id', 'full_name', 'email', 'password', 'is_verified', 'otp'],
                        result
                    ))
                return None
            except Exception as e:
                print(f"Error getting user: {e}")
                return None
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def update_otp(user_id, otp):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET otp = %s, otp_created_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, email, otp
                """, (otp, user_id))
                result = cursor.fetchone()
                conn.commit()
                return dict(zip(['id', 'email', 'otp'], result)) if result else None
            except Exception as e:
                print(f"Error updating OTP: {e}")
                return None
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def verify_user(user_id):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET is_verified = TRUE, otp = NULL 
                    WHERE id = %s
                    RETURNING id, email, is_verified
                """, (user_id,))
                result = cursor.fetchone()
                conn.commit()
                return dict(zip(['id', 'email', 'is_verified'], result)) if result else None
            except Exception as e:
                print(f"Error verifying user: {e}")
                return None
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def verify_otp(email, otp):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id FROM users 
                    WHERE email = %s AND otp = %s 
                    AND otp_created_at > NOW() - INTERVAL '10 minutes'
                """, (email, otp))
                result = cursor.fetchone()
                return {'id': result[0]} if result else None
            except Exception as e:
                print(f"Error verifying OTP: {e}")
                return None
            finally:
                cursor.close()
                conn.close()