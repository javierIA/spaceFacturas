
import os
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import urllib
from dotenv import load_dotenv

load_dotenv()


Host=os.getenv("HOST")
User=os.getenv("USER")
Password=os.getenv("PASS")
Database=os.getenv("DATABASE")

server = Host # to specify an alternate port
database = Database
username = User
password = Password
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password)
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params,echo=True)
Base = declarative_base()

class providers(Base):
    __tablename__ = "provedores"
    id_fiscal=Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    ident_fiscal = Column(VARCHAR)

def __init__(self, name, ident_fiscal):
    """"""
    self.name = name
    self.ident_fiscal = ident_fiscal
     
def __repr__(self):
        return f'provider({self.id_fiscal}, {self.name}, {self.ident_fiscal})'
    
    
class clients(Base):
    __tablename__ = "clients"
    RFC_clients=Column(VARCHAR(50), primary_key=True)
    Name_clients = Column(VARCHAR(50))
    
def __init__(self, RFC_clients, Name_clients):
    self.RFC_clients = RFC_clients
    self.Name_clients = Name_clients
    
def __repr__(self):
    return f'provider({self.RFC_clients}, {self.Name_clients})'

class pdf(Base):
    __tablename__ = "pdfs"
    id_pdfs=Column(Integer, primary_key=True,autoincrement=True)
    author_pdfs = Column(VARCHAR)
    path_pdfs = Column(VARCHAR,unique=True)
    status_pdfs = Column(VARCHAR)

def __init__(self, author_pdfs, path_pdfs, status_pdfs):
    self.author_pdfs = author_pdfs
    self.path_pdfs = path_pdfs
    self.status_pdfs = status_pdfs
def __repr__(self):
    return f'pdf({self.author_pdfs}, {self.path_pdfs})'
    
    
    
def get_providers():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(providers).all()
def get_provider(id_fiscal):
    Session = sessionmaker(bind=engine)
    session = Session()
  
    return session.query(providers).filter(providers.ident_fiscal==id_fiscal).first()
def get_clients():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(clients).all()
def get_client(RFC_clients):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(clients).filter(clients.RFC_clients==RFC_clients).first()
    
def get_pdfs():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(pdf).all()
def get_pdf(id_pdfs):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(pdf).filter(pdf.id_pdfs==id_pdfs).first()
def update_pdf(id_pdfs,status_pdfs):
    Session = sessionmaker(bind=engine)
    session = Session()
    temp = session.query(pdf).filter(pdf.id_pdfs==id_pdfs).first()
    temp.status_pdfs = status_pdfs
    session.commit()
    
    