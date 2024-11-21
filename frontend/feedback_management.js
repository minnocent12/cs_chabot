document.addEventListener('DOMContentLoaded', () => {
    loadFeedback();

    // Load feedback from the server
    function loadFeedback() {
        fetch('/feedback')
            .then(response => response.json())
            .then(data => populateFeedbackTable(data))
            .catch(error => console.error('Error loading feedback:', error));
    }

    // Populate the feedback table with data
    function populateFeedbackTable(feedbackList) {
        const tbody = document.querySelector('#feedback-table tbody');
        tbody.innerHTML = ''; // Clear existing rows

        if (feedbackList.length === 0) {
            // If no feedback is found, display a message
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="4" style="text-align: center;">No feedback found.</td>';
            tbody.appendChild(row);
            return;
        }

        feedbackList.forEach(feedback => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${feedback.user_message}</td>
                <td>${feedback.bot_response}</td>
                <td>${feedback.feedback}</td>
                <td class="actions">
                    <button onclick="deleteFeedback(${feedback.id})"><i class="fas fa-trash-alt"></i> Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // Store the ID of the feedback to delete
    let feedbackToDelete = null;

    // Open the dialog for confirmation
    window.deleteFeedback = function(id) {
        feedbackToDelete = id; // Store the ID to be deleted
        openDialog(); // Open the confirmation dialog
    };

    // Open the dialog
    function openDialog() {
        document.getElementById('confirmation-dialog').style.display = 'block';
    }

    // Close the dialog
    window.closeDialog = function() {
        document.getElementById('confirmation-dialog').style.display = 'none';
    };

    // Confirm deletion
    document.getElementById('confirm-delete').addEventListener('click', function() {
        if (feedbackToDelete !== null) {
            fetch(`/feedback/delete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: feedbackToDelete })
            })
            .then(response => {
                if (response.ok) {
                    loadFeedback(); // Reload feedback after deletion
                } else {
                    console.error('Error deleting feedback:', response);
                }
            })
            .catch(error => console.error('Error deleting feedback:', error))
            .finally(() => {
                closeDialog(); // Close the dialog regardless of the outcome
                feedbackToDelete = null; // Reset the ID
            });
        }
    });
});
