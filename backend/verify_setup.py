import os

def verify_setup():
    """Verify that all required files and directories exist"""
    
    print("🔍 Verifying project setup...\n")
    
    # Check directories
    directories = [
        'database',
        'song_features',
        'uploads',
        'app',
        'models',
        'utils'
    ]
    
    print("📁 Checking directories:")
    all_dirs_exist = True
    for directory in directories:
        exists = os.path.exists(directory)
        status = "✅" if exists else "❌"
        print(f"   {status} {directory}/")
        if not exists:
            all_dirs_exist = False
    print()
    
    # Check database file
    print("🗄️  Checking database:")
    db_exists = os.path.exists('database/songs.db')
    status = "✅" if db_exists else "❌"
    print(f"   {status} database/songs.db")
    print()
    
    # Check Python files
    print("📝 Checking Python files:")
    files = [
        'models/database.py',
        'app/__init__.py',
        'models/__init__.py',
        'utils/__init__.py'
    ]
    
    all_files_exist = True
    for file in files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"   {status} {file}")
        if not exists:
            all_files_exist = False
    print()
    
    # Final verdict
    if all_dirs_exist and all_files_exist and db_exists:
        print("✅ Setup verification PASSED! You're ready to go!")
    else:
        print("❌ Setup verification FAILED. Please run setup.py again.")
        return False
    
    return True

if __name__ == "__main__":
    verify_setup()