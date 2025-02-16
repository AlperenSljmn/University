from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Kullanıcı modeli
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Ülke modeli
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(2), nullable=False)  # Ülke kodu (TR, UK, US gibi)
    university_count = db.Column(db.Integer, default=0)
    language_school_count = db.Column(db.Integer, default=0)
    min_tuition_fee = db.Column(db.Integer)  # Yıllık minimum eğitim ücreti
    min_living_cost = db.Column(db.Integer)  # Aylık minimum yaşam maliyeti
    visa_success_rate = db.Column(db.Integer)  # Vize başarı oranı
    work_permit = db.Column(db.Boolean, default=False)  # Çalışma izni
    programs = db.relationship('Program', backref='country', lazy=True)

# Program modeli
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Lisans, Yüksek Lisans, Doktora
    duration = db.Column(db.String(50))  # Program süresi
    language = db.Column(db.String(50))  # Eğitim dili
    min_fee = db.Column(db.Integer)  # Minimum ücret
    max_fee = db.Column(db.Integer)  # Maximum ücret
    requirements = db.Column(db.Text)  # Gereksinimler
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

# Danışmanlık başvuru modeli
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    education_level = db.Column(db.String(50), nullable=False)
    target_country = db.Column(db.String(50), nullable=False)
    program_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)

# Örnek veri ekleme fonksiyonu
def add_sample_data():
    # Ülke verileri
    countries = [
        {
            'name': 'İngiltere',
            'code': 'UK',
            'university_count': 150,
            'language_school_count': 15,
            'min_tuition_fee': 15000,
            'min_living_cost': 1000,
            'visa_success_rate': 95,
            'work_permit': True
        },
        {
            'name': 'Amerika',
            'code': 'US',
            'university_count': 200,
            'language_school_count': 25,
            'min_tuition_fee': 20000,
            'min_living_cost': 1200,
            'visa_success_rate': 85,
            'work_permit': True
        },
        {
            'name': 'Almanya',
            'code': 'DE',
            'university_count': 120,
            'language_school_count': 18,
            'min_tuition_fee': 0,
            'min_living_cost': 800,
            'visa_success_rate': 90,
            'work_permit': True
        },
        {
            'name': 'Kanada',
            'code': 'CA',
            'university_count': 96,
            'language_school_count': 12,
            'min_tuition_fee': 12000,
            'min_living_cost': 900,
            'visa_success_rate': 88,
            'work_permit': True
        },
        {
            'name': 'İrlanda',
            'code': 'IE',
            'university_count': 32,
            'language_school_count': 8,
            'min_tuition_fee': 10000,
            'min_living_cost': 850,
            'visa_success_rate': 92,
            'work_permit': True
        }
    ]

    for country_data in countries:
        country = Country.query.filter_by(code=country_data['code']).first()
        if not country:
            country = Country(**country_data)
            db.session.add(country)

    # Program verileri
    programs = [
        {
            'name': 'İşletme Lisans',
            'type': 'Lisans',
            'duration': '4 yıl',
            'language': 'İngilizce',
            'min_fee': 12000,
            'max_fee': 25000,
            'requirements': 'Lise diploması, IELTS 6.0',
            'country_id': 1
        },
        {
            'name': 'Bilgisayar Mühendisliği',
            'type': 'Lisans',
            'duration': '4 yıl',
            'language': 'İngilizce',
            'min_fee': 15000,
            'max_fee': 30000,
            'requirements': 'Lise diploması, IELTS 6.5',
            'country_id': 1
        },
        {
            'name': 'MBA',
            'type': 'Yüksek Lisans',
            'duration': '1-2 yıl',
            'language': 'İngilizce',
            'min_fee': 20000,
            'max_fee': 40000,
            'requirements': 'Lisans diploması, IELTS 6.5, 2 yıl iş tecrübesi',
            'country_id': 1
        }
    ]

    for program_data in programs:
        program = Program.query.filter_by(name=program_data['name'], country_id=program_data['country_id']).first()
        if not program:
            program = Program(**program_data)
            db.session.add(program)

    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    countries = Country.query.all()
    return render_template('home.html', countries=countries)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        application = Application(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            education_level=request.form.get('education_level'),
            target_country=request.form.get('target_country'),
            program_type=request.form.get('program_type'),
            message=request.form.get('message')
        )
        try:
            db.session.add(application)
            db.session.commit()
            flash('Başvurunuz başarıyla alındı!', 'success')
        except:
            db.session.rollback()
            flash('Başvuru gönderilirken bir hata oluştu. Lütfen tekrar deneyin.', 'error')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('home'))
        flash('Geçersiz kullanıcı adı veya şifre', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Kullanıcı adı kontrolü
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor.', 'error')
            return redirect(url_for('register'))

        # E-posta kontrolü
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta adresi zaten kayıtlı.', 'error')
            return redirect(url_for('register'))

        # Şifre kontrolü
        if password != password_confirm:
            flash('Şifreler eşleşmiyor.', 'error')
            return redirect(url_for('register'))

        # Yeni kullanıcı oluşturma
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_data()  # Örnek verileri ekle
    app.run(debug=True) 