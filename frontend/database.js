// Utility function to show a professional dialog box
function showDialog(message, onClose) {
    const dialog = document.createElement('div');
    dialog.classList.add('dialog');
    dialog.innerHTML = `
        <div class="dialog-content">
            <p>${message}</p>
            <button onclick="closeDialog(${onClose ? 'true' : 'false'})">OK</button>
        </div>
    `;
    document.body.appendChild(dialog);
}


function closeDialog(resetForm) {
    const dialog = document.querySelector('.dialog');
    if (dialog) {
        document.body.removeChild(dialog);
    }
    if (resetForm) {
        resetAllForms();
    }
}

// Utility function to reset all forms
function resetAllForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => form.reset());
}


// Intents Functions

let isSearchResultDisplayed = false;

function fetchIntents() {
    fetch('/intents')
        .then(response => response.json())
        .then(data => {
            if (isSearchResultDisplayed) {
                return;  // If search results are displayed, don't load regular results.
            }
            displayIntents(data);
        });
}

function handleSearch(event) {
    if (event.key === 'Enter') {
        searchIntents();
    }
}

function searchIntents() {
    const searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();

    fetch('/intents')
        .then(response => response.json())
        .then(data => {
            let filteredData;
            if (!isNaN(searchQuery) && searchQuery !== '') {
                // If the search query is a number, compare IDs exactly
                const searchID = parseInt(searchQuery);
                filteredData = data.filter(intent => intent.id === searchID);
            } else {
                // If the search query is not a number, filter by intent name
                filteredData = data.filter(intent => 
                    intent.intent_name.toLowerCase().includes(searchQuery)
                );
            }
            displayIntents(filteredData);
            isSearchResultDisplayed = true;  // Indicate search results are shown.
        });
}


