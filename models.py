from dataclasses import dataclass
from sqlalchemy import Column, Date, Integer, String,VARCHAR

from db import Base

@dataclass
class providers(Base):
    __tablename__ = "provedores"
    id_fiscal=Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    ident_fiscal = Column(VARCHAR)
@dataclass
class clients(Base):
    __tablename__ = "clients"
    RFC_clients=Column(VARCHAR(50), primary_key=True)
    Name_clients = Column(VARCHAR(50))

print(providers)
    