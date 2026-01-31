from models.database import engine, Base

def init_db():
    """Initialize the database"""
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()