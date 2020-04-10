# https://ru.wikibooks.org/wiki/Flask

from flask import Flask, render_template, request
from api_hh_skills import parsing_skills
from api_hh_salary import parsing_av_salary
import sqlite3 as lite
import sys

app = Flask(__name__)

@app.route('/')
def main_index():
    return render_template('index.html')

@app.route('/request_sgk')
def request_sgk():
     return render_template('request_sgk.html')

@app.route('/request_api')
def request_api():
    return render_template('request_api.html')

@app.route('/parsing_answer', methods = ['POST'])
def parsing_answer():
     city = request.form['city']
     vacancy = request.form['vacancy']

     # Получение информации по средней зарплате путем парсинга сайта
     av_salary = round(parsing_av_salary(city, vacancy), 2)
     if av_salary == 0:
         av_salary = 'Нет информации'

     # Получение информации об основных навыках путем парсинга сайта
     skills_list = parsing_skills(city, vacancy)
     len_skills = len(skills_list)
     if len_skills == 0:
         skills_info = 'Нет информации'
     else:
         skills_info = ''
         for i in range(len_skills-1):
            skills_info = skills_info + skills_list[i] + ', '
         skills_info = skills_info + skills_list[len_skills-1]
    # Наполнение формы для выдачи информацией
     data = {
             'city': city,
             'vacancy': vacancy,
             'av_salary': av_salary,
             'skills_info': skills_info}
     try:
         connect = lite.connect('vacancy_db.db')
         with connect:
             cur = connect.cursor()
             # Подсчет количества существующих записей в базе
             cur.execute("SELECT Count() FROM vacancies")
             numberOfRows = cur.fetchone()[0]
             # Вставка данных в базу
             cur.execute("INSERT INTO vacancies VALUES(?,?,?,?,?)", (
             numberOfRows+1, city, vacancy, av_salary, skills_info))
             # connect.close()
     except lite.Error as e:
         print(f"Error {e.args[0]}:")
         sys.exit(1)
     return render_template('parsing_answer.html', data=data)

@app.route('/contacts')
def contacts():
     return render_template('contacts.html')

@app.route('/contacts_ok', methods = ['POST'])
def contacts_ok():
     email = request.form['email']
     name = request.form['name']
     post_mail = request.form['post_mail']
     message = request.form['message'].strip()
     try:
         connect = lite.connect('contacts_db.db')
         with connect:
             cur = connect.cursor()
             # Подсчет количества существующих записей в базе
             cur.execute("SELECT Count() FROM contacts")
             numberOfRows = cur.fetchone()[0]
             # Вставка данных в базу
             cur.execute("INSERT INTO contacts VALUES(?,?,?,?,?)", (numberOfRows + 1, email, name, post_mail, message))
             # connect.close()
     except lite.Error as e:
        print(f"Error {e.args[0]}:")
        sys.exit(1)
     return render_template('contacts_ok.html', message=message)

if __name__ == "__main__":
    # app.run()  # в режиме отладки на одном компьютере
    # хорош для начала разработки на локальном сервере. Но это потребует ручного перезапуска сервера после каждого изменения в коде.
    # app.run(host='0.0.0.0') # сделать сервер общедоступным в локальной сети
    app.run(debug=True) # сервер будет сам перегружаться после каждого изменения в коде
