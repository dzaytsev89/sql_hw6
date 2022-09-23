import sqlalchemy
import json
from models import Publisher, Book, Shop, Sale, Stock, create_tables
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser

# DB_USER
db_users = configparser.ConfigParser()
db_users.read("db_user.ini")
sql_user = db_users['db_admin']
sql_login = sql_user['user']
sql_pass = sql_user['pass']


Base = declarative_base()
DSN = f'postgresql://{sql_login}:{sql_pass}@localhost:5432/books'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    create_tables(engine)
    session_orm = Session()

#  fill database
    with open('fixtures/tests_data.json', 'r') as f:
        json_data = json.load(f)
        for line in json_data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
                    }[line.get('model')]
            session_orm.add(model(**line['fields']))
            session_orm.commit()

#  query to database
    while True:
        pub = input('Please enter Publisher id or Publisher name or exit to stop: ')
        if pub.isdigit():
            for q in session_orm.query(Publisher).filter(Publisher.id == int(pub)):
                print(q)
        elif pub == 'exit':
            break
        else:
            for q in session_orm.query(Publisher).filter(Publisher.name == pub):
                print(q)
    session_orm.close()
