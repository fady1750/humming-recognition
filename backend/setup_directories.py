import os

# List of directories to create
DIRECTORIES = [
    'database',
    'song_features',
    'uploads',
    'app',
    'models',
    'utils'
]

def setup_directories():
    """Create all required directories for the project"""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    print("\n✅ All directories created successfully!")

if __name__ == "__main__":
    setup_directories()