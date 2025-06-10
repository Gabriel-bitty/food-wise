const express = require('express');
const router = express.Router();
const chatController = require('../controllers/chatController');

router.post('/:module/messages', chatController.saveMessage);
router.get('/:module/messages', chatController.getMessages);
router.get('/:module/context', chatController.getContext);
router.delete('/:module/messages', chatController.clearMessages);
router.delete('/messages', chatController.clearAllMessages);

module.exports = router;