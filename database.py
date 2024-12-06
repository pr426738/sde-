from sqlalchemy import create_engine

def init_db():
    return create_engine('postgresql://username:password@localhost/railway')