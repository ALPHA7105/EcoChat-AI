// Initialize marked with options for syntax highlighting
marked.setOptions({
  highlight: function(code, language) {
      return hljs.highlightAuto(code).value;
  },
  breaks: true,
  gfm: true
});

// Dark/Light Theme Toggle
document.querySelector('.theme-toggle').addEventListener('click', () => {
  document.body.classList.toggle('dark-theme');
  const icon = document.querySelector('.theme-toggle i');
  if (document.body.classList.contains('dark-theme')) {
      icon.classList.remove('fa-moon');
      icon.classList.add('fa-sun');
  } else {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-moon');
  }
});

// Chat functionality
document.getElementById('send-btn').addEventListener('click', () => {
  const userInput = document.getElementById('user-input').value.trim();
  if (userInput) {
      appendMessage('user', userInput);
      fetchBotResponse(userInput);
      document.getElementById('user-input').value = '';
  }
});

document.getElementById('user-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
      document.getElementById('send-btn').click();
  }
});

function appendMessage(sender, message, isMarkdown = true) {
  const chatBox = document.getElementById('chat-box');
  const messageElement = document.createElement('div');
  messageElement.className = `chat-message ${sender}-message`;
  
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  
  const icon = document.createElement('i');
  icon.className = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
  avatar.appendChild(icon);
  
  const content = document.createElement('div');
  content.className = 'message-content';
  
  // Process markdown for bot messages if enabled
  if (sender === 'bot' && isMarkdown) {
      content.innerHTML = marked.parse(message);
  } else {
      // Escape HTML for user messages to prevent XSS
      const p = document.createElement('p');
      p.textContent = message;
      content.appendChild(p);
  }
  
  messageElement.appendChild(avatar);
  messageElement.appendChild(content);
  
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight;
  
  // Apply syntax highlighting to code blocks
  if (sender === 'bot' && isMarkdown) {
      document.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightElement(block);
      });
  }
}

async function fetchBotResponse(userInput) {
  // Show typing indicator
  const typingMessageId = showTypingIndicator();
  
  try {
      const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyCvv3NHzv-AiUn0VVdrjtt8Jkijvzvxb5k', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              contents: [{ 
                  parts: [{ 
                      text: userInput + "\n\nPlease format your response using markdown when appropriate." 
                  }] 
              }],
          }),
      });
      
      const data = await response.json();
      
      // Remove typing indicator
      removeTypingIndicator(typingMessageId);
      
      // Process Gemini API response
      if (data.candidates && data.candidates[0] && data.candidates[0].content) {
          const botResponse = data.candidates[0].content.parts[0].text;
          appendMessage('bot', botResponse, true);
      } else {
          appendMessage('bot', 'Sorry, received an empty or invalid response.', false);
      }
  } catch (error) {
      // Remove typing indicator and show error
      removeTypingIndicator(typingMessageId);
      appendMessage('bot', 'Sorry, something went wrong. Please try again.', false);
      console.error('Error:', error);
  }
}

// Typing indicator functions
function showTypingIndicator() {
  const chatBox = document.getElementById('chat-box');
  const typingElement = document.createElement('div');
  typingElement.className = 'chat-message bot-message typing-indicator';
  typingElement.id = 'typing-' + Date.now(); // unique ID
  
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  
  const icon = document.createElement('i');
  icon.className = 'fas fa-robot';
  avatar.appendChild(icon);
  
  const content = document.createElement('div');
  content.className = 'message-content';
  content.innerHTML = '<p>...</p>';
  
  typingElement.appendChild(avatar);
  typingElement.appendChild(content);
  
  chatBox.appendChild(typingElement);
  chatBox.scrollTop = chatBox.scrollHeight;
  
  return typingElement.id;
}

function removeTypingIndicator(id) {
  const element = document.getElementById(id);
  if (element) {
      element.remove();
  }
}

// Add a welcome message when the page loads with some examples of markdown
window.addEventListener('DOMContentLoaded', () => {
  const welcomeMessage = `# Welcome to SpaceGPT! 

I can help answer your questions about space and technology. Here are some examples of what you can ask me:

* Tell me about black holes
* What is the James Webb Space Telescope?
* How do rockets work?
* Explain quantum computing

I support **markdown** formatting, including:
- *Italic text*
- **Bold text**
- \`code snippets\`
- And even code blocks:

\`\`\`python
def hello_space():
  print("Hello, universe!")
\`\`\`

What would you like to know today?`;

  // Remove the default message and add our welcome message
  const defaultMessage = document.querySelector('.bot-message');
  if (defaultMessage) {
      defaultMessage.remove();
  }
  
  appendMessage('bot', welcomeMessage, true);
});
