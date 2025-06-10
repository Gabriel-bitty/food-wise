const sequelize = require('../config/database');
const Client = require('../models/Client');

const seedData = {
    clients: [
        {
            name: 'Dean',
            passkey: '616'
        }
    ]
};

async function seedDatabase() {
    try {
        await sequelize.authenticate();
        console.log('✅ Database conectada!');
        
        // Seed Clients
        console.log('👥 Semeando clientes...');
        
        for (const clientData of seedData.clients) {
            const existingClient = await Client.findOne({
                where: { name: clientData.name }
            });
            
            if (!existingClient) {
                await Client.create(clientData);
                console.log(`   ✓ Created client: ${clientData.name}`);
            } else {
                console.log(`   ℹ️  Cliente '${clientData.name}' já existe...`);
            }
        }

        console.log('✅ Semeado com sucesso!');

        const allClients = await Client.findAll({
            attributes: ['id', 'name']
        });
        
        console.log('📊 Current clients in database:');
        allClients.forEach(client => {
            console.log(`   - ID: ${client.id}, Name: ${client.name}, Created: ${client.created_at}`);
        });
        
    } catch (error) {
        console.error('❌ Erro:', error.message);
        throw error;
    }
}

module.exports = seedDatabase;
if (require.main === module) {
    seedDatabase()
        .then(() => {
            console.log('🎯 Processo concluído');
            process.exit(0);
        })
        .catch((error) => {
            console.error('💥 Erro no processo :', error);
            process.exit(1);
        });
}