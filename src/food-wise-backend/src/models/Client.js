const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database'); // Should destructure

const Client = sequelize.define('Client', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    name: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    passkey: {
        type: DataTypes.STRING,
        allowNull: false
    }
});

module.exports = Client;