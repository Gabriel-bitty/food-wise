require('dotenv').config();
const express = require('express');
const cors = require('cors');
const clientRoutes = require('./routes/clients');
const chatRoutes = require('./routes/chat');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/clients', clientRoutes);
app.use('/api/chat', chatRoutes); // para quanto ter

app.get('/', (req, res) => {
    res.json({ Message: 'Backend Funcionando' });
});

module.exports = app;