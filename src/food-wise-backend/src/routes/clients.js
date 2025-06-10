const express = require('express');
const router = express.Router();
const clientController = require('../controllers/clientController');

// Route to create a new client
router.post('/', clientController.createClient);

// Route to retrieve all clients
router.get('/', clientController.getAllClients);

// Route to retrieve a specific client by ID
router.get('/:id', clientController.getClientById);

module.exports = router;