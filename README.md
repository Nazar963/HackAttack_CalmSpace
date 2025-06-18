# Audio Processing Hack Attack Project

A multi-container application for real-time audio recording, processing, and analysis. The system captures audio from the browser, processes it through a Flask-based AI service, and provides audio loudness analysis with a normalized decibel level output.

## 🏗️ Architecture Overview

This project consists of three main components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Vue.js FE     │◄──►│   Laravel BE    │◄──►│   Flask API     │
│   (Port 5173)   │    │   (Port 8000)   │    │   (Port 5000)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      Frontend              Backend              Audio Processing
   - Vue 3 + Vite         - Laravel 10         - Python Flask
   - Audio Recording      - File Handling      - Audio Analysis
   - UI Components        - API Gateway        - NumPy/Pydub
```

### Components

1. **Frontend (FE)** - Vue.js 3 application with Vite
   - Real-time audio recording using WebRTC
   - Audio format conversion (WebM → WAV)
   - Bootstrap-based responsive UI
   - Axios for HTTP communication

2. **Backend (BE)** - Laravel 10 application
   - RESTful API endpoints
   - File upload handling
   - Proxy service to Flask API
   - CSRF protection

3. **Audio Processing API (BE-api)** - Flask Python service
   - Audio signal processing
   - Decibel level calculation
   - Audio format support via Pydub
   - Comprehensive logging

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js (for local development)
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:Nazar963/HackAttack_CalmSpace.git
   cd HackAttack_CalmSpace
   ```

2. **Install frontend dependencies** (recommended)
   ```bash
   cd FE
   npm install
   cd ..
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Laravel Backend: http://localhost:8000
   - Flask API: http://localhost:5000

### Laravel Permissions Fix (if needed)
```bash
sudo chown -R $(whoami):www-data BE/storage BE/bootstrap/cache
sudo chmod -R 775 BE/storage BE/bootstrap/cache
```

## 📋 Available Commands

### Docker Management
```bash
# Start all containers
docker-compose up --build

# Stop all containers
docker-compose down

# View container status
docker-compose ps

# View logs
docker-compose logs [service-name]

# Clean up (remove images)
docker-compose down --rmi all
```

### Development
```bash
# Frontend development (in FE directory)
npm install
npm run dev
npm run build

# Laravel backend (in BE directory)
composer install
php artisan serve
```

## 🔧 Technical Details

### Frontend Technologies
- **Vue.js 3** with Composition API
- **Vite** for fast development and building
- **Bootstrap Vue Next** for UI components
- **Axios** for HTTP requests
- **WaveFile** for audio format conversion
- **WebRTC MediaRecorder API** for audio capture

### Backend Technologies
- **Laravel 10** (PHP framework)
- **Guzzle HTTP** for external API calls
- **CORS** support for cross-origin requests

### Audio Processing API
- **Flask** (Python web framework)
- **Pydub** for audio manipulation
- **NumPy** for numerical computations
- **CORS** enabled for cross-origin requests

### Audio Processing Logic

The Flask API performs the following audio analysis:

1. **Audio Reception**: Receives WAV files via multipart form upload
2. **Signal Processing**: Converts audio samples to PCM data
3. **Decibel Calculation**: Computes average dB level using the formula:
   ```
   dB = 20 * log10(|amplitude| + ε)
   ```
4. **Normalization**: Maps dB values from [-200, 0] range to [0, 100] scale
5. **Response**: Returns normalized loudness level as JSON

## 📡 API Endpoints

### Laravel Backend (Port 8000)
- `POST /process-data` - Upload audio file for processing
- `GET /csrf-token` - Get CSRF token for secure requests
- `GET /` - Welcome page

### Flask API (Port 5000)
- `POST /process-data` - Direct audio processing endpoint

### Request/Response Format

**Request:**
```http
POST /process-data
Content-Type: multipart/form-data

file: [audio file in WAV format]
```

**Response:**
```json
{
  "average_db": 45.7,
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Audio processing failed: [error details]"
}
```

## 🎵 Audio Processing Features

- **Real-time Recording**: Browser-based audio capture
- **Format Conversion**: Automatic WebM to WAV conversion
- **Loudness Analysis**: Scientific dB level calculation
- **Normalization**: User-friendly 0-100 scale output
- **Error Handling**: Comprehensive error reporting
- **Logging**: Detailed processing logs for debugging

## 🛠️ Development Guide

### Project Structure
```
new_hackattack/
├── docker-compose.yml          # Multi-container orchestration
├── README.md                   # Basic setup instructions
├── BE/                         # Laravel backend
│   ├── app/Http/Controllers/   # API controllers
│   ├── app/Services/          # External service integrations
│   └── routes/                # API routes
├── BE-api/                    # Flask audio processing
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Python container config
└── FE/                        # Vue.js frontend
    ├── src/components/        # Vue components
    ├── src/axios-config.js    # HTTP client configuration
    └── package.json           # Node.js dependencies
```

### Key Files

#### Frontend
- `src/components/Record.vue` - Main audio recording component
- `src/axios-config.js` - HTTP client with CSRF configuration

#### Laravel Backend
- `app/Http/Controllers/DataController.php` - Processes file uploads
- `app/Services/FlaskServices.php` - Flask API integration
- `routes/web.php` - Web routes definition

#### Flask API
- `app.py` - Audio processing logic and API endpoints
- `requirements.txt` - Python package dependencies

### Environment Configuration

The application is configured for development with hardcoded localhost URLs. For production deployment:

1. Update axios configuration with production URLs
2. Configure environment variables for different stages
3. Implement proper secret management
4. Set up SSL/TLS certificates

## 🔍 Troubleshooting

### Common Issues

1. **Frontend container fails to start**
   - Run `npm install` in the FE directory
   - Check if port 5173 is available

2. **Laravel permission errors**
   - Run the permission fix commands above
   - Ensure Docker has proper file access

3. **Audio processing errors**
   - Check Flask API logs: `docker-compose logs flask`
   - Verify audio file format (should be WAV)
   - Ensure file size is reasonable (< 10MB recommended)

4. **CORS issues**
   - Verify CORS configuration in both Laravel and Flask
   - Check browser developer tools for specific errors

### Debug Information

View logs for debugging:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs frontend
docker-compose logs backend
docker-compose logs flask
```

## 🔐 Security Considerations

- CSRF protection enabled for Laravel routes
- File upload validation in place
- Error message sanitization to prevent information disclosure
- Temporary file cleanup after processing

## 📈 Performance Notes

- Audio files are processed in-memory for speed
- Temporary files are cleaned up immediately after processing
- Flask API includes comprehensive logging for performance monitoring
- Frontend uses efficient audio conversion libraries

## 🚧 Future Enhancements

- [ ] Add audio visualization during recording
- [ ] Implement audio file storage and history
- [ ] Add real-time audio streaming processing
- [ ] Include more audio analysis features (frequency, pitch, etc.)
- [ ] Add user authentication and session management
- [ ] Implement audio quality assessment
- [ ] Add support for multiple audio formats
- [ ] Create audio processing analytics dashboard

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request

## 📄 License

This project is created for educational and demonstration purposes.

---

**Note**: This is a development setup. For production deployment, additional security, performance, and monitoring configurations are recommended.
