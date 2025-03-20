from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
Bootstrap(app)

# Load configuration from .env file
app.config.from_prefixed_env()

# Flask-Mail 설정
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key'),
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER'),
    MAIL_MAX_EMAILS=None,
    MAIL_ASCII_ATTACHMENTS=False,
    MAIL_SUPPRESS_SEND=False
)

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/cases')
def cases():
    return render_template('cases.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        phone = request.form.get('phone')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, phone, email, subject, message]):
            flash('모든 필수 항목을 입력해주세요.', 'danger')
            return redirect(url_for('contact'))

        try:
            # 이메일 내용 구성
            email_content = f"""
            새로운 문의가 접수되었습니다:
            
            이름: {name}
            회사: {company}
            전화: {phone}
            이메일: {email}
            문의 유형: {subject}
            
            문의 내용:
            {message}
            """

            # 이메일 전송
            msg = Message(
                subject=f'[JYT 웹사이트] {subject} - {name}',
                recipients=[app.config['MAIL_DEFAULT_SENDER']],
                body=email_content,
                charset='utf-8'
            )
            
            with app.app_context():
                mail.send(msg)
            
            flash('문의가 성공적으로 전송되었습니다. 빠른 시일 내에 답변 드리겠습니다.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f'이메일 전송 오류: {str(e)}')
            flash('문의 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True) 