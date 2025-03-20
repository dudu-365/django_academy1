from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 실제 운영 환경에서는 안전한 키로 변경하세요

# 정적 파일 서빙을 위한 설정
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

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
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # 여기에 이메일 전송 로직 추가
        # send_email(name, email, subject, message)
        
        flash('문의가 성공적으로 전송되었습니다. 빠른 시일 내에 답변 드리겠습니다.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True) 