function displayIntents(data) {
    const tableBody = document.querySelector('#intentsTable tbody');
    tableBody.innerHTML = '';  // Clear any existing content
    data.forEach(intent => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${intent.id}</td>
            <td>${intent.intent_name}</td>
            <td>${intent.has_submenu}</td>
            <td>
                <button onclick="populateUpdateIntentForm(${intent.id}, '${intent.intent_name}', ${intent.has_submenu})">Edit</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


function fetchIntents() {
    fetch('/intents')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#intentsTable tbody');
            tableBody.innerHTML = '';  // Clear any existing content
            data.forEach(intent => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${intent.id}</td>
                    <td>${intent.intent_name}</td>
                    <td>${intent.has_submenu}</td>
                    <td>
                        <button onclick="populateUpdateIntentForm(${intent.id}, '${intent.intent_name}', ${intent.has_submenu})">Edit</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function unloadIntents() {
    const tableBody = document.querySelector('#intentsTable tbody');
    tableBody.innerHTML = '';  // This will clear the table content
    isSearchResultDisplayed = false;  // Reset search display flag
}

function addIntent() {
    const form = document.getElementById('addIntentForm');
    const intentName = form.intentName.value.trim();
    const hasSubmenu = form.hasSubmenu.value;

    // Check if all required fields are filled
    if (!intentName || !hasSubmenu) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    const formData = new FormData(form);

    fetch('/intents/add', {
        method: 'POST',
        body: JSON.stringify({
            intent_name: formData.get('intentName'),
            has_submenu: formData.get('hasSubmenu') === 'true'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Intent added successfully!', true);
            fetchIntents();
        } else {
            showDialog('Error adding intent.', false);
        }
    });
}




function updateIntent() {
    const form = document.getElementById('updateIntentForm');
    const updateId = form.updateId.value.trim();
    const updateIntentName = form.updateIntentName.value.trim();
    const updateHasSubmenu = form.updateHasSubmenu.value.trim();

    // Check if all required fields are filled
    if (!updateId || !updateIntentName || !updateHasSubmenu) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    fetch('/intents/update', {
        method: 'POST',
        body: JSON.stringify({
            id: updateId,
            intent_name: updateIntentName,
            has_submenu: updateHasSubmenu === 'true'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Intent updated successfully!', true);
            fetchIntents(); // Refresh the intents
        } else {
            showDialog('Error updating intent.', false);
        }
    });
}



function deleteIntent() {
    const form = document.getElementById('deleteIntentForm');
    const formData = new FormData(form);
    fetch('/intents/delete', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('deleteId')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Intent deleted successfully!', true);
              fetchIntents();
          } else {
              showDialog('Error deleting intent.', false);
          }
      });
}

function populateUpdateIntentForm(id, name, hasSubmenu) {
    document.getElementById('updateId').value = id;
    document.getElementById('updateIntentName').value = name;
    document.getElementById('updateHasSubmenu').value = hasSubmenu ? 'true' : 'false';
}






// Responses Functions


function handleResponseSearch(event) {
    if (event.key === 'Enter') {
        searchResponses();
    }
}

function searchResponses() {
    const searchQuery = document.getElementById('searchResponseInput').value.trim().toLowerCase();

    fetch('/responses')
        .then(response => response.json())
        .then(data => {
            let filteredData;
            if (!isNaN(searchQuery) && searchQuery !== '') {
                // If the search query is a number, filter by exact intent_id
                const searchIntentID = parseInt(searchQuery);
                filteredData = data.filter(response => response.intent_id === searchIntentID);
            } else {
                // If the search query is not a number, filter by response text
                filteredData = data.filter(response => 
                    response.response.toLowerCase().includes(searchQuery)
                );
            }
            displayResponses(filteredData); // Display filtered results
        });
}

function displayResponses(data) {
    const tableBody = document.querySelector('#responsesTable tbody');
    tableBody.innerHTML = '';  // Clear existing content
    data.forEach(response => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${response.id}</td>
            <td>${response.intent_id}</td>
            <td>${response.response}</td>
            <td>
                <button onclick="populateUpdateResponseForm(${response.id}, ${response.intent_id}, '${response.response}')">Edit</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


function fetchResponses() {
    fetch('/responses')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#responsesTable tbody');
            tableBody.innerHTML = '';  // Clear any existing content
            data.forEach(response => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${response.id}</td>
                    <td>${response.intent_id}</td>
                    <td>${response.response}</td>
                    <td>
                        <button onclick="populateUpdateResponseForm(${response.id}, ${response.intent_id}, '${response.response}')">Edit</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function unloadResponses() {
    const tableBody = document.querySelector('#responsesTable tbody');
    tableBody.innerHTML = '';  // This will clear only the table content
}



function addResponse() {
    const form = document.getElementById('addResponseForm');
    const responseIntentId = form.responseIntentId.value.trim();
    const responseText = form.responseText.value.trim();

    // Check if all required fields are filled
    if (!responseIntentId || !responseText) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    const formData = new FormData(form);

    fetch('/responses/add', {
        method: 'POST',
        body: JSON.stringify({
            intent_id: formData.get('responseIntentId'),
            response: formData.get('responseText')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Response added successfully!', true);
            fetchResponses(); // Refresh the list of responses
        } else {
            showDialog('Error adding response.', false);
        }
    });
}


function updateResponse() {
    const form = document.getElementById('updateResponseForm');
    const updateResponseId = form.updateResponseId.value.trim();
    const updateResponseText = form.updateResponseText.value.trim();

    // Validate form inputs
    if (!updateResponseId || !updateResponseText) {
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission if validation fails
    }

    fetch('/responses/update', {
        method: 'POST',
        body: JSON.stringify({
            id: updateResponseId,
            response: updateResponseText // Only send response text
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Response updated successfully!', true);  // Use a dialog box instead of alert
            fetchResponses();  // Reload the responses to reflect the changes
        } else {
            showDialog('Error updating response.', false);
        }
    })
    .catch(error => {
        showDialog('An unexpected error occurred.', false);
        console.error('Error during response update:', error);
    });
}



function deleteResponse() {
    const form = document.getElementById('deleteResponseForm');
    const formData = new FormData(form);
    fetch('/responses/delete', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('deleteResponseId')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Response deleted successfully!', true);
              fetchResponses();
          } else {
              showDialog('Error deleting response.', false);
          }
      });
}

function populateUpdateResponseForm(id, intentId, response) {
    document.getElementById('updateResponseId').value = id;
    document.getElementById('updateResponseText').value = response;
}




// Keywords Functions

function handleKeywordSearch(event) {
    if (event.key === 'Enter') {
        searchKeywords();
    }
}

function searchKeywords() {
    const searchQuery = document.getElementById('searchKeywordInput').value.trim().toLowerCase();

    fetch('/keywords')
        .then(response => response.json())
        .then(data => {
            let filteredData;
            if (!isNaN(searchQuery) && searchQuery !== '') {
                // If search query is a number, filter by exact intent_id
                const searchIntentID = parseInt(searchQuery);
                filteredData = data.filter(keyword => keyword.intent_id === searchIntentID);
            } else {
                // If the search query is not a number, filter by keyword text
                filteredData = data.filter(keyword =>
                    keyword.keyword.toLowerCase().includes(searchQuery)
                );
            }
            displayKeywords(filteredData); // Display filtered results
        });
}

function displayKeywords(data) {
    const tableBody = document.querySelector('#keywordsTable tbody');
    tableBody.innerHTML = '';  // Clear existing content
    data.forEach(keyword => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${keyword.id}</td>
            <td>${keyword.intent_id}</td>
            <td>${keyword.keyword}</td>
            <td>
                <button onclick="populateUpdateKeywordForm(${keyword.id}, ${keyword.intent_id}, '${keyword.keyword}')">Edit</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function fetchKeywords() {
    fetch('/keywords')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#keywordsTable tbody');
            tableBody.innerHTML = '';  // Clear any existing content
            data.forEach(keyword => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${keyword.id}</td>
                    <td>${keyword.intent_id}</td>
                    <td>${keyword.keyword}</td>
                    <td>
                        <button onclick="populateUpdateKeywordForm(${keyword.id}, ${keyword.intent_id}, '${keyword.keyword}')">Edit</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function unloadKeywords() {
    const tableBody = document.querySelector('#keywordsTable tbody');
    tableBody.innerHTML = '';  // This will clear only the table content
}


function addKeyword() {
    const form = document.getElementById('addKeywordForm');
    const keywordIntentId = form.keywordIntentId.value.trim();
    const keywordText = form.keywordText.value.trim();

    // Check if all required fields are filled
    if (!keywordIntentId || !keywordText) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    const formData = new FormData(form);

    fetch('/keywords/add', {
        method: 'POST',
        body: JSON.stringify({
            intent_id: formData.get('keywordIntentId'),
            keyword: formData.get('keywordText')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Keyword added successfully!', true);
            fetchKeywords(); // Refresh the list of keywords
        } else {
            showDialog('Error adding keyword.', false);
        }
    });
}


function updateKeyword() {
    const form = document.getElementById('updateKeywordForm');
    const updateKeywordId = form.updateKeywordId.value.trim();
    const updateKeywordText = form.updateKeywordText.value.trim();

    // Validate form inputs
    if (!updateKeywordId || !updateKeywordText) {
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission if validation fails
    }

    fetch('/keywords/update', {
        method: 'POST',
        body: JSON.stringify({
            id: updateKeywordId,
            keyword: updateKeywordText
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Keyword updated successfully!', true); // Use a dialog box instead of alert
            fetchKeywords(); // Reload the keywords to reflect the changes
        } else {
            showDialog('Error updating keyword.', false);
        }
    })
    .catch(error => {
        showDialog('An unexpected error occurred.', false);
        console.error('Error during keyword update:', error);
    });
}


function deleteKeyword() {
    const form = document.getElementById('deleteKeywordForm');
    const formData = new FormData(form);
    fetch('/keywords/delete', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('deleteKeywordId')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Keyword deleted successfully!', true);
              fetchKeywords();
          } else {
              showDialog('Error deleting keyword.', false);
          }
      });
}

function populateUpdateKeywordForm(id, intentId, keyword) {
    document.getElementById('updateKeywordId').value = id;
    document.getElementById('updateKeywordText').value = keyword;
}




// Submenu Responses Functions


function handleSubmenuSearch(event) {
    if (event.key === 'Enter') {
        searchSubmenuResponses();
    }
}

function searchSubmenuResponses() {
    const searchQuery = document.getElementById('searchSubmenuInput').value.trim().toLowerCase();

    fetch('/submenu_responses')
        .then(response => response.json())
        .then(data => {
            let filteredData;
            if (!isNaN(searchQuery) && searchQuery !== '') {
                // If search query is a number, filter by exact intent_id
                const searchIntentID = parseInt(searchQuery);
                filteredData = data.filter(response => response.intent_id === searchIntentID);
            } else {
                // If the search query is not a number, filter by submenu_option or submenu_response text
                filteredData = data.filter(response =>
                    response.submenu_option.toLowerCase().includes(searchQuery) ||
                    response.submenu_response.toLowerCase().includes(searchQuery)
                );
            }
            displaySubmenuResponses(filteredData); // Display filtered results
        });
}

function displaySubmenuResponses(data) {
    const tableBody = document.querySelector('#submenuResponsesTable tbody');
    tableBody.innerHTML = '';  // Clear any existing content
    data.forEach(response => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${response.id}</td>
            <td>${response.intent_id}</td>
            <td>${response.submenu_option}</td>
            <td>${response.submenu_response}</td>
            <td>
                <button onclick="populateUpdateSubmenuResponseForm(${response.id}, ${response.intent_id}, '${response.submenu_option}', '${response.submenu_response}')">Edit</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


function fetchSubmenuResponses() {
    fetch('/submenu_responses')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#submenuResponsesTable tbody');
            tableBody.innerHTML = '';  // Clear any existing content
            data.forEach(response => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${response.id}</td>
                    <td>${response.intent_id}</td>
                    <td>${response.submenu_option}</td>
                    <td>${response.submenu_response}</td>
                    <td>
                        <button onclick="populateUpdateSubmenuResponseForm(${response.id}, ${response.intent_id}, '${response.submenu_option}', '${response.submenu_response}')">Edit</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function unloadSubmenuResponses() {
    const tableBody = document.querySelector('#submenuResponsesTable tbody');
    tableBody.innerHTML = '';  // This will clear only the table content
}

function addSubmenuResponse() {
    const form = document.getElementById('addSubmenuResponseForm');
    const submenuIntentId = form.submenuIntentId.value.trim();
    const submenuOption = form.submenuOption.value.trim();
    const submenuResponse = form.submenuResponse.value.trim();

    // Check if all required fields are filled
    if (!submenuIntentId || !submenuOption || !submenuResponse) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    const formData = new FormData(form);

    fetch('/submenu_responses/add', {
        method: 'POST',
        body: JSON.stringify({
            intent_id: formData.get('submenuIntentId'),
            submenu_option: formData.get('submenuOption'),
            submenu_response: formData.get('submenuResponse')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Submenu response added successfully!', true);
            fetchSubmenuResponses(); // Refresh the submenu responses
        } else {
            showDialog('Error adding submenu response.', false);
        }
    });
}


function updateSubmenuResponse() {
    const form = document.getElementById('updateSubmenuResponseForm');
    const submenuResponseId = form.updateSubmenuResponseId.value.trim();
    const submenuOption = form.updateSubmenuOption.value.trim();
    const submenuResponseText = form.updateSubmenuResponseText.value.trim();

    // Check if all required fields are filled
    if (!submenuResponseId || !submenuOption || !submenuResponseText) {
        // Show a dialog box if any required fields are empty
        showDialog('Please fill in all required fields', false);
        return; // Prevent form submission
    }

    const formData = new FormData(form);

    fetch('/submenu_responses/update', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('updateSubmenuResponseId'),
            submenu_option: formData.get('updateSubmenuOption'),
            submenu_response: formData.get('updateSubmenuResponseText')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDialog('Submenu response updated successfully!', true);
            fetchSubmenuResponses(); // Refresh the submenu responses
        } else {
            showDialog('Error updating submenu response.', false);
        }
    });
}


function deleteSubmenuResponse() {
    const form = document.getElementById('deleteSubmenuResponseForm');
    const formData = new FormData(form);
    fetch('/submenu_responses/delete', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('deleteSubmenuResponseId')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Submenu response deleted successfully!', true);
              fetchSubmenuResponses();
          } else {
              showDialog('Error deleting submenu response.', false);
          }
      });
}

function populateUpdateSubmenuResponseForm(id, intentId, option, response) {
    document.getElementById('updateSubmenuResponseId').value = id;
    document.getElementById('updateSubmenuOption').value = option;
    document.getElementById('updateSubmenuResponseText').value = response;
}
