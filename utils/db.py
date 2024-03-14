from sqlmodel import Session, SQLModel, create_engine

username = "root"
password = "123456"
host = "localhost"
port = 3306
database = "fwwb"
mysql_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(mysql_url)
# engine = create_engine(mysql_url, echo=True,)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def getSession():
    # with Session(engine) as session:
        # yield session
    with Session(engine) as session:
        return session
# Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session

# Code below omitted 👇

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()



# def main():
    # create_db_and_tables()
    # add_user()
    # print(get_user('johndoe'))