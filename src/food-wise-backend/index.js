const app = require('./src/app');
const { sequelize } = require('./src/config/database');
const seedDatabase = require('./src/utils/seed');

const PORT = process.env.PORT || 3000;

async function connectWithRetry(retries = 5, delay = 3000) {
    try {
        console.log('Tentando conectar ao banco...');
        await sequelize.authenticate();
        console.log('Conectado ao banco com sucesso!');
        return true;
    } catch (error) {
        console.error(`Erro ao conectar ao banco: ${error.message}`);
        
        if (retries > 0) {
            console.log(`Tentando novamente em ${delay/1000}s... (${retries} tentativas restantes)`);
            await new Promise(resolve => setTimeout(resolve, delay));
            return connectWithRetry(retries - 1, delay);
        } else {
            throw new Error('Não foi possível conectar ao banco após várias tentativas.');
        }
    }
}

async function startServer() {
    try {
        await connectWithRetry();
        await sequelize.sync();
        await seedDatabase();

        app.listen(PORT, () => {
            console.log(`Servidor rodando na porta ${PORT}`);
        });
    } catch (error) {
        console.error('Falha ao inicializar o servidor:', error.message);
        process.exit(1);
    }
}

startServer();