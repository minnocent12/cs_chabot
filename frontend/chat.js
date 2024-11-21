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

function showBlueTyingIndicator() {
    // Create the blue tying indicator element
    const chatBody = document.querySelector('.chat-body');
    const indicator = document.createElement('div');
    indicator.id = 'blue-tying-indicator';
    indicator.innerHTML = '<p>Blue is tying...</p>';  // Text for the indicator

    // Add a class to style the indicator
    indicator.classList.add('blue-tying-indicator');
    chatBody.appendChild(indicator);
    chatBody.scrollTop = chatBody.scrollHeight; // Scroll to bottom
}

function hideBlueTyingIndicator() {
    const indicator = document.getElementById('blue-tying-indicator');
    if (indicator) {
        indicator.remove();  // Remove the "Blue tying..." indicator
    }
}

function sendMessage() {
    const userInputElement = document.getElementById('user-input');
    const userInput = userInputElement.value;

    if (!userInput.trim()) return;

    addMessage(userInput, 'user');  // Display the user's message

    // Reset the textarea value and height
    userInputElement.value = '';
    userInputElement.style.height = 'auto'; // Reset height to auto

    addMessage('...', 'bot-typing'); // Show typing indicator

    // Show the "Blue tying..." indicator
    showBlueTyingIndicator();

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
            hideBlueTyingIndicator();  // Hide the "Blue tying..." indicator after the response

            if (data.choose_keyword || (data.submenu_options && data.submenu_options.length > 0)) {
                const responseContent = data.choose_keyword
                    ? data.choose_keyword.map(keyword => 
                        `<button class="submenu-button" onclick="selectKeyword('${keyword}')">${keyword}</button>`).join('')
                    : data.submenu_options.map(option => 
                        `<button class="submenu-button" onclick="selectSubmenuOption('${option}')">${option}</button>`).join('');
                
                addMessage(`<p>${data.response}</p><div>${responseContent}</div>`, 'bot');
            } else {
                // Straight response
                addMessage(data.response || "Sorry, I didn't understand that.", 'bot', userInput, true); // Add feedback
            }
            
        }, 1000); // Delay after bot typing indicator
    });
}




function addTypingMessage(message, sender) {
    const chatBody = document.querySelector('.chat-body');
    const messageElement = document.createElement('div');
    messageElement.classList.add(`${sender}-message`);

    const currentTime = getCurrentTime();

    if (sender === 'bot') {
        // Split message into words
        const words = message.split(' ');
        const totalTime = 100; // 1 seconds total typing time
        const timePerWord = totalTime / words.length; // Calculate time per word

        // Initialize empty message content
        messageElement.innerHTML = `
            <img src="/assets/chatbot_logo.png" alt="Bot Icon">
            <div class="message-content">
                <p></p>
                <span class="timestamp">${currentTime}</span>
            </div>
        `;
        
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;

        const messageContent = messageElement.querySelector('.message-content p');

        // Display words one by one with a fast typing effect
        words.forEach((word, index) => {
            setTimeout(() => {
                messageContent.innerHTML += `${word} `;
                chatBody.scrollTop = chatBody.scrollHeight; // Scroll to show new content
            }, index * timePerWord);
        });
    }
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
            addMessage(data.response || "Sorry, I didn't understand that.", 'bot', null, false);
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
            addMessage("Sorry, I couldn't get a response for that option.", 'bot', null,false); // Handle undefined
        }
    });
}



