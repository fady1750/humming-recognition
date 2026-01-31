from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Add FFmpeg to PATH for this application
    ffmpeg_bin = r'C:\ffmpeg\bin'
    os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ.get('PATH', '')
    print(f"✅ FFmpeg path added: {ffmpeg_bin}")
    
    # Enable CORS
    CORS(app)
    
    # Configuration
    app.config.from_object('app.config.Config')
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app