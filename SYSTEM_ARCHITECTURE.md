# SYSTEM ARCHITECTURE

## 1. System Overview
This document defines the architecture for a high-fidelity 3D Gaussian Splatting (3DGS) simulation platform. The system leverages the Gemini API for multimodal reasoning (text + image interpretation) and orchestrates a dedicated 3DGS engine to achieve "World Labs Marble" quality outputs.

## 2. Core Components
- **Frontend (Client)**: React.js application utilizing React Three Fiber and a WebGL 3DGS renderer (e.g., `mkkellogg/GaussianSplats3D`).
- **Backend (API Gateway)**: Python FastAPI server.
- **AI Reasoning Layer**: Google Gemini API for spatial reasoning, layout planning, and prompt enhancement.
- **3D Generation Engine**: Dedicated 3DGS model API (e.g., Luma AI, Tripo3D, or self-hosted LRM) to generate `.ply` files from Gemini's structured outputs.
- **Storage**: Blob storage for persisting uploaded images and generated `.ply` splat files.

## 3. Data Models & Schema
```typescript
interface WorldEntity {
  id: string; // UUID
  prompt: string;
  original_image_url?: string;
  spatial_layout: Record<string, any>; // JSON structured by Gemini
  gs_ply_url?: string;
  status: 'PENDING' | 'ANALYZING' | 'GENERATING' | 'READY' | 'FAILED';
  created_at: Date;
}
```

## 4. State Management
- **Client-Side**: Zustand for UI state management. React Query for handling API requests and polling for generation status.
- **Server-Side**: Redis + Celery for managing long-running 3D generation tasks asynchronously without blocking the main API threads.

## 5. Directory Structure
```text
/3d_sim_project
├── /src
│   ├── /backend
│   │   ├── api/
│   │   ├── services/
│   │   │   ├── gemini_service.py
│   │   │   └── gs_engine.py
│   │   └── main.py
│   ├── /frontend
│   │   ├── /components
│   │   │   ├── SplatViewer.jsx
│   │   │   └── GeneratorForm.jsx
│   │   └── App.jsx
└── /config
```

## 6. Security & Infrastructure Layers
- **API Security**: Token-based authentication, strict rate limiting to protect Gemini API quotas.
- **Data Integrity**: File upload validation (size limits, MIME type verification for images).
- **CORS**: Restricted origins configured on the FastAPI gateway.
