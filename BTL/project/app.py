from flask import Flask, render_template, request, redirect, session
import sqlite3
from crypto_utils import des3_encrypt, des3_decrypt, aes_encrypt, aes_decrypt
from log_utils import write_log
from base64 import b64encode
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            cmnd TEXT,
            bhxh TEXT,
            bank TEXT,
            key_des TEXT,
            key_aes TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        cmnd = request.form['cmnd']
        bhxh = request.form['bhxh']
        bank = request.form['bank']

        key1 = b64encode(os.urandom(16)).decode()
        key2 = b64encode(os.urandom(32)).decode()

        cmnd_enc = des3_encrypt(cmnd, key1)
        bhxh_enc = aes_encrypt(bhxh, key2)
        bank_enc = aes_encrypt(bank, key2)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("""INSERT INTO users (username, password, name, cmnd, bhxh, bank, key_des, key_aes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                      (username, password, name, cmnd_enc, bhxh_enc, bank_enc, key1, key2))
            conn.commit()
        except:
            return "Tài khoản đã tồn tại"
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = user[0]
            session['role'] = 'admin' if user[1].lower() == 'admin' else 'user'
            return redirect('/admin' if session['role'] == 'admin' else '/dashboard')
        return "Sai tài khoản hoặc mật khẩu"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (session['user'],))
    user = c.fetchone()
    conn.close()

    key1 = user[7]
    key2 = user[8]

    cmnd = des3_decrypt(user[4], key1)
    bhxh = aes_decrypt(user[5], key2)
    bank = aes_decrypt(user[6], key2)

    return render_template('dashboard.html', name=user[3], cmnd=cmnd, bhxh=bhxh, bank=bank)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        cmnd = request.form['cmnd']
        bhxh = request.form['bhxh']
        bank = request.form['bank']
        c.execute("SELECT * FROM users WHERE id=?", (session['user'],))
        user = c.fetchone()
        key1 = user[7]
        key2 = user[8]
        cmnd_enc = des3_encrypt(cmnd, key1)
        bhxh_enc = aes_encrypt(bhxh, key2)
        bank_enc = aes_encrypt(bank, key2)
        c.execute("UPDATE users SET name=?, cmnd=?, bhxh=?, bank=? WHERE id=?",
                  (name, cmnd_enc, bhxh_enc, bank_enc, session['user']))
        conn.commit()
        conn.close()
        write_log(session.get('user'), 'Sửa thông tin', 'Người dùng đã sửa thông tin')
        return redirect('/dashboard')
    else:
        c.execute("SELECT * FROM users WHERE id=?", (session['user'],))
        user = c.fetchone()
        conn.close()
        key1 = user[7]
        key2 = user[8]
        cmnd = des3_decrypt(user[4], key1)
        bhxh = aes_decrypt(user[5], key2)
        bank = aes_decrypt(user[6], key2)
        return render_template('edit.html', name=user[3], cmnd=cmnd, bhxh=bhxh, bank=bank)

@app.route('/delete')
def delete():
    if 'user' not in session:
        return redirect('/login')
    write_log(session.get('user'), 'Xóa tài khoản', 'Người dùng tự xóa tài khoản')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (session['user'],))
    conn.commit()
    conn.close()
    session.clear()
    return redirect('/login')

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username, name FROM users WHERE username != 'admin'")
    users = c.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@app.route('/admin/view/<int:user_id>', methods=['GET', 'POST'])
def admin_view(user_id):
    if session.get('role') != 'admin':
        return redirect('/login')
    if request.method == 'POST':
        admin_pass = request.form['password']
        if admin_pass != 'admin123':
            return "<script>alert('Sai mật khẩu quản trị!'); window.location='/admin';</script>"
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = c.fetchone()
        conn.close()
        key1 = user[7]
        key2 = user[8]
        decrypted = {
            'id': user[0],
            'username': user[1],
            'name': user[3],
            'cmnd': des3_decrypt(user[4], key1),
            'bhxh': aes_decrypt(user[5], key2),
            'bank': aes_decrypt(user[6], key2)
        }
        write_log('admin', 'Xem thông tin', f'Admin xem user_id={user_id}')
        return render_template('admin_detail.html', user=decrypted)
    return render_template('admin_verify.html', user_id=user_id)

@app.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_edit(user_id):
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    key1 = user[7]
    key2 = user[8]
    if request.method == 'POST':
        name = request.form['name']
        cmnd = request.form['cmnd']
        bhxh = request.form['bhxh']
        bank = request.form['bank']
        cmnd_enc = des3_encrypt(cmnd, key1)
        bhxh_enc = aes_encrypt(bhxh, key2)
        bank_enc = aes_encrypt(bank, key2)
        c.execute("UPDATE users SET name=?, cmnd=?, bhxh=?, bank=? WHERE id=?",
                  (name, cmnd_enc, bhxh_enc, bank_enc, user_id))
        conn.commit()
        conn.close()
        write_log('admin', 'Sửa thông tin', f'Admin sửa user_id={user_id}')
        return redirect('/admin')
    cmnd = des3_decrypt(user[4], key1)
    bhxh = aes_decrypt(user[5], key2)
    bank = aes_decrypt(user[6], key2)
    return render_template('admin_edit.html', user=user, cmnd=cmnd, bhxh=bhxh, bank=bank)

@app.route('/admin/delete/<int:user_id>')
def admin_delete(user_id):
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    write_log('admin', 'Xóa tài khoản', f'Admin xóa user_id={user_id}')
    return redirect('/admin')

# Import SQLAlchemy hoặc thư viện DB bạn đang dùng
# from your_database_module import db # Ví dụ

@app.route('/admin/logs')
# @login_required # Nên có yêu cầu đăng nhập admin ở đây
def admin_logs():
    # Lấy dữ liệu log từ cơ sở dữ liệu (ví dụ: 50 log gần nhất)
    # logs_data = db.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50").fetchall() # Ví dụ truy vấn
    # Dữ liệu giả định cho đến khi bạn có DB thật
    logs_data = [
        (1, 1, 'admin', 'User Edit', 2, 'Edited user "user1" full name to "Trần Thị B"', '2025-07-01 10:00:00', '192.168.1.1'),
        (2, 1, 'admin', 'User Delete', 3, 'Deleted user "tester"', '2025-07-01 10:05:00', '192.168.1.1'),
        (3, 1, 'admin', 'Login Success', None, 'Admin logged in', '2025-07-01 09:55:00', '192.168.1.1'),
    ]
    return render_template('admin_logs.html', logs=logs_data)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        old = request.form['old_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        if new != confirm:
            return "<script>alert('Mật khẩu mới và xác nhận không trùng khớp'); window.location='/change-password';</script>"

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE id=?", (session['user'],))
        current_pass = c.fetchone()[0]

        if old != current_pass:
            conn.close()
            return "<script>alert('Mật khẩu cũ không đúng'); window.location='/change-password';</script>"

        c.execute("UPDATE users SET password=? WHERE id=?", (new, session['user']))
        conn.commit()
        conn.close()

        write_log(session['user'], 'Đổi mật khẩu', 'Người dùng đã đổi mật khẩu')
        return "<script>alert('Đổi mật khẩu thành công'); window.location='/dashboard';</script>"

    return render_template('change_password.html')
@app.route('/admin/change-password/<int:user_id>', methods=['GET', 'POST'])
def admin_change_password(user_id):
    if session.get('role') != 'admin':
        return redirect('/login')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    
    if not user:
        conn.close()
        return "Không tìm thấy người dùng"
    
    username = user[0]
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        c.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
        conn.commit()
        conn.close()
        write_log('admin', 'Đổi mật khẩu', f'Admin đổi mật khẩu cho user_id={user_id}')
        return redirect('/admin')

    conn.close()
    return render_template('admin_change_password.html', user_id=user_id, username=username)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
