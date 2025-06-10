const sequelize = require('../config/database');
const Client = require('../models/Client');

async function seedDatabase() {
    try {
        await sequelize.authenticate();
        console.log('✅ Database conectada!');
        
        const existingClients = await Client.findAll();
        
        if (existingClients.length === 0) {
            console.log('📝 Criando clientes iniciais...');
            
            await Client.bulkCreate([
                { name: 'Sam', passkey: '333' },
                { name: 'Dean', passkey: '616' },
                { name: 'Castiel', passkey: '777' }
            ]);
            
            console.log('✅ Clientes criados com sucesso!');
        } else {
            console.log('ℹ️  Clientes já existem, pulando a criação...');
        }
        
        const allClients = await Client.findAll();
        console.log('📊 Current clients in database:');
        allClients.forEach(client => {
            console.log(`   - ID: ${client.id}, Name: ${client.name}`);
        });
        
    } catch (error) {
        console.error('❌ Erro ao criar seeds:', error);
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