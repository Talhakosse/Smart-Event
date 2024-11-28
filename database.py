from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="smart_event"
)

# Kayıt Sayfası
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = generate_password_hash(request.form['sifre'])
        eposta = request.form['eposta']
        konum = request.form.get('konum')
        ilgi_alanlari = request.form.get('ilgi_alanlari')
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        dogum_tarihi = request.form['dogum_tarihi']
        cinsiyet = request.form['cinsiyet']
        telefon_no = request.form.get('telefon_no')
        profil_fotografi = request.form.get('profil_fotografi')

        print(kullanici_adi, sifre, ad, soyad, dogum_tarihi, cinsiyet, eposta, telefon_no, konum, ilgi_alanlari)

        cursor = db.cursor()
        print("Bağlantı başarılı")
        try:
            cursor.execute("""
                INSERT INTO Kullanıcılar (kullanici_adi, sifre, eposta, konum, ilgi_alanlari, ad, soyad, dogum_tarihi, cinsiyet, telefon_no, profil_fotografi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (kullanici_adi, sifre, eposta, konum, ilgi_alanlari, ad, soyad, dogum_tarihi, cinsiyet, telefon_no, profil_fotografi))
            
            print("denem12")
            db.commit()
            flash('Kayıt başarılı! Lütfen giriş yapın.')
            print  ("Kayıt Başarılı")
            print(kullanici_adi, sifre, ad, soyad, dogum_tarihi, cinsiyet, eposta, telefon_no, konum, ilgi_alanlari)

            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            print("Kayıt Başarısız!!!!!!")
            flash('Kullanıcı adı veya e-posta zaten kayıtlı.')
            return redirect(url_for('register'))

    return render_template('register.html')
# Gmaps Api KEY
# AIzaSyBP3bz0Tjl0ea105t9zeY_nUtpQz93Tq6c Aktif
# Giriş Sayfası
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("selamiko")
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        print(kullanici_adi)
        print(sifre)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Kullanıcılar WHERE kullanici_adi = %s", (kullanici_adi,))
        user = cursor.fetchone()
        print(check_password_hash(user['sifre']),sifre)
        if user and check_password_hash(user['sifre'], sifre):

            session['user_id'] = user['ID']
            flash('Giriş başarılı!')
            print("Selam baba")
            return redirect(url_for('dashboard'))  # Burada 'dashboard' fonksiyonuna yönlendiriyoruz
        else:
            flash('Kullanıcı adı veya şifre hatalı!')

    return render_template('login.html')

# Ana Sayfa
@app.route('/dashboard')
def dashboard():
    print("Hİİ")
    if 'user_id' in session:
        return render_template('dashboard.html')  # dashboard.html dosyasını render ediyoruz
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)