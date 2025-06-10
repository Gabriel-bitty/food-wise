const app = require('./src/app');
const sequelize = require('./src/config/database');
const seedDatabase = require('./src/scripts/seed');

const PORT = process.env.PORT || 3000;

async function startServer() {
    try {
        console.log('🚀 Starting Food Wise Backend...');
        
        // Test database connection
        console.log('📡 Conectando ao banco de dados...');
        await sequelize.authenticate();
        console.log('✅ Conexão com o banco de dados estabelecida com sucesso.');

        // Sync database models (create tables if they don't exist)
        console.log('🔄 Sincronizando o banco de dados...');
        await sequelize.sync({ alter: true });
        console.log('✅ Banco de dados sincronizado com sucesso.');

        // Run seed data (only creates if doesn't exist)
        console.log('🌱 Verificando seeds...');
        await seedDatabase();
        
        app.listen(PORT, () => {
            console.log(`🎯 Server running on http://localhost:${PORT}`);
            console.log('');
            console.log('👤 Cliente Seeded:');
            console.log('Name: Dean');
            console.log('Passkey: 616');
        });
        
    } catch (error) {
        console.error('❌ Falha ao iniciar o servidor:', error);
        console.error('🔍 Verificando conexão com o banco de dados...');

        try {
            await sequelize.authenticate();
            console.log('✅ Conexão com o banco de dados está funcionando');
        } catch (dbError) {
            console.error('❌ Falha na conexão com o banco de dados:', dbError.message);

            if (dbError.code === 'ER_ACCESS_DENIED_ERROR') {
                console.error('🔐 Verifique suas credenciais do MySQL no arquivo .env');
            } else if (dbError.code === 'ECONNREFUSED') {
                console.error('🔌 Certifique-se de que o servidor MySQL está em execução');
            }
        }
        
        process.exit(1);
    }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n🛑 Encerrando o servidor...');
    try {
        await sequelize.close();
        console.log('✅ Conexão com o banco de dados fechada.');
        process.exit(0);
    } catch (error) {
        console.error('❌ Erro durante o encerramento:', error);
        process.exit(1);
    }
});

startServer();