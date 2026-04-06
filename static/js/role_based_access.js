/**
 * Role-Based Access Control System
 * Manages admin UI visibility and user interactions based on user role
 */

class RoleBasedAccess {
    constructor() {
        this.isAdmin = this.checkAdminStatus();
        this.init();
    }

    /**
     * Check if current user is admin
     */
    checkAdminStatus() {
        const adminStatus = document.body.dataset.isAdmin;
        return adminStatus === 'true' || adminStatus === '1';
    }

    /**
     * Initialize role-based access controls
     */
    init() {
        if (this.isAdmin) {
            this.initAdminFeatures();
        } else {
            this.initUserFeatures();
        }
        
        // Initialize toast notifications
        this.setupToasts();
        
        // Initialize loading indicators
        this.setupLoadingIndicators();
    }

    /**
     * Initialize admin-specific features
     */
    initAdminFeatures() {
        // Show admin-only elements
        this.showAdminElements();
        
        // Add edit hover effects
        this.setupEditHoverEffects();
        
        // Setup admin buttons
        this.setupAdminButtons();
    }

    /**
     * Initialize user-specific features
     */
    initUserFeatures() {
        // Hide all admin elements - they're already hidden via CSS
        // but we can add event listeners for user features
        this.setupUserBookingFlow();
    }

    /**
     * Show all admin-only elements
     */
    showAdminElements() {
        const adminElements = document.querySelectorAll('[data-admin-only="true"]');
        adminElements.forEach(el => {
            el.classList.remove('d-none');
            el.style.display = '';
        });
    }

    /**
     * Setup edit hover effects for admin
     */
    setupEditHoverEffects() {
        const editableItems = document.querySelectorAll('[data-editable="bike"], [data-editable="location"]');
        
        editableItems.forEach(item => {
            // Add hover class for visual feedback
            item.addEventListener('mouseenter', () => {
                if (this.isAdmin) {
                    item.classList.add('admin-hover');
                    // Show edit icon
                    const editIcon = item.querySelector('[data-edit-icon]');
                    if (editIcon) {
                        editIcon.style.opacity = '1';
                    }
                }
            });

            item.addEventListener('mouseleave', () => {
                item.classList.remove('admin-hover');
                const editIcon = item.querySelector('[data-edit-icon]');
                if (editIcon) {
                    editIcon.style.opacity = '0';
                }
            });
        });
    }

    /**
     * Setup admin action buttons
     */
    setupAdminButtons() {
        // Admin buttons are already set up by admin_inline_editor.js
        // This just ensures they're properly connected
        const adminButtons = document.querySelectorAll('[data-admin-action]');
        adminButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleAdminAction(e);
            });
        });
    }

    /**
     * Handle admin action clicks
     */
    handleAdminAction(event) {
        const action = event.target.dataset.adminAction;
        const target = event.target.dataset.actionTarget;
        
        switch(action) {
            case 'edit':
                this.showEditModal(target);
                break;
            case 'delete':
                this.showDeleteConfirm(target);
                break;
            case 'add':
                this.showAddModal(target);
                break;
        }
    }

    /**
     * Setup user booking flow
     */
    setupUserBookingFlow() {
        const bookingButtons = document.querySelectorAll('[data-action="book"]');
        bookingButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showNotification('Redirecting to booking form...', 'info');
            });
        });
    }

    /**
     * Setup toast notification system
     */
    setupToasts() {
        // Create toast container if not exists
        if (!document.getElementById('toast-container')) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
            
            // Add CSS for toasts
            this.addToastStyles();
        }
    }

    /**
     * Add CSS styles for toast notifications
     */
    addToastStyles() {
        const style = document.createElement('style');
        style.innerHTML = `
            .toast-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            }

            .toast-message {
                background: white;
                border-left: 4px solid #FF6B6B;
                padding: 16px;
                margin-bottom: 10px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                animation: slideIn 0.3s ease-out;
                display: flex;
                align-items: center;
                gap: 12px;
                max-width: 100%;
            }

            .toast-message.success {
                border-left-color: #27ae60;
                background: #f0fdf4;
            }

            .toast-message.success .toast-icon {
                color: #27ae60;
            }

            .toast-message.error {
                border-left-color: #e74c3c;
                background: #fef2f2;
            }

            .toast-message.error .toast-icon {
                color: #e74c3c;
            }

            .toast-message.info {
                border-left-color: #3498db;
                background: #f0f9ff;
            }

            .toast-message.info .toast-icon {
                color: #3498db;
            }

            .toast-message.warning {
                border-left-color: #f39c12;
                background: #fffbf0;
            }

            .toast-message.warning .toast-icon {
                color: #f39c12;
            }

            .toast-icon {
                font-size: 1.2rem;
                min-width: 24px;
            }

            .toast-content {
                flex: 1;
                color: #2c3e50;
                font-weight: 500;
            }

            .toast-close {
                background: none;
                border: none;
                cursor: pointer;
                color: #7f8c8d;
                font-size: 1.2rem;
                padding: 0;
                margin-left: 8px;
            }

            .toast-close:hover {
                color: #2c3e50;
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

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Show toast notification
     */
    showNotification(message, type = 'info', duration = 4000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast-message ${type}`;
        
        // Map type to icon
        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-content">${message}</div>
            <button class="toast-close">×</button>
        `;

        container.appendChild(toast);

        // Close button
        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.removeToast(toast);
        });

        // Auto remove
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);
    }

    /**
     * Remove toast with animation
     */
    removeToast(toast) {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }

    /**
     * Setup loading indicators
     */
    setupLoadingIndicators() {
        // Add loading overlay styles
        const style = document.createElement('style');
        style.innerHTML = `
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.4);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 9998;
                animation: fadeIn 0.3s ease-out;
            }

            .loading-overlay.active {
                display: flex;
            }

            .spinner {
                width: 50px;
                height: 50px;
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .btn-loading {
                position: relative;
                color: transparent;
            }

            .btn-loading::after {
                content: '';
                position: absolute;
                width: 16px;
                height: 16px;
                top: 50%;
                left: 50%;
                margin-left: -8px;
                margin-top: -8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 0.6s linear infinite;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Show loading overlay
     */
    showLoading(message = 'Loading...') {
        let overlay = document.getElementById('loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div style="text-align: center;">
                    <div class="spinner"></div>
                    <p style="color: white; margin-top: 20px; font-weight: 500;">${message}</p>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        overlay.classList.add('active');
    }

    /**
     * Hide loading overlay
     */
    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('active');
            setTimeout(() => overlay.remove(), 300);
        }
    }

    /**
     * Show edit modal (for admin)
     */
    showEditModal(target) {
        this.showNotification(`Edit mode for ${target}`, 'info');
    }

    /**
     * Show delete confirmation
     */
    showDeleteConfirm(target) {
        this.showNotification(`Are you sure you want to delete?`, 'warning');
    }

    /**
     * Show add modal
     */
    showAddModal(target) {
        this.showNotification(`Add new ${target}`, 'info');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.roleBasedAccess = new RoleBasedAccess();
});
