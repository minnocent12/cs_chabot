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
    tableBody.innerHTML = '';  // This will clear only the table content
}

function addIntent() {
    const form = document.getElementById('addIntentForm');
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
    }).then(response => response.json())
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
    const formData = new FormData(form);
    fetch('/intents/update', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('updateId'),
            intent_name: formData.get('updateIntentName'),
            has_submenu: formData.get('updateHasSubmenu') === 'true'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Intent updated successfully!', true);
              fetchIntents();
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
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Response added successfully!', true);
              fetchResponses();
          } else {
              showDialog('Error adding response.', false);
          }
      });
}

function updateResponse() {
    const form = document.getElementById('updateResponseForm');
    const formData = new FormData(form);
    fetch('/responses/update', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('updateResponseId'),
            response: formData.get('updateResponseText')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Response updated successfully!', true);
              fetchResponses();
          } else {
              showDialog('Error updating response.', false);
          }
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
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Keyword added successfully!', true);
              fetchKeywords();
          } else {
              showDialog('Error adding keyword.', false);
          }
      });
}

function updateKeyword() {
    const form = document.getElementById('updateKeywordForm');
    const formData = new FormData(form);
    fetch('/keywords/update', {
        method: 'POST',
        body: JSON.stringify({
            id: formData.get('updateKeywordId'),
            keyword: formData.get('updateKeywordText')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Keyword updated successfully!', true);
              fetchKeywords();
          } else {
              showDialog('Error updating keyword.', false);
          }
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
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Submenu response added successfully!', true);
              fetchSubmenuResponses();
          } else {
              showDialog('Error adding submenu response.', false);
          }
      });
}

function updateSubmenuResponse() {
    const form = document.getElementById('updateSubmenuResponseForm');
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
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              showDialog('Submenu response updated successfully!', true);
              fetchSubmenuResponses();
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
