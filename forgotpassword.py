from flask import Flask, request, render_template, flash, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="smart_event"
)

# Flask-Mail yapılandırması
app.config['MAIL_SERVER'] = 'smtp.yourmailserver.com'  # E-posta sunucunuzu girin
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # E-posta adresinizi girin
app.config['MAIL_PASSWORD'] = 'your_password'  # E-posta şifrenizi girin
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # E-posta adresini veritabanında kontrol et
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Kullanıcılar WHERE eposta = %s", (email,))
        user = cursor.fetchone()

        if user:
            # Eğer kullanıcı bulunursa, şifre sıfırlama e-postasını gönder
            try:
                # Şifre sıfırlama bağlantısı için token oluşturma (örnek amaçlı sabit bir değer kullanıldı)
                token = 'sifirlama_tokeni_olustur'  # Burada güvenli bir token oluşturmalısın
                reset_url = url_for('reset_password', token=token, _external=True)
                
                # E-posta gönderme işlemi
                msg = Message("Şifre Sıfırlama Talebi",
                              sender="your_email@example.com",
                              recipients=[email])
                msg.body = f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n\n{reset_url}"
                mail.send(msg)

                flash("Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"E-posta gönderilirken bir hata oluştu: {e}", "error")
                return redirect(url_for('forgot_password'))
        else:
            # Eğer e-posta adresi veritabanında bulunamazsa
            flash("Bu e-posta adresi kayıtlı değil.", "error")
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')
