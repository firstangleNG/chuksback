// Modal toggle functions
function openModal() {
    document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}




 // Search by Ticket ID and Customer Name
 function searchTickets() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#repairTable tbody tr")
  rows.forEach(row => {
      const ticketID = row.children[0].textContent.toLowerCase();
      const customerName = row.children[1].textContent.toLowerCase()
      if (ticketID.includes(input) || customerName.includes(input)) {
          row.style.display = "";
      } else {
          row.style.display = "none";
            }
 });
}

    // Filter table by Status and Technician
    function filterTable() {
        const status = document.getElementById("statusFilter").value.toLowerCase();
        const tech = document.getElementById("techFilter").value.toLowerCase();
        const rows = document.querySelectorAll("#repairTable tbody tr");

        rows.forEach(row => {
            const rowStatus = row.children[5].textContent.toLowerCase();
            const rowTech = row.children[3].textContent.toLowerCase();

            const statusMatch = !status || rowStatus === status;
            const techMatch = !tech || rowTech.includes(tech);

            row.style.display = statusMatch && techMatch ? "" : "none";
        });
    }




document.addEventListener("DOMContentLoaded",()=>{
    const userIdInput = document.getElementById("user-id").value.trim()
    localStorage.setItem("logged_in_user_id",userIdInput)
})