# 🎨 Volcengine Image Generator

A complete, production-ready Docker application for AI image generation using Volcengine's Visual Intelligence API. Create stunning images from text descriptions or transform existing images with state-of-the-art AI technology.

![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)

## ✨ Features

### 🖼️ Text-to-Image Generation
- Generate images from detailed text prompts
- Support for negative prompts to exclude unwanted elements
- Multiple style presets (Anime, Photographic, Digital Art, etc.)
- Batch generation (up to 4 images at once)
- Customizable parameters (size, steps, CFG scale, seed)

### 🎨 Image-to-Image Transformation
- Transform existing images with AI
- Adjustable transformation strength
- Style transfer capabilities
- Same powerful controls as text-to-image

### 📚 History Management
- Browse all your generated images
- View generation parameters
- Download images individually or in bulk
- Copy prompts for reuse

### 💎 Beautiful UI
- Modern, responsive interface built with Vue 3 and Element Plus
- Dark theme optimized for visual work
- Smooth animations and transitions
- Real-time task progress monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Nginx (Port 3000)                  │
│        Static Files + Reverse Proxy             │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼─────┐   ┌─────▼──────┐
│  Frontend  │   │   Backend  │
│  (Vue 3)   │   │  (FastAPI) │
│            │   │  Port 8000 │
└────────────┘   └─────┬──────┘
                       │
                ┌──────▼──────────┐
                │  Volcengine API │
                │  Image Service  │
                └─────────────────┘
```

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Volcengine account with Visual Intelligence API access (optional for demo mode)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd volcengine-image-generator
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Volcengine credentials (optional - works in demo mode without credentials):

```env
VOLCENGINE_ACCESS_KEY=your_access_key_here
VOLCENGINE_SECRET_KEY=your_secret_key_here
VOLCENGINE_REGION=cn-beijing
```

**Note:** If you don't provide credentials, the application will run in demo mode using placeholder images.

### 3. Start the Application

```bash
docker-compose up -d
```

This will:
- Build the backend service (FastAPI)
- Build the frontend service (Vue 3)
- Set up Nginx reverse proxy
- Start all services

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

## 📖 Usage Guide

### Text-to-Image Generation

1. Navigate to **Text to Image** page
2. Enter your prompt (e.g., "A serene mountain landscape at sunset")
3. Optionally add a negative prompt (e.g., "blurry, low quality")
4. Adjust parameters:
   - **Width/Height**: Image dimensions (64-2048px)
   - **Steps**: Sampling steps (10-100, higher = better quality)
   - **CFG Scale**: Prompt adherence (1-20, higher = stricter)
   - **Seed**: For reproducible results (-1 for random)
   - **Style Preset**: Choose an art style
   - **Number of Images**: Generate 1-4 images
5. Click **Generate Image**
6. Wait for processing (typically 10-30 seconds)
7. Download or view your generated images

### Image-to-Image Transformation

1. Navigate to **Image to Image** page
2. Upload an image (drag & drop or click)
3. Enter transformation prompt
4. Adjust **Strength** (0-1, higher = more transformation)
5. Configure other parameters as needed
6. Click **Transform Image**

### Viewing History

1. Navigate to **History** page
2. Browse all your generated images
3. Click images to view in full size
4. Copy prompts or download images

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VOLCENGINE_ACCESS_KEY` | Your Volcengine access key | - |
| `VOLCENGINE_SECRET_KEY` | Your Volcengine secret key | - |
| `VOLCENGINE_REGION` | API region | `cn-beijing` |
| `DEFAULT_WIDTH` | Default image width | `512` |
| `DEFAULT_HEIGHT` | Default image height | `512` |
| `DEFAULT_STEPS` | Default sampling steps | `20` |
| `MAX_BATCH_SIZE` | Max images per request | `4` |
| `MAX_HISTORY_SIZE` | Max history entries | `1000` |

### Custom Port Configuration

Edit `docker-compose.yml` to change ports:

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Change 8080 to your preferred port
```

## 🛠️ Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/generate/text2image` - Generate image from text
- `POST /api/v1/generate/image2image` - Transform image
- `GET /api/v1/tasks/{task_id}` - Check task status
- `GET /api/v1/tasks/history` - Get generation history
- `GET /health` - Health check

## 📦 Project Structure

```
volcengine-image-generator/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry
│   │   ├── config.py        # Configuration
│   │   ├── schemas.py       # Pydantic models
│   │   ├── routers/         # API routes
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Vue 3 frontend
│   ├── src/
│   │   ├── views/           # Pages
│   │   ├── components/      # Vue components
│   │   ├── api/             # API client
│   │   └── styles/          # Styles
│   ├── Dockerfile
│   └── package.json
├── nginx/                    # Nginx configuration
│   ├── Dockerfile
│   └── nginx.conf
├── docs/                     # Documentation
│   └── RESEARCH_PLAN.md     # Technical design doc
├── docker-compose.yml        # Docker orchestration
├── .env.example             # Environment template
└── README.md
```

## 🔒 Security Considerations

- Never commit `.env` file with real credentials
- Use HTTPS in production
- Implement rate limiting for public deployments
- Set appropriate CORS origins in production
- Consider adding authentication for multi-user deployments

## 🚀 Deployment

### Production Deployment

1. Set up a server with Docker and Docker Compose
2. Clone the repository
3. Configure production environment variables
4. Use a production-ready `.env` file
5. Set up SSL/TLS with Let's Encrypt
6. Configure firewall rules
7. Start services:

```bash
docker-compose up -d
```

### Scaling

For high-traffic deployments:
- Use Kubernetes for orchestration
- Add Redis for task queue
- Implement horizontal scaling for backend
- Use CDN for static assets
- Set up load balancing

## 🐛 Troubleshooting

### Images Not Generating

1. Check if Volcengine credentials are correct
2. Verify API quota/limits
3. Check backend logs: `docker-compose logs backend`

### Frontend Not Loading

1. Check if backend is running: `docker-compose ps`
2. Verify nginx configuration
3. Check frontend logs: `docker-compose logs frontend`

### Port Conflicts

If port 3000 or 8000 is already in use:

```bash
docker-compose down
# Edit docker-compose.yml to change ports
docker-compose up -d
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- [Volcengine](https://www.volcengine.com/) for the powerful Image Generation API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent backend framework
- [Vue.js](https://vuejs.org/) for the progressive frontend framework
- [Element Plus](https://element-plus.org/) for beautiful UI components

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the [Research Plan](docs/RESEARCH_PLAN.md) for technical details
- Review API documentation at `/docs` endpoint

## 🎉 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built with ❤️ for the AI art community**
