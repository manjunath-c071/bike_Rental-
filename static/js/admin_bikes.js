// Admin Bike Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // CSRF token setup for AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Add bike modal
    const addBikeBtn = document.getElementById('add-bike-btn');
    const addBikeModal = $('#addBikeModal');

    if (addBikeBtn) {
        addBikeBtn.addEventListener('click', function() {
            addBikeModal.modal('show');
        });
    }

    // Handle add bike form submission
    const addBikeForm = document.getElementById('add-bike-form');
    if (addBikeForm) {
        addBikeForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch('{% url "admin_dashboard:bike_create" %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addBikeModal.modal('hide');
                    location.reload(); // Refresh to show new bike
                } else {
                    // Show errors
                    console.error('Error:', data.errors);
                    alert('Error adding bike: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding bike');
            });
        });
    }

    // Inline editing functionality
    let editingRow = null;

    // Make cells editable on double-click
    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('dblclick', function() {
            if (editingRow) return; // Only one edit at a time

            const bikeId = this.dataset.bikeId;
            const field = this.dataset.field;
            const currentValue = this.textContent.trim();

            editingRow = this.closest('tr');

            // Create input field
            const input = document.createElement('input');
            input.type = this.dataset.inputType || 'text';
            input.className = 'form-control form-control-sm';
            input.value = currentValue;

            // Handle special cases
            if (field === 'bike_type') {
                const select = document.createElement('select');
                select.className = 'form-control form-control-sm';
                select.innerHTML = `
                    <option value="MTB" ${currentValue === 'Mountain Bike' ? 'selected' : ''}>Mountain Bike</option>
                    <option value="Road" ${currentValue === 'Road Bike' ? 'selected' : ''}>Road Bike</option>
                    <option value="Hybrid" ${currentValue === 'Hybrid Bike' ? 'selected' : ''}>Hybrid Bike</option>
                    <option value="Cruiser" ${currentValue === 'Cruiser Bike' ? 'selected' : ''}>Cruiser Bike</option>
                    <option value="BMX" ${currentValue === 'BMX Bike' ? 'selected' : ''}>BMX Bike</option>
                    <option value="Electric" ${currentValue === 'Electric Bike' ? 'selected' : ''}>Electric Bike</option>
                `;
                this.innerHTML = '';
                this.appendChild(select);
                select.focus();
            } else if (field === 'city') {
                const select = document.createElement('select');
                select.className = 'form-control form-control-sm';
                select.innerHTML = `
                    <option value="Delhi" ${currentValue === 'Delhi' ? 'selected' : ''}>Delhi</option>
                    <option value="Mumbai" ${currentValue === 'Mumbai' ? 'selected' : ''}>Mumbai</option>
                    <option value="Bangalore" ${currentValue === 'Bangalore' ? 'selected' : ''}>Bangalore</option>
                    <option value="Hyderabad" ${currentValue === 'Hyderabad' ? 'selected' : ''}>Hyderabad</option>
                    <option value="Chennai" ${currentValue === 'Chennai' ? 'selected' : ''}>Chennai</option>
                    <option value="Kolkata" ${currentValue === 'Kolkata' ? 'selected' : ''}>Kolkata</option>
                    <option value="Pune" ${currentValue === 'Pune' ? 'selected' : ''}>Pune</option>
                    <option value="Jaipur" ${currentValue === 'Jaipur' ? 'selected' : ''}>Jaipur</option>
                    <option value="Lucknow" ${currentValue === 'Lucknow' ? 'selected' : ''}>Lucknow</option>
                    <option value="Ahmedabad" ${currentValue === 'Ahmedabad' ? 'selected' : ''}>Ahmedabad</option>
                `;
                this.innerHTML = '';
                this.appendChild(select);
                select.focus();
            } else {
                this.innerHTML = '';
                this.appendChild(input);
                input.focus();
                input.select();
            }

            // Add save/cancel buttons
            const actionsCell = this.closest('tr').querySelector('.actions-cell');
            const originalActions = actionsCell.innerHTML;
            actionsCell.innerHTML = `
                <button class="btn btn-sm btn-success save-btn" data-bike-id="${bikeId}" data-field="${field}">
                    <i class="fas fa-check"></i>
                </button>
                <button class="btn btn-sm btn-secondary cancel-btn">
                    <i class="fas fa-times"></i>
                </button>
            `;

            // Handle save
            const saveBtn = actionsCell.querySelector('.save-btn');
            saveBtn.addEventListener('click', function() {
                const newValue = field === 'bike_type' || field === 'city' ?
                    this.closest('tr').querySelector(`[data-field="${field}"] select`).value :
                    input.value;

                updateBikeField(bikeId, field, newValue, this.closest('tr'), originalActions);
            });

            // Handle cancel
            const cancelBtn = actionsCell.querySelector('.cancel-btn');
            cancelBtn.addEventListener('click', function() {
                cancelEdit(this.closest('tr'), originalActions);
            });

            // Handle Enter key
            const element = field === 'bike_type' || field === 'city' ? select : input;
            element.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    saveBtn.click();
                } else if (e.key === 'Escape') {
                    cancelBtn.click();
                }
            });
        });
    });

    function updateBikeField(bikeId, field, value, row, originalActions) {
        fetch(`/dashboard/bikes/${bikeId}/edit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                field: field,
                value: value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cell content
                const cell = row.querySelector(`[data-field="${field}"]`);
                if (field === 'bike_type') {
                    const typeLabels = {
                        'MTB': 'Mountain Bike',
                        'Road': 'Road Bike',
                        'Hybrid': 'Hybrid Bike',
                        'Cruiser': 'Cruiser Bike',
                        'BMX': 'BMX Bike',
                        'Electric': 'Electric Bike'
                    };
                    cell.textContent = typeLabels[value] || value;
                } else {
                    cell.textContent = value;
                }

                // Restore original actions
                row.querySelector('.actions-cell').innerHTML = originalActions;
                editingRow = null;

                // Show success message
                showMessage('Bike updated successfully!', 'success');
            } else {
                showMessage('Error updating bike: ' + (data.error || 'Unknown error'), 'error');
                cancelEdit(row, originalActions);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error updating bike', 'error');
            cancelEdit(row, originalActions);
        });
    }

    function cancelEdit(row, originalActions) {
        // Restore original content
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const field = cell.dataset.field;
            const originalValue = cell.dataset.originalValue;
            cell.textContent = originalValue;
        });

        // Restore actions
        row.querySelector('.actions-cell').innerHTML = originalActions;
        editingRow = null;
    }

    function showMessage(message, type) {
        // Create and show a temporary message
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; position: fixed;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        document.body.appendChild(alertDiv);

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                $(alertDiv).alert('close');
            }
        }, 3000);
    }

    // Delete bike functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-bike-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.delete-bike-btn');
            const bikeId = btn.dataset.bikeId;
            const bikeName = btn.dataset.bikeName;

            if (confirm(`Are you sure you want to delete "${bikeName}"?`)) {
                fetch(`/dashboard/bikes/${bikeId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        btn.closest('tr').remove();
                        showMessage('Bike deleted successfully!', 'success');
                    } else {
                        showMessage('Error deleting bike: ' + (data.error || 'Unknown error'), 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error deleting bike', 'error');
                });
            }
        }
    });
});