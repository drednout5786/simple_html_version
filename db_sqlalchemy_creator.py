from sqlalchemy import Column, Integer, String, Float, Date, Text, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import exc, CheckConstraint

# https://coderlessons.com/tutorials/bazy-dannykh/sqlalchemy/sqlalchemy-kratkoe-rukovodstvo
# Чтобы соединиться с СУБД, используется функция create_engine():
# для настройки объекта механизма, который впоследствии используется для выполнения операций SQL
engine = create_engine('sqlite:///orm1.sqlite', echo=False)

# Декларативное создание таблицы, класса и отображения за один раз
# Базовый класс хранит каталог классов и сопоставленных таблиц в декларативной системе. Это называется декларативным базовым классом.
Base = declarative_base()

class Vacancy_info(Base):
    __slots__ = ()
    __tablename__ = 'vacancy_info'
    id = Column(Integer, primary_key=True)
    city = Column(Integer, ForeignKey('city.id'))
    vacancy = Column(Integer, ForeignKey('vacancy.id'))
    av_salary = Column(Float)
    skills_list = Column(String)
    # try:
    #     av_salary = Column(Integer, positive=True)
    # except TypeError:
    #     print("Ошибка! Значение заработной платы не может быть отрицательным.")
    # __table_args__ = (
    #     CheckConstraint(av_salary >= 0, name='check_bar_positive'),
    #     {})


    def __init__(self, city, vacancy, av_salary, skills_list):
        self.city = city
        self.vacancy = vacancy
        self.av_salary = av_salary
        self.skills_list = skills_list

    def __str__(self):
        return f'{self.city}, {self.vacancy}, {self.av_salary}, {self.skills_list}'

class City(Base):
    __slots__ = ()
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String, unique=True)

    def __init__(self, city):
        self.city = city

    def __str__(self):
        return f'{self.city}'

class Vacancy(Base):
    __slots__ = ()
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy = Column(String, unique=True)

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def __str__(self):
        return f'{self.vacancy}'


class Contacts(Base):
    __slots__ = ()
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    post_mail = Column(String)
    message = Column(String)
    date = Column(Date)

    def __init__(self, email, name, post_mail, message, date):
        self.email = email
        self.name = name
        self.post_mail = post_mail
        self.message = message
        self.date = date

    def __str__(self):
       return f'{self.email}, {self.name}, {self.post_mail}, {self.message}, {self.date}'

if __name__ == '__main__':
    # Создание таблицы
    # Объект Table создается в соответствии со спецификациями и связывается с классом путем создания объекта Mapper.
    # Этот объект сопоставления не используется напрямую, но используется внутри как интерфейс между отображаемым классом и таблицей.
    #
    # Каждый объект Table является членом большой коллекции, известной как MetaData, и этот объект доступен с помощью
    # атрибута .metadata декларативного базового класса. Метод MetaData.create_all () передает наш движок в качестве
    # источника подключения к базе данных. Для всех таблиц, которые еще не были созданы, он выдает операторы CREATE TABLE в базу данных.
    Base.metadata.create_all(engine)

    # Создание сессии. Теперь мы готовы начать общение с базой данных.
    # Чтобы взаимодействовать с базой данных, нам нужно получить ее дескриптор. Объект сеанса является дескриптором базы данных.
    # Класс сеанса определяется с помощью sessionmaker () – настраиваемого метода фабрики сеансов, который привязан к объекту механизма, созданному ранее.
    Session = sessionmaker(bind=engine)

    # Затем объект сеанса устанавливается с помощью конструктора по умолчанию следующим образом:
    session = Session()

    # Пробное наполнение базы -----------------------------------------------------------------
    # city = [['Москва'], ['Самара']]
    # vacancy = [['Python'], ['SQL']]
    # session.commit()
    # vacancy_info = [['Москва', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux', datetime.today()],
    #                 # ['Самара', 'SQL', 67437.5, 'sql, t, процедура, ms, интересоваться, функция, триггер, server, хранить, oracle', datetime.today()],
    #                 # ['Москва', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux', datetime.today()],
    #                 # ['Орел', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux', datetime.today()],
    #                 ['Самара', 'SQL', 67437.5, 'sql, t, процедура, ms, интересоваться, функция, триггер, server, хранить, oracle', datetime.today()]
    #                 ]
    #
    # contacts = [['q1@mail.ru', 'Борис', 'Москва, ул.Тверская, д.7, кв.1', 'Хочу в отпуск!'],
    #             ['q2@mail.ru', 'Ольга', 'Самара, ул.Ленина, д.3, кв.56', 'Хочу на работу!']]
    #
    # session.add_all([City(x[0]) for x in city])
    # session.add_all([Vacancy(x[0]) for x in vacancy])
    #
    # session.commit()
    #
    # session.add_all([Vacancy_info(session.query(City).filter(City.city == x[0]).first().id,
    #                               session.query(Vacancy).filter(Vacancy.vacancy == x[1]).first().id,
    #                               x[2], x[3]) for x in vacancy_info])
    # session.commit()
    #
    # session.add_all([Contacts(x[0], x[1], x[2], x[3]) for x in contacts])
    # session.commit()

    # JOIN ---------------------
    # Объединение 2-х таблиц Vacancy_info и City по столбцу Vacancy_info.city == City.id
    # query = session.query(Vacancy_info, City)
    # query = query.join(Vacancy_info, Vacancy_info.city == City.id)
    # records = query.all()
    # for obj1, obj2 in records:
    #     print(obj1,obj2)

    # FILTER ---------------------
    # Первый найденный по фильтру
    # city_query1 = session.query(Vacancy_info).filter_by(city=1).first()
    # print(city_query1)

    # Все найденные по фильтру
    # city_query = session.query(Vacancy_info).filter(Vacancy_info.city.in_([1])).all()
    # for city in city_query:
    #     print(city.city, city.skills_list)
    # -------------------------------------------------------------------------------
    # Все найденные без фильтров
    # for u in session.query(Vacancy_info).order_by(Vacancy_info.id):
    #     print('print5: ', u)

    # Отладка отлицательной или нулевой срезней зарплаты ----------------------------
    # city = 'Смоленск'
    # vacancy = 'дворник'
    # av_salary = -100.5
    # skills_info = ''
    #
    # # if av_salary <= 0:
    # #     av_salary = 0
    #
    # try:
    #     session.add(City(city))
    #     session.commit()
    # except exc.IntegrityError:
    #     session.rollback()
    #
    # try:
    #     session.add(Vacancy(vacancy))
    #     session.commit()
    # except exc.IntegrityError:
    #     session.rollback()
    #
    # session.add(Vacancy_info(session.query(City).filter(City.city == city).first().id,
    #                          session.query(Vacancy).filter(Vacancy.vacancy == vacancy).first().id,
    #                          av_salary, skills_info))
    # session.commit()




