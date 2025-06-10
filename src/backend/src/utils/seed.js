const { sequelize } = require('../config/database'); // Should destructure
const Client = require('../models/Client');

const seedDatabase = async () => {
    try {
        await sequelize.sync(); // Create tables if they don't exist
        
        // Simple seed - create client if it doesn't exist
        const [client, created] = await Client.findOrCreate({
            where: { name: 'Cliente' },
            defaults: {
                name: 'Cliente',
                passkey: '12345'
            }
        });

        if (created) {
            console.log('Seed client created successfully:', client.name);
        } else {
            console.log('Seed client already exists:', client.name);
        }
    } catch (error) {
        console.error('Error seeding database:', error);
    }
};

module.exports = seedDatabase;