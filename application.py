# https://ru.wikibooks.org/wiki/Flask

from flask import Flask, render_template, request
from api_hh_skills import parsing_skills
from api_hh_salary import parsing_av_salary

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
def cars_form():
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
     return render_template('parsing_answer.html', data=data)

@app.route('/contacts')
def contacts():
     return render_template('contacts.html')

if __name__ == "__main__":
    # app.run()  # в режиме отладки на одном компьютере
    # хорош для начала разработки на локальном сервере. Но это потребует ручного перезапуска сервера после каждого изменения в коде.
    # app.run(host='0.0.0.0') # сделать сервер общедоступным в локальной сети
    app.run(debug=True) # сервер будет сам перегружаться после каждого изменения в коде
