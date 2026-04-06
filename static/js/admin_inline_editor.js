/**
 * Admin Inline Editing System
 * Allows admins to edit content directly from website pages
 */

class AdminEditor {
    constructor() {
        this.isAdmin = this.checkAdminStatus();
        this.editingElement = null;
        
        if (this.isAdmin) {
            this.initializeAdminControls();
            this.setupEventListeners();
        }
    }
    
    checkAdminStatus() {
        const adminStatus = document.body.dataset.isAdmin;
        return adminStatus === 'true' || adminStatus === '1';
    }
    
    initializeAdminControls() {
        // Add admin toolbar
        this.createAdminToolbar();
        
        // Mark editable elements
        this.markEditableElements();
    }
    
    createAdminToolbar() {
        const toolbar = document.createElement('div');
        toolbar.id = 'admin-toolbar';
        toolbar.className = 'admin-toolbar';
        toolbar.innerHTML = `
            <div class="toolbar-content">
                <span class="admin-badge">👨‍💻 ADMIN MODE</span>
                <div class="toolbar-actions">
                    <button class="toolbar-btn" id="toggle-edit-mode" title="Toggle Edit Mode">
                        ✎ Edit Mode
                    </button>
                    <button class="toolbar-btn" id="admin-dashboard" title="Go to Dashboard">
                        📊 Dashboard
                    </button>
                    <button class="toolbar-btn" id="help-btn" title="Help">
                        ? Help
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(toolbar);
        
        this.addToolbarStyles();
    }
    
    addToolbarStyles() {
        if (document.getElementById('admin-toolbar-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'admin-toolbar-styles';
        styles.innerHTML = `
            #admin-toolbar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 0;
                z-index: 10000;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            
            .toolbar-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                padding: 10px 20px;
            }
            
            .admin-badge {
                font-weight: bold;
                font-size: 12px;
                letter-spacing: 1px;
                background: rgba(255, 255, 255, 0.2);
                padding: 4px 10px;
                border-radius: 4px;
            }
            
            .toolbar-actions {
                display: flex;
                gap: 10px;
            }
            
