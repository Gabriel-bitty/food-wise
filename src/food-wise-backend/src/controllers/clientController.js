const Client = require('../models/Client');

const clientController = {
    // Get all clients
    async getAllClients(req, res) {
        try {
            const clients = await Client.findAll({
                attributes: ['id', 'name'] // Don't expose passkey
            });
            res.json(clients);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Verify client credentials
    async verifyClient(req, res) {
        try {
            const { name, passkey } = req.body;
            
            const client = await Client.findOne({
                where: { name, passkey }
            });

            if (client) {
                res.json({ 
                    success: true, 
                    client: { id: client.id, name: client.name } 
                });
            } else {
                res.status(401).json({ 
                    success: false, 
                    message: 'Invalid credentials' 
                });
            }
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Create a new client
    async createClient(req, res) {
        try {
            const { name, passkey } = req.body;
            const client = await Client.create({ name, passkey });
            res.status(201).json({ 
                id: client.id, 
                name: client.name 
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Get client by ID
    async getClientById(req, res) {
        try {
            const { id } = req.params;
            const client = await Client.findByPk(id, {
                attributes: ['id', 'name']
            });
            
            if (client) {
                res.json(client);
            } else {
                res.status(404).json({ error: 'Client not found' });
            }
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = clientController;