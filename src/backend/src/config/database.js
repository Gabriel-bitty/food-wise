require('dotenv').config();
const { Sequelize } = require('sequelize');
const path = require('path');

const getDatabaseConfig = () => {
    if (process.env.DB_HOST && process.env.DB_NAME) {
        return {
            database: process.env.DB_NAME,
            username: process.env.DB_USER || 'root',
            password: process.env.DB_PASSWORD || '',
            host: process.env.DB_HOST || 'localhost',
            port: parseInt(process.env.DB_PORT) || 3306,
            dialect: 'mysql',
            logging: false,
            pool: {
                max: parseInt(process.env.DB_POOL_MAX) || 5,
                min: parseInt(process.env.DB_POOL_MIN) || 0,
                acquire: parseInt(process.env.DB_POOL_ACQUIRE) || 30000,
                idle: parseInt(process.env.DB_POOL_IDLE) || 10000
            },
            dialectOptions: {
                charset: 'utf8mb4',
                timezone: process.env.DB_TIMEZONE || '+00:00',
                ...(process.env.NODE_ENV === 'production' && {
                    ssl: {
                        require: true,
                        rejectUnauthorized: false
                    }
                })
            },
            define: {
                charset: 'utf8mb4',
                collate: 'utf8mb4_unicode_ci'
            }
        };
    }
    
    console.log('⚠️  No MySQL environment variables found, using SQLite fallback');
    return {
        dialect: 'sqlite',
        storage: path.join(__dirname, '..', 'database.sqlite'),
        logging: process.env.NODE_ENV === 'development' ? console.log : false
    };
};

const config = getDatabaseConfig();
let sequelize;

if (config.dialect === 'mysql') {
    sequelize = new Sequelize(config.database, config.username, config.password, {
        host: config.host,
        port: config.port,
        dialect: config.dialect,
        logging: config.logging,
        pool: config.pool,
        dialectOptions: config.dialectOptions,
        define: {
            timestamps: true,
            createdAt: 'created_at',
            updatedAt: 'updated_at',
            ...config.define
        }
    });
} else {
    sequelize = new Sequelize({
        dialect: config.dialect,
        storage: config.storage,
        logging: config.logging,
        define: {
            timestamps: true,
            createdAt: 'created_at',
            updatedAt: 'updated_at'
        }
    });
}

const testConnection = async () => {
    try {
        await sequelize.authenticate();
        
        if (config.dialect === 'mysql') {
            console.log(`✅ MySQL connection established successfully`);
            console.log(`🔗 Connected to: ${config.host}:${config.port}/${config.database}`);
            console.log(`👤 User: ${config.username}`);
        } else {
            console.log('✅ SQLite connection established successfully');
        }
        
        return true;
    } catch (error) {
        console.error('❌ Unable to connect to the database:', error.message);
        
        if (config.dialect === 'mysql') {
            console.error('🔍 MySQL Connection Details:');
            console.error(`   Host: ${config.host}`);
            console.error(`   Port: ${config.port}`);
            console.error(`   Database: ${config.database}`);
            console.error(`   User: ${config.username}`);
            console.error('💡 Please check your .env file and MySQL server status');
        }
        
        return false;
    }
};


const getDatabaseInfo = () => {
    return {
        dialect: config.dialect,
        host: config.dialect === 'mysql' ? config.host : 'local',
        database: config.dialect === 'mysql' ? config.database : 'sqlite',
        connected: false // 
    };
};

module.exports = sequelize;
module.exports.testConnection = testConnection;
module.exports.getDatabaseInfo = getDatabaseInfo;