require('dotenv').config();
const express = require('express');
const cors = require('cors');
const clientRoutes = require('./routes/clients');
const chatRoutes = require('./routes/chat');

const app = express();

// Middleware
app.use(cors({
    origin: ['http://localhost:8501', 'http://localhost:3000'], 
    credentials: true
}));
app.use(express.json());


// Rotas
app.use('/api/clients', clientRoutes);
app.use('/api/chat', chatRoutes);

app.get('/', (req, res) => {
    res.json({ 
        message: 'Food Wise Backend API',
        version: '1.0.0',
        endpoints: {
            clients: '/api/clients',
            chat: '/api/chat'
        }
    });
});

app.use((err, req, res, next) => {
    console.error('❌ Error:', err.stack);
    res.status(500).json({
        success: false,
        error: 'Erro servidor',
        message: err.message
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        success: false,
        error: 'Nao encontrado',
        path: req.originalUrl
    });
});

module.exports = app;