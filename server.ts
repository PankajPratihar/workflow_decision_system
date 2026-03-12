import express from 'express';
import { createServer as createViteServer } from 'vite';
import path from 'path';
import { workflowEngine } from './src/engine';
import { WorkflowRequest } from './src/types';

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Routes
  app.post('/api/workflow/process', async (req, res) => {
    try {
      const request: WorkflowRequest = req.body;
      
      // Basic validation
      if (!request.requestId || !request.workflowId || !request.payload) {
        return res.status(400).json({ error: 'Missing required fields: requestId, workflowId, payload' });
      }

      const result = await workflowEngine.processRequest(request);
      res.json(result);
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  });

  app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Workflow Decision Platform running on http://localhost:${PORT}`);
  });
}

startServer();
