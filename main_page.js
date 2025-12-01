document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotContainer = document.querySelector('.chatbot-container');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSendBtn = document.getElementById('chatbot-send-btn');
    const chatbotMessages = document.getElementById('chatbot-messages');

    const API_URL = 'http://localhost:5000/api';

    // Open chatbot
    chatbotToggle.addEventListener('click', function() {
        chatbotContainer.classList.add('active');
        chatbotToggle.classList.add('active');
        chatbotInput.focus();
    });

    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotContainer.classList.remove('active');
        chatbotToggle.classList.remove('active');
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && chatbotContainer.classList.contains('active')) {
            chatbotContainer.classList.remove('active');
            chatbotToggle.classList.remove('active');
        }
    });

    // Send message
    chatbotSendBtn.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = chatbotInput.value.trim();
        
        if (message === '') return;

        // Add user message
        addMessage(message, 'user-message');
        chatbotInput.value = '';

        try {
            // Send to Python backend
            const response = await fetch(`${API_URL}/chatbot`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                addMessage(data.message, 'bot-message');
            } else {
                addMessage('Sorry, something went wrong. Please try again.', 'bot-message');
            }
        } catch (error) {
            console.error('Error:', error);
            // Fallback to local response if backend is unavailable
            addMessage(getBotResponse(message), 'bot-message');
        }
    }

    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${className}`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Fallback function if backend is unavailable
    function getBotResponse(userMessage) {
        const message = userMessage.toLowerCase();

        if (message.includes('hello') || message.includes('hi')) {
            return 'Hello! 👋 What can I help you with today?';
        } else if (message.includes('product') || message.includes('item')) {
            return 'We have a wide range of fashion items. Check out our New Arrivals section! 👗👔';
        } else if (message.includes('price') || message.includes('cost')) {
            return 'Our prices range from $45 to $150. We offer great quality at affordable prices! 💰';
        } else if (message.includes('delivery') || message.includes('shipping')) {
            return 'We offer fast and reliable shipping. Your order will arrive within 5-7 business days. 📦';
        } else if (message.includes('return') || message.includes('refund')) {
            return 'We have a 30-day return policy. If you\'re not satisfied, we\'ll make it right! ✅';
        } else if (message.includes('size') || message.includes('fit')) {
            return 'Please refer to our size guide on the product pages. Feel free to contact us for more details! 📏';
        } else if (message.includes('contact') || message.includes('support')) {
            return 'You can reach our support team at support@fashion-freek.com or call us at 1-800-FASHION. 📞';
        } else if (message.includes('sale') || message.includes('discount')) {
            return 'Check out our latest offers in the New Arrivals section! Subscribe to get exclusive deals. 🎉';
        } else {
            return 'Thanks for your message! Our team will get back to you soon. Is there anything else I can help you with?';
        }
    }
});
async function sendMessageToChatbot(message) {
  const response = await fetch('/chatbot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  });
  const data = await response.json();
  // Process the response, update chat UI
  console.log(data);
}
