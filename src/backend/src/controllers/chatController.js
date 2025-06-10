const ChatMessage = require('../models/ChatMessage');
const { Op } = require('sequelize');

class ChatController {
    async saveMessage(req, res) {
        try {
            const { module } = req.params;
            const { role, content, userId, context, sessionId } = req.body;

            const message = await ChatMessage.create({
                userId: userId || 'anonymous',
                module,
                role,
                content,
                context,
                sessionId
            });

            res.status(201).json({
                success: true,
                message: {
                    id: message.id,
                    role: message.role,
                    content: message.content,
                    timestamp: message.timestamp,
                    context: message.context
                }
            });
        } catch (error) {
            console.error('Error saving message:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to save message'
            });
        }
    }

    async getMessages(req, res) {
        try {
            const { module } = req.params;
            const { userId, sessionId, limit = 50 } = req.query;

            const whereClause = { module };
            
            if (userId) {
                whereClause.userId = userId;
            }
            
            if (sessionId) {
                whereClause.sessionId = sessionId;
            }

            const messages = await ChatMessage.findAll({
                where: whereClause,
                order: [['timestamp', 'ASC']],
                limit: parseInt(limit),
                attributes: ['id', 'role', 'content', 'timestamp', 'context']
            });

            res.json({
                success: true,
                messages: messages
            });
        } catch (error) {
            console.error('Error fetching messages:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch messages'
            });
        }
    }

    async getContext(req, res) {
        try {
            const { module } = req.params;
            const { userId, sessionId, maxMessages = 10 } = req.query;

            const whereClause = { module };
            
            if (userId) {
                whereClause.userId = userId;
            }
            
            if (sessionId) {
                whereClause.sessionId = sessionId;
            }

            const recentMessages = await ChatMessage.findAll({
                where: whereClause,
                order: [['timestamp', 'DESC']],
                limit: parseInt(maxMessages),
                attributes: ['role', 'content', 'timestamp']
            });

            const context = recentMessages.reverse();

            res.json({
                success: true,
                context: context,
                count: context.length
            });
        } catch (error) {
            console.error('Error fetching context:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch context'
            });
        }
    }

    async clearMessages(req, res) {
        try {
            const { module } = req.params;
            const { userId, sessionId } = req.query;

            const whereClause = { module };
            
            if (userId) {
                whereClause.userId = userId;
            }
            
            if (sessionId) {
                whereClause.sessionId = sessionId;
            }

            await ChatMessage.destroy({
                where: whereClause
            });

            res.json({
                success: true,
                message: 'Messages cleared successfully'
            });
        } catch (error) {
            console.error('Error clearing messages:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to clear messages'
            });
        }
    }

    async clearAllMessages(req, res) {
        try {
            const { userId, sessionId } = req.query;

            const whereClause = {};
            
            if (userId) {
                whereClause.userId = userId;
            }
            
            if (sessionId) {
                whereClause.sessionId = sessionId;
            }

            await ChatMessage.destroy({
                where: whereClause
            });

            res.json({
                success: true,
                message: 'All messages cleared successfully'
            });
        } catch (error) {
            console.error('Error clearing all messages:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to clear all messages'
            });
        }
    }
}

module.exports = new ChatController();