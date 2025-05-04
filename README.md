# kiezen

An application for DJs to help them choose songs in their library.

## Project Structure

The project is organized into several components:

- `web/` - Vue.js web application
- `backend/` - Python backend service
- `mobile/` - Future mobile application
- `desktop/` - Future desktop application
- `shared/` - Shared code and utilities

## Features

- Add dummy (ghost) songs with metadata or links
- Mobile app for adding songs via share functionality
- Web interface with:
  - Song list management
  - Forms for adding new songs and dummy songs
  - Playlist management
  - Song deletion
  - Playlist creation and management

## Development Setup

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn

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

## License

[Add your license here]