            .toolbar-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .toolbar-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                border-color: white;
            }
            
            body.admin-mode {
                padding-top: 50px;
            }
            
            .editable-element {
                position: relative;
            }
            
            .edit-mode .editable-element {
                border: 2px dashed #667eea;
                padding: 8px;
                border-radius: 4px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .edit-mode .editable-element:hover {
                background: rgba(102, 126, 234, 0.1);
                box-shadow: 0 0 8px rgba(102, 126, 234, 0.3);
            }
            
            .edit-btn {
                position: absolute;
                top: 5px;
                right: 5px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                cursor: pointer;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            .edit-mode .editable-element:hover .edit-btn {
                opacity: 1;
            }
            
            .edit-modal-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 10001;
            }
            
            .edit-modal-overlay.active {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .edit-modal {
                background: white;
                border-radius: 8px;
                padding: 30px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            }
            
            .edit-modal h3 {
                margin-bottom: 20px;
                color: #667eea;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #2c3e50;
            }
            
            .form-group input,
            .form-group textarea,
            .form-group select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-family: inherit;
            }
            
            .modal-actions {
                display: flex;
                gap: 10px;
                justify-content: flex-end;
                margin-top: 20px;
            }
            
            .modal-btn {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .modal-btn-save {
                background: #667eea;
                color: white;
            }
            
            .modal-btn-save:hover {
                background: #5568d3;
            }
            
            .modal-btn-cancel {
                background: #ecf0f1;
                color: #2c3e50;
            }
            
            .modal-btn-cancel:hover {
                background: #bdc3c7;
            }
            
            .toast-notification {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border-radius: 4px;
                padding: 15px 20px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                z-index: 10002;
                animation: slideIn 0.3s ease-out;
            }
            
            .toast-notification.success {
                border-left: 4px solid #27ae60;
            }
            
            .toast-notification.error {
                border-left: 4px solid #e74c3c;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    markEditableElements() {
        // Mark bike items as editable
        document.querySelectorAll('[data-editable]').forEach(element => {
            element.classList.add('editable-element');
            
            if (!element.querySelector('.edit-btn')) {
                const editBtn = document.createElement('button');
                editBtn.className = 'edit-btn';
                editBtn.innerHTML = '✎';
                editBtn.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.openEditModal(element);
                };
                element.appendChild(editBtn);
            }
        });
    }
    
    setupEventListeners() {
        // Toggle edit mode
        document.getElementById('toggle-edit-mode')?.addEventListener('click', () => {
            document.body.classList.toggle('edit-mode');
            localStorage.setItem('admin-edit-mode', document.body.classList.contains('edit-mode'));
        });
        
        // Dashboard link
        document.getElementById('admin-dashboard')?.addEventListener('click', () => {
            window.location.href = '/dashboard/';
        });
        
        // Restore edit mode preference
        if (localStorage.getItem('admin-edit-mode') === 'true') {
            document.body.classList.add('edit-mode');
        }
    }
    
    openEditModal(element) {
        const elementType = element.dataset.editable;
        const elementId = element.dataset.id;
        
        // Create modal
        const overlay = document.createElement('div');
        overlay.className = 'edit-modal-overlay active';
        
        const modal = document.createElement('div');
        modal.className = 'edit-modal';
        
        if (elementType === 'bike') {
            modal.innerHTML = this.getBikeEditForm(element);
        } else if (elementType === 'location') {
            modal.innerHTML = this.getLocationEditForm(element);
        }
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
        
        // Close modal on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.remove();
            }
        });
    }
    
    getBikeEditForm(element) {
        const bikeId = element.dataset.id;
        const bikeName = element.dataset.name || '';
        const bikePrice = element.dataset.price || '';
        
        return `
            <h3>Edit Bike</h3>
            <form onsubmit="return adminEditor.saveBike(event, ${bikeId})">
                <div class="form-group">
                    <label>Bike Name</label>
                    <input type="text" id="bike-name" value="${bikeName}" required>
                </div>
                <div class="form-group">
                    <label>Hourly Price (₹)</label>
                    <input type="number" id="bike-price" value="${bikePrice}" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="bike-available"> Available
                    </label>
                </div>
                <div class="modal-actions">
                    <button type="button" class="modal-btn modal-btn-cancel" onclick="this.closest('.edit-modal-overlay').remove()">
                        Cancel
                    </button>
                    <button type="submit" class="modal-btn modal-btn-save">
                        Save Changes
                    </button>
                </div>
            </form>
        `;
    }
    
    getLocationEditForm(element) {
        const locationId = element.dataset.id;
        const locationName = element.dataset.name || '';
        const locationIcon = element.dataset.icon || '';
        
        return `
            <h3>Edit Location</h3>
            <form onsubmit="return adminEditor.saveLocation(event, ${locationId})">
                <div class="form-group">
                    <label>Location Name</label>
                    <input type="text" id="location-name" value="${locationName}" required>
                </div>
                <div class="form-group">
                    <label>Icon/Emoji</label>
                    <input type="text" id="location-icon" value="${locationIcon}" maxlength="2" required>
                </div>
                <div class="modal-actions">
                    <button type="button" class="modal-btn modal-btn-cancel" onclick="this.closest('.edit-modal-overlay').remove()">
                        Cancel
                    </button>
                    <button type="submit" class="modal-btn modal-btn-save">
                        Save Changes
                    </button>
                </div>
            </form>
        `;
    }
    
    saveBike(event, bikeId) {
        event.preventDefault();
        
        const name = document.getElementById('bike-name').value;
        const price = document.getElementById('bike-price').value;
        const available = document.getElementById('bike-available').checked;
        
        fetch(`/api/admin/bike/${bikeId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify({
                name: name,
                rental_price_hourly: price,
                is_available: available
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Bike updated successfully!', 'success');
                document.querySelector('.edit-modal-overlay').remove();
                // Reload to show changes
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showNotification('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            this.showNotification('Error: ' + error, 'error');
        });
        
        return false;
    }
    
    saveLocation(event, locationId) {
        event.preventDefault();
        
        const name = document.getElementById('location-name').value;
        const icon = document.getElementById('location-icon').value;
        
        fetch(`/api/admin/location/${locationId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify({
                name: name,
                icon: icon
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Location updated successfully!', 'success');
                document.querySelector('.edit-modal-overlay').remove();
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showNotification('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            this.showNotification('Error: ' + error, 'error');
        });
        
        return false;
    }
    
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `toast-notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
    }
}

// Initialize admin editor when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.adminEditor = new AdminEditor();
    });
} else {
    window.adminEditor = new AdminEditor();
}
