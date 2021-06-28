from flask import request
from flask import Response
from PIL import Image
from io import BytesIO
import json
from flask import Flask
import os
import numpy as np
from flask_bootstrap import Bootstrap

print("Hello world")
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return '<html><head></head> <body> Hello World! <br> We have <br> <a href="/net">Individual Quest</a> </body></html>'
if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
from flask import render_template

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
# модули валидации полей формы
from wtforms.validators import DataRequired, InputRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeI2PcaAAAAAFFrENF59lFzOhzD1OIP9EIZ0kNl'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeI2PcaAAAAAAuCgoZ4PHcy59UJyZSD22eEafEI'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами

bootstrap = Bootstrap(app)
# создаем форму для загрузки файла

class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 
 number = DecimalField('Размер вашей рамки', validators=[InputRequired(), NumberRange(min=0, max=3000, message='Разместите числа от 0 до 3000')])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[ FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
 
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from iz1 import makegraphs
from werkzeug.utils import secure_filename
# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def iz():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filenames = {}
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  for f in os.listdir('./static/'): #
   os.remove('./static/'+f) # 
  # файлы с изображениями читаются из каталога src
  filename = os.path.join('./static/', secure_filename(form.upload.data.filename)) #
  # сохраняем загруженный файл
  form.upload.data.save(filename)
  fimage = Image.open(filename)
  # передать загруженный файл
  filenames = makegraphs(fimage,form.number.data)
 # передаем форму в шаблон
 # если был нажат сабмит, либо передадим falsy значения
 return render_template('iz.html',form=form,image_res=filenames)