function addFeedbackIcons(userMessage, botMessage) {
    const chatBody = document.querySelector('.chat-body');
    const feedbackContainer = document.createElement('div');
    let feedbackSubmitted = false;  // Flag to prevent multiple submissions

    feedbackContainer.classList.add('feedback-container');
    feedbackContainer.style.display = 'flex';
    feedbackContainer.style.alignItems = 'center';
    feedbackContainer.style.position = 'absolute';
    feedbackContainer.style.right = '10px'; // Align thumbs on the right side of the message

    // Create the "Was this helpful?" text with blue color
    const helpfulText = document.createElement('span');
    helpfulText.textContent = 'Was this helpful? ';
    helpfulText.style.marginRight = '10px'; // Add spacing between text and icons
    helpfulText.style.color = 'blue'; // Make the text blue

    // Thumbs up and down as Font Awesome icons with colors
    const thumbUp = document.createElement('span');
    thumbUp.innerHTML = '<i class="fas fa-thumbs-up" style="color: green;"></i>';
    thumbUp.classList.add('thumb-icon');
    thumbUp.style.cursor = 'pointer';
    thumbUp.onclick = () => submitFeedback('up', userMessage, botMessage, feedbackContainer);

    const thumbDown = document.createElement('span');
    thumbDown.innerHTML = '<i class="fas fa-thumbs-down" style="color: red;"></i>';
    thumbDown.classList.add('thumb-icon');
    thumbDown.style.cursor = 'pointer';
    thumbDown.onclick = () => submitFeedback('down', userMessage, botMessage, feedbackContainer);

    feedbackContainer.appendChild(helpfulText);  // Add the helpful text before thumbs
    feedbackContainer.appendChild(thumbUp);
    feedbackContainer.appendChild(thumbDown);

    // Append thumbs to the last bot message container
    const lastBotMessage = chatBody.querySelector('.bot-message:last-child .message-content');
    if (lastBotMessage) lastBotMessage.appendChild(feedbackContainer);

    // Set a timer to automatically remove feedback icons if the user continues chatting
    const feedbackTimeout = setTimeout(() => {
        if (feedbackContainer && !feedbackSubmitted) feedbackContainer.remove();
    }, 100000); // Disappear after 10 seconds if not clicked

    // Remove feedback icons on new message send
    document.getElementById('user-input').addEventListener('input', () => {
        if (feedbackContainer && !feedbackSubmitted) {
            feedbackContainer.remove();
            clearTimeout(feedbackTimeout); // Clear timeout to avoid errors
        }
    });

    // Function to submit feedback and ensure it's sent to the server
    function submitFeedback(feedback, userMessage, botMessage, feedbackContainer) {
        if (feedbackSubmitted) return;  // Prevent multiple submissions
        feedbackSubmitted = true;       // Set flag to true to prevent further clicks
    
        fetch('/store_feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_message: userMessage, bot_message: botMessage, feedback: feedback })
        })
        .then(response => {
            if (response.ok) {
                if (feedback === 'up') {
                    // Replace the feedback container content with "Thank you" message
                    feedbackContainer.innerHTML = ''; // Clear existing content
                    const thankYouMessage = document.createElement('span');
                    thankYouMessage.textContent = "Thank you for your feedback!";
                    thankYouMessage.style.color = 'blue'; // Add color for visibility
                    thankYouMessage.style.fontWeight = 'bold'; // Optional styling
                    feedbackContainer.appendChild(thankYouMessage);
    
                    // Remove the "Thank you" message (and container) after 5 seconds
                    setTimeout(() => {
                        feedbackContainer.remove();
                    }, 5000);
                } else if (feedback === 'down') {
                    // Remove feedback container immediately
                    feedbackContainer.remove();
    
                    // Fetch and display similar questions
                    fetch('/get_similar_questions', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    })
                    .then(response => response.json())
                    .then(similarQuestions => {
                        if (similarQuestions && similarQuestions.length > 0) {
                            const chatBody = document.querySelector('.chat-body');
    
                            // Create the list of similar questions with clickable buttons
                            const messageElement = document.createElement('div');
                            messageElement.classList.add('bot-message');
    
                            const similarQuestionsList = similarQuestions.map(q => 
                                `<button class="submenu-button" onclick="selectSimilarQuestion('${q}')">${q}</button>`
                            ).join('');
                            messageElement.innerHTML = `
                                <img src="/assets/chatbot_logo.png" alt="Bot Icon">
                                <div class="message-content">
                                    <p>Here are some questions related to what you asked above:</p>
                                    <div>${similarQuestionsList}</div>
                                </div>
                            `;
    
                            chatBody.appendChild(messageElement);
                            chatBody.scrollTop = chatBody.scrollHeight;
                        } else {
                            // Handle case where there are no similar questions
                            addMessage("Sorry, I do not have more information on that topic.", 'bot');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching similar questions:', error);
                    });
                }
            } else {
                console.error('Feedback submission failed with status:', response.status);
            }
        })
        .catch(error => console.error('Error submitting feedback:', error));
    }
}


// This function will be called when a similar question is clicked
function selectSimilarQuestion(question) {
    addMessage(question, 'user'); // Display the selected similar question
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: question }) // Send the selected question as a message
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






function addMessage(message, sender, userMessage, addFeedback = false) {
    const chatBody = document.querySelector('.chat-body');
    const messageElement = document.createElement('div');
    messageElement.classList.add(`${sender}-message`);

    const currentTime = getCurrentTime();

    function linkify(text) {
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        const emailPattern = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/g;
        return text
            .replace(urlPattern, '<a href="$1" target="_blank">$1</a>')
            .replace(emailPattern, '<a href="mailto:$1" target="_blank">$1</a>');
    }

    if (sender === 'bot') {
        messageElement.innerHTML = `
            <img src="/assets/chatbot_logo.png" alt="Bot Icon">
            <div class="message-content">
                <p>${linkify(message)}</p>
                <span class="timestamp">${currentTime}</span>
            </div>
        `;
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;

        if (addFeedback) {
            addFeedbackIcons(userMessage, message); // Call feedback function only if true
        }
    } else if (sender === 'user') {
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
                <span class="timestamp">${currentTime}</span>
            </div>
        `;
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
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
            const submenuHtml = data.submenu_options.map(option => 
                `<button class="submenu-button" onclick="selectSubmenuOption('${option}')">${option}</button>`
            ).join('');
            addMessage(`<p>${data.response}</p><div>${submenuHtml}</div>`, 'bot', null, false);
        } else {
            addMessage(data.response || "Sorry, I didn't understand that.", 'bot', null, true);
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


document.getElementById('user-input').addEventListener('input', function () {
    this.style.height = 'auto'; // Reset height
    this.style.height = this.scrollHeight + 'px'; // Set height to scroll height
});

