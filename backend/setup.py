import os
import sys

def create_directories():
    """Create all required directories"""
    directories = [
        'database',
        'song_features',
        'uploads',
        'app',
        'models',
        'utils'
    ]
    
    print("📁 Creating project directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}/")
    print()

def create_init_files():
    """Create __init__.py files for Python packages"""
    init_files = [
        'app/__init__.py',
        'models/__init__.py',
        'utils/__init__.py'
    ]
    
    print("📝 Creating __init__.py files...")
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"   ✅ {init_file}")
    print()

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    try:
        from models.database import Base, engine
        Base.metadata.create_all(engine)
        print("   ✅ Database initialized successfully!")
    except Exception as e:
        print(f"   ❌ Error initializing database: {e}")
        sys.exit(1)

def main():
    print("=" * 50)
    print("🎵 Humming Recognition System - Setup")
    print("=" * 50)
    print()
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Create __init__.py files
    create_init_files()
    
    # Step 3: Initialize database
    initialize_database()
    
    print()
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Add songs using: python add_song.py <audio_file> <title> <artist>")
    print("2. Start the server: python run.py")
    print()

if __name__ == "__main__":
    main()