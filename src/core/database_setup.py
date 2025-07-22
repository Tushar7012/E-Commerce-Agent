import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from log import logging
from exception import CustomException
Base = declarative_base()

class Product(Base):
    """Defines the 'products' table schema."""
    __tablename__ = 'products'
    
    sku = Column(String, primary_key=True, comment="Your unique product SKU")
    product_name = Column(String, nullable=False)
    my_cost = Column(Float, nullable=False, comment="The cost you pay for the product")
    
    competitors = relationship("Competitor", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(sku='{self.sku}', name='{self.product_name}')>"

class Competitor(Base):
    """Defines the 'competitors' table schema."""
    __tablename__ = 'competitors'
    
    id = Column(Integer, primary_key=True)
    competitor_name = Column(String, nullable=False)
    product_url = Column(String, nullable=False, unique=True, comment="Direct URL to competitor's product page")
    product_sku = Column(String, ForeignKey('products.sku'), nullable=False)
    
    # This links a competitor back to a single product
    product = relationship("Product", back_populates="competitors")

    def __repr__(self):
        return f"<Competitor(name='{self.competitor_name}', url='{self.product_url}')>"


def setup_database():
    """Connects to the database and creates tables if they don't exist."""
    try:
        load_dotenv()
        db_path = os.getenv("DATABASE_PATH")
        
        if not db_path:
            raise ValueError("DATABASE_PATH not found in your .env file.")

        # Ensure the 'data' directory exists before creating the database file
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        database_url = f"sqlite:///{db_path}"
        engine = create_engine(database_url)
        
        logging.info("Connecting to the database...")
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully (if they didn't already exist).")

    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    setup_database()