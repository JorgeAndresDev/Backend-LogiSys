from sqlalchemy import Column, BigInteger, String
from database.base_class import Base

class Cashless(Base):
    __tablename__ = "tbl_cashless"

    codigo = Column(BigInteger, primary_key=True, index=True)
    cliente = Column(String(255), nullable=False)
    dt = Column(BigInteger, nullable=False)
    placa = Column(String(20), nullable=False)
    numero = Column(BigInteger, nullable=False)
    novedad = Column(String(255), nullable=True)
