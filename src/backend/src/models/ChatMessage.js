const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const ChatMessage = sequelize.define('ChatMessage', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    userId: {
        type: DataTypes.STRING,
        allowNull: false,
        field: 'user_id'
    },
    module: {
        type: DataTypes.ENUM('fichasTecnicas', 'logomarca', 'mockups'),
        allowNull: false
    },
    role: {
        type: DataTypes.ENUM('user', 'assistant'),
        allowNull: false
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    context: {
        type: DataTypes.JSON,
        allowNull: true
    },
    timestamp: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    sessionId: {
        type: DataTypes.STRING,
        allowNull: true,
        field: 'session_id'
    }
}, {
    tableName: 'chat_messages',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
});

module.exports = ChatMessage;