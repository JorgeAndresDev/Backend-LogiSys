from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database.base_class import Base

class SafeInspection(Base):
    __tablename__ = "inspeccion_cajas_fuertes"

    id = Column(Integer, primary_key=True, index=True)
    placa_vehiculo = Column(String(10), index=True, nullable=False)
    puerta_estado = Column(String(50), nullable=False)
    puerta_facilidad = Column(String(50), nullable=False)
    clave_precisa = Column(String(50), nullable=False)
    clave_autorizada = Column(String(50), nullable=False)
    perilla_funciona = Column(String(50), nullable=False)
    numeros_visibles = Column(String(50), nullable=False)
    caja_anclada = Column(String(50), nullable=False)
    observaciones = Column(Text, nullable=True)
    fecha_inspeccion = Column(DateTime(timezone=True), server_default=func.now())

class FirstAidInspection(Base):
    __tablename__ = "inspecciones_botiquines"

    id = Column(Integer, primary_key=True, index=True)
    placa_vehiculo = Column(String(10), index=True, nullable=False)
    gasas_limpias = Column(String(50))
    esparadrapo_tela = Column(String(50))
    baja_lenguas = Column(String(50))
    guantes_latex = Column(String(50))
    venda_elastica_2 = Column(String(50))
    venda_elastica_3 = Column(String(50))
    venda_elastica_5 = Column(String(50))
    venda_algodon = Column(String(50))
    yodopovidona = Column(String(50))
    solucion_salina = Column(String(50))
    termometro_digital = Column(String(50))
    alcohol_antiseptico = Column(String(50))
    botella_agua = Column(String(50))
    bandas_adhesivas = Column(String(50))
    tijeras_punta_roma = Column(String(50))
    pito_emergencias = Column(String(50))
    manual_primeros_auxilios = Column(String(50))
    observaciones = Column(Text)
    fecha_inspeccion = Column(DateTime(timezone=True), server_default=func.now())

