
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const body = document.body;

    sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
    body.classList.toggle('no-scroll'); // Prevents scrolling when sidebar is open
}
 
// const dropdownBtn = document.getElementById('inventoryDropdownBtn');
// const dropdownContent = document.getElementById('inventoryDownContent');

// dropdownBtn.addEventListener('mouseenter', () => {
//     dropdownContent.classList.add('show-inventory-items');
// });

// dropdownBtn.addEventListener('click', () => {
//     if (document.location.href =="/inventory/"){
//         dropdownContent.classList.toggle('show-inventory-items');
//     }
   
// });

// document.addEventListener('click', (event) => {
//     if (!dropdownBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
//         dropdownContent.classList.remove('show-inventory-items');
//     }
// });





// Functionality for all modals

function openModal(modalId) {
    // Hide all modals before showing the selected one
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = "none";
    });

    // Show only the selected modal
    document.getElementById(modalId).style.display = "flex";
}

function closeModal() {
    // Hide all modals when close button is clicked
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = "none";
    });
}