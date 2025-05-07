# Kiezen

An application for DJs to help them choose songs in their library. This project aims to provide a comprehensive solution for managing and organizing music collections across multiple platforms.

## Project Overview

Kiezen is a multi-platform application that helps DJs manage their music library efficiently. It provides features for organizing songs, creating playlists, and managing metadata across web, mobile, and desktop platforms.

## Project Structure

The project is organized into several components:

- `web/` - Vue.js web application
  - Modern, responsive web interface
  - Song management and playlist creation
  - File upload and metadata management
  
- `backend/` - Python FastAPI backend service
  - RESTful API endpoints
  - File storage and management
  - Database operations
  
- `mobile/` - Future mobile application
  - Native mobile experience
  - Share functionality for adding songs
  - Offline support
  
- `desktop/` - Future desktop application
  - Native desktop experience
  - Local file system integration
  - System tray integration
  
- `shared/` - Shared code and utilities
  - Common types and interfaces
  - Shared components
  - Utility functions

## Features

### Current Features
- Song management
  - Add and remove songs
  - Upload music files
  - Add dummy (ghost) songs with metadata
  - Basic metadata management

### Planned Features
- Playlist management
- Advanced search and filtering
- Song metadata extraction
- Cross-platform synchronization
- Mobile share functionality
- Desktop integration
- Offline support

## Development Setup

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn
- Git

### Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/kiezen.git
cd kiezen
```

2. Install dependencies:
```sh
# Install root dependencies
npm install

# Install web app dependencies
cd web
npm install
```

### Development

#### Web Application
```sh
# From the root directory
npm run dev:web

# Or from the web directory
cd web
npm run dev
```

#### Backend
```sh
cd backend
# Setup Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the backend server
python src/main.py
```

### Building for Production

```sh
# Build web application
npm run build:web
```

## Project Status

The project is currently in active development. See the [tasks.md](docs/tasks.md) file for current and planned tasks.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

[Add your license here]

## Contact

[Add contact information here]
