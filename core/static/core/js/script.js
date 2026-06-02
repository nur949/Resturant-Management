document.addEventListener('DOMContentLoaded', function() {
    // Helper function for CSRF token
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

    // Add Item to Order
    const addButtons = document.querySelectorAll('.add-item-btn');
    addButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.dataset.orderId;
            const itemId = this.dataset.itemId;
            const quantity = 1; // Default to 1 for now

            const formData = new FormData();
            formData.append('order_id', orderId);
            formData.append('item_id', itemId);
            formData.append('quantity', quantity);

            fetch('/ajax/add-order-item/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the UI
                    location.reload(); // Simplest way to reflect changes for now
                }
            });
        });
    });

    // Update Order Status
    const statusSelect = document.getElementById('order-status-select');
    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            const orderId = this.dataset.orderId;
            const status = this.value;
            const paymentMethod = document.getElementById('payment-method-select')?.value || 'cash';
            const taxRate = document.getElementById('tax-rate-input')?.value || 0;

            const formData = new FormData();
            formData.append('order_id', orderId);
            formData.append('status', status);
            formData.append('payment_method', paymentMethod);
            formData.append('tax_rate', taxRate);

            fetch('/ajax/update-order-status/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (status === 'paid') {
                        window.location.href = '/orders/';
                    } else {
                        location.reload();
                    }
                }
            });
        });
    }

    // --- Professional Action Dropdowns with Sidebar Focus Mode ---
    document.addEventListener('click', function(e) {
        const toggle = e.target.closest('.action-btn-toggle');
        const allMenus = document.querySelectorAll('.action-menu-content');
        const sidebar = document.getElementById('mainSidebar');
        const mainContent = document.querySelector('.main-content');

        if (toggle) {
            const menu = toggle.nextElementSibling;
            const isShowing = menu.classList.contains('show');
            
            // Hide all other menus first
            allMenus.forEach(m => m.classList.remove('show'));
            
            // Toggle current menu
            if (!isShowing) {
                menu.classList.add('show');
                // AUTO-CLOSE SIDEBAR (Focus Mode)
                sidebar.classList.add('collapsed');
                mainContent.classList.add('expanded');
            } else {
                // If closing menu manually, restore sidebar
                sidebar.classList.remove('collapsed');
                mainContent.classList.remove('expanded');
            }
        } else {
            // Clicked outside - hide all menus and RESTORE sidebar
            let clickedInsideMenu = false;
            allMenus.forEach(m => {
                if (m.contains(e.target)) clickedInsideMenu = true;
                m.classList.remove('show');
            });
            
            if (!clickedInsideMenu) {
                sidebar.classList.remove('collapsed');
                mainContent.classList.remove('expanded');
            }
        }
    });

    // --- Top Header Profile Dropdown ---
    const profileToggle = document.getElementById('profileDropdownToggle');
    const profileMenu = document.getElementById('profileMenu');

    if (profileToggle) {
        profileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            profileMenu.classList.toggle('show');
            // Hide notification dropdown if open
            if (notifDropdown) notifDropdown.classList.remove('show');
        });
    }

    // --- Real-time Notifications ---
    const notifToggle = document.getElementById('notificationToggle');
    const notifDropdown = document.getElementById('notificationDropdown');
    const notifList = document.getElementById('notificationList');
    const notifDot = document.getElementById('notifDot');
    const notifCountBadge = document.getElementById('notifCount');

    function fetchNotifications() {
        fetch('/ajax/notifications/')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const count = data.count;
                    if (count > 0) {
                        notifDot.style.display = 'block';
                        notifCountBadge.innerText = count + ' New';
                        
                        let html = '';
                        data.notifications.forEach(n => {
                            html += `
                                <div class="notification-item unread" onclick="markAsRead(${n.id})">
                                    <div class="notification-icon-circle"><i class="fas fa-info-circle"></i></div>
                                    <div class="notification-content">
                                        <div class="notification-title">${n.title}</div>
                                        <div class="notification-text">${n.message}</div>
                                        <div class="notification-time">${n.time}</div>
                                    </div>
                                </div>
                            `;
                        });
                        notifList.innerHTML = html;
                    } else {
                        notifDot.style.display = 'none';
                        notifCountBadge.innerText = '0 New';
                        notifList.innerHTML = '<div class="p-2 text-center text-muted">No new alerts.</div>';
                    }
                }
            });
    }

    window.markAsRead = function(id) {
        const formData = new FormData();
        fetch(`/ajax/notifications/${id}/read/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: formData
        }).then(() => fetchNotifications());
    }

    if (notifToggle) {
        notifToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            notifDropdown.classList.toggle('show');
            // Hide profile menu if open
            if (profileMenu) profileMenu.classList.remove('show');
        });
    }

    // Close all dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (profileToggle && !profileToggle.contains(e.target)) profileMenu?.classList.remove('show');
        if (notifToggle && !notifToggle.contains(e.target)) notifDropdown?.classList.remove('show');
    });

    // Initial fetch and poll every 60 seconds
    fetchNotifications();
    setInterval(fetchNotifications, 60000);

    // --- Mobile Sidebar Toggle ---
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    const sidebar = document.getElementById('mainSidebar');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                    sidebar.classList.remove('mobile-show');
                }
            }
        });
    }
});
