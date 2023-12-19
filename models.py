from sqlalchemy import String, Integer, Column, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Car(Base):
    """
    Represents information about a car.

    Attributes:
        id (int): The unique identifier for the car.
        nama (str): The name of the car.
        jenis (str): The type of the car.
        merek (str): The brand or make of the car.
        model (str): The model of the car.
        tahun (int): The manufacturing year of the car.
        harga (float): The price of the car.
        konsumsi_bahan_bakar (float): The fuel consumption of the car.
        tingkat_kepentingan (int): The importance level of the car.
    """

    __tablename__ = 'Mobil'

    id: int = Column(Integer, primary_key=True, index=True)
    nama: str = Column(String, index=True)
    jenis: str = Column(String)
    merek: str = Column(String)
    model: str = Column(String)
    tahun: int = Column(Integer)
    harga: float = Column(Float)
    konsumsi_bahan_bakar: float = Column(Float)
    tingkat_kepentingan: int = Column(Integer)

    def __init__(self, nama, jenis, merek, model, tahun, harga, konsumsi_bahan_bakar, tingkat_kepentingan):
        self.nama = nama
        self.jenis = jenis
        self.merek = merek
        self.model = model
        self.tahun = tahun
        self.harga = harga
        self.konsumsi_bahan_bakar = konsumsi_bahan_bakar
        self.tingkat_kepentingan = tingkat_kepentingan

    def __repr__(self):
        return f"Mobil(id={self.id!r}, nama={self.nama!r}, jenis={self.jenis!r}, merek={self.merek!r}, model={self.model!r}, tahun={self.tahun!r}, harga={self.harga!r}, konsumsi_bahan_bakar={self.konsumsi_bahan_bakar!r}, tingkat_kepentingan={self.tingkat_kepentingan!r})"
