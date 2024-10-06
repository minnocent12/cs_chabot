function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12; // Convert to 12-hour format
    hours = hours ? hours : 12; // If hour is 0, make it 12
    const formattedTime = `${hours}:${minutes} ${ampm}`;

    return formattedTime;
}

function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    const chatIconImg = document.getElementById('chat-icon-img');

    if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
        chatWindow.style.display = 'flex'; // Show the chat window
        chatIconImg.src = '/assets/drop.png'; // Change to dropdown icon
    } else {
        chatWindow.style.display = 'none'; // Hide the chat window
        chatIconImg.src = '/assets/chat.png'; // Change back to chat icon
    }
}

function closeChat() {
    const chatWindow = document.getElementById('chat-window');
    const chatIconImg = document.getElementById('chat-icon-img');

    // Hide the chat window
    chatWindow.style.display = 'none'; 
    // Change the icon back to chat icon
    chatIconImg.src = '/assets/chat.png'; 
    
    // Clear the chat body (reset the conversation)
    const chatBody = document.querySelector('.chat-body');
    chatBody.innerHTML = '';

    // Clear the user input field
    document.getElementById('user-input').value = '';
}

function minimizeChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.style.display = 'none'; // Hide the chat window
    const chatIconImg = document.getElementById('chat-icon-img');
    chatIconImg.src = '/assets/chat.png'; // Change back to chat icon
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    addMessage(userInput, 'user');
    document.getElementById('user-input').value = '';

    addMessage('...', 'bot-typing');

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            removeTypingIndicator();

            if (data.choose_keyword) {
                // Combine the message with keyword options
                const keywordButtons = data.choose_keyword.map(keyword => 
                    `<button class="submenu-button" onclick="selectKeyword('${keyword}')">${keyword}</button>`
                ).join('');
                const messageWithKeywords = `<p>${data.response}</p><div>${keywordButtons}</div>`;
                addMessage(messageWithKeywords, 'bot');
            } else if (data.submenu_options && data.submenu_options.length > 0) {
                // Create submenu buttons
                const submenuButtons = data.submenu_options.map(option => 
                    `<button class="submenu-button" onclick="selectSubmenuOption('${option}')">${option}</button>`
                ).join('');

                // Combine the response message with submenu options into a single message
                const messageWithSubmenu = `<p>${data.response}</p><div>${submenuButtons}</div>`;
                addMessage(messageWithSubmenu, 'bot');
            } else {
                // Show the bot's response if there are no submenu options
                addMessage(data.response || "Sorry, I didn't understand that.", 'bot');
            }
        }, 2000);
    });
}


function selectKeyword(keyword) {
    addMessage(keyword, 'user');
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: keyword })
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator(); // Ensure typing indicator is removed
        
        // If the response has submenu options, display them
        if (data.submenu_options && data.submenu_options.length > 0) {
            const submenuHtml = data.submenu_options.map(option => 
                `<button class="submenu-button" onclick="selectSubmenuOption('${option}')">${option}</button>`
            ).join('');
            addMessage(`<div>${submenuHtml}</div>`, 'bot');
        } else {
            addMessage(data.response || "Sorry, I didn't understand that.", 'bot');
        }
    });
}



    

function selectSubmenuOption(option) {
    addMessage(option, 'user'); // Display the selected submenu option
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: option }) // Send the submenu option as a message
    })
    .then(response => response.json())
    .then(data => {
        // Check if the response has submenu_response
        if (data.submenu_response) {
            addMessage(data.submenu_response, 'bot'); // Display the response for the submenu option
        } else {
            addMessage("Sorry, I couldn't get a response for that option.", 'bot'); // Handle undefined
        }
    });
}




function addMessage(message, sender) {
    const chatBody = document.querySelector('.chat-body');
    const messageElement = document.createElement('div');
    messageElement.classList.add(`${sender}-message`);

    const currentTime = getCurrentTime();

    if (sender === 'bot') {
        messageElement.innerHTML = `
            <img src="/assets/chatbot_logo.png" alt="Bot Icon">
            <div class="message-content">
                <p>${message}</p>
                <span class="timestamp">${currentTime}</span>
            </div>
        `;
    } else if (sender === 'bot-typing') {
        messageElement.innerHTML = `
            <div class="message-content">
                <p class="typing-indicator">Blue is typing</p>
            </div>
        `;
        messageElement.id = 'typing-indicator';
    } else {
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
                <span class="timestamp">${currentTime}</span>
            </div>
        `;
    }

    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove(); // Remove the typing indicator once the bot responds
    }
}


function askPredefinedQuestion(question) {
    addMessage(question, 'user'); // Display user's predefined question as their input
    
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: question }) // Send the question to the backend
    })
    .then(response => response.json())
    .then(data => {
        if (data.submenu_options && data.submenu_options.length > 0) {
            // If there are submenu options, display them as buttons
            const submenuHtml = data.submenu_options.map(option => 
                `<button class="submenu-button" onclick="selectSubmenuOption('${option}')">${option}</button>`
            ).join('');

            // Combine the response message with submenu options into a single message
            const messageWithSubmenu = `<p>${data.response}</p><div>${submenuHtml}</div>`;

            addMessage(messageWithSubmenu, 'bot');
        } else {
            // If no submenu options, display the bot's response
            addMessage(data.response || "Sorry, I didn't understand that.", 'bot');
        }
        
        closeDialog(); // Close the dialog after selecting a predefined question
    })
    .catch(error => {
        console.error('Error:', error); // Handle any potential errors
        addMessage("Oops, something went wrong. Please try again.", 'bot');
    });
}


function showDialog() {
    const dialog = document.getElementById('predefined-dialog');
    dialog.style.display = 'flex'; // Show the dialog
}

function closeDialog() {
    const dialog = document.getElementById('predefined-dialog');
    dialog.style.display = 'none'; // Hide the dialog
}

// Make sure the predefined-questions-btn button exists
const predefinedQuestionsBtn = document.getElementById('predefined-questions-btn');
if (predefinedQuestionsBtn) {
    predefinedQuestionsBtn.addEventListener('click', showDialog); // Trigger showDialog when needed
}

// Adding event listener for the "Enter" key
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage(); // Trigger send message on Enter key press
    }
});

document.addEventListener('DOMContentLoaded', () => {
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slideshow img');
    
    function showSlides() {
        slides.forEach((slide, index) => {
            slide.style.opacity = index === slideIndex ? '1' : '0';
        });
        slideIndex = (slideIndex + 1) % slides.length;
        setTimeout(showSlides, 5000); // Change slide every 5 seconds
    }

    showSlides(); // Start the slideshow
});

