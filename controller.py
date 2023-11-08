from flask import Flask, render_template, request, redirect, url_for
import vonage
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calls.db'
db = SQLAlchemy(app)


# Определение модели базы данных
class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, name, phone, description=None):
        self.name = name
        self.phone = phone
        self.description = description


# Создание базы данных
with app.app_context():
    db.create_all()

# Инициализация клиента Vonage
client = vonage.Client(key="8c97096a", secret="aRETPXUqPavRgIH1")
sms = vonage.Sms(client)


@app.route('/')
def index():
    return render_template('site.html')


@app.route('/', methods=['POST'])
def submit_request():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        # Добавьте валидацию данных (пример: проверка корректности номера)

        call = Call(name=name, phone=phone)
        db.session.add(call)

        try:
            db.session.commit()

            # Создайте текстовое сообщение с русским текстом
            text_message = f'Новый заказ звонка от {name}. Телефон: {phone}'

            responseData = sms.send_message({
                'from': "Vonage API",
                'to': '375292595918',  # Примечание: ваш номер получателя
                'text': text_message,
                'type': 'unicode'
            })

            if responseData["messages"][0]["status"] == "0":
                return redirect(url_for('index'))
            else:
                return "Ошибка при отправке SMS"

        except Exception as e:
            db.session.rollback()
            return f'Ошибка: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
