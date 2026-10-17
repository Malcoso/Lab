
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import base
engine = create_engine('sqlite:///mydb.db',echo =True)
sessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False)
session=sessionLocal()

base.metadata.create_all(engine)
