const email_messages = document.getElementById('email-messages')
document.getElementById("send-email-btn").addEventListener("click",async ()=>{
    
    const customerId = localStorage.getItem("current_customer_id");
    const ticketId = localStorage.getItem("current_ticket");
    const email = document.getElementById("emailInput").value.trim();
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const response = await fetch("/repairs/email-tickets/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            customer_id: customerId,
            ticket_id: ticketId,
            email:email  
        })
    });
    // 10/5088/
    const data = await response.json();
    
    if (response.ok) {
    
        alert("Email sent successfully. The user will recieve the email in a while.")
    } else {
     
        // email_messages.textContent = "Email not sent. Error occured."
        alert("Email not sent. Error occured.")
    }
});

document.addEventListener('DOMContentLoaded', async () => {
    const ticketId = localStorage.getItem("current_ticket")
    const customerId = localStorage.getItem('current_customer_id');
    const invoice_ticket_id_field = document.getElementById('ticket_id')
    invoice_ticket_id_field.value = ticketId;
    try {
        const response = await fetch(`/repairs/customer-email/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ customer_id: customerId })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.email) {
                document.getElementById('emailInput').value = data.email;
            }
        } else {
            console.error('Error fetching email:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }

    const logged_in_user = localStorage.getItem('logged_in_user_id')
    const repairsBtn = document.getElementById("repairs-list-btn").addEventListener('click',()=>{
        window.location.href = `/repairs/tickets/${logged_in_user}/`;
    })

    const invoiceField = document.getElementById("invoice");
    
    // Add the text "List of all items in this invoice" to the table
    const firstRow = document.querySelector("#invoice-items tbody tr");
    if (firstRow) {  
        const infoTextDiv = document.createElement("h3");
        infoTextDiv.textContent = "Invoice Items";
        firstRow.insertAdjacentElement("afterend", infoTextDiv);
    }
});



// Printing functionality///////////////////////////

// Get all dropdown links
const dropdownLinks = document.querySelectorAll('.print-dropdown-menu a');

// Attach event listener to each link
dropdownLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior

        const selectedOption = link.getAttribute('data-option');

        // Perform action based on selection
        if (selectedOption === "full-page") {
            printSection()
        } else if (selectedOption === "thermal") {
            // 
        } else if (selectedOption === "email") {
            const email_container = document.getElementById('email-container')
            email_container.classList.add("email_flex")
        }
    });
});



// Hide Email Container 
function hideEmailContainer(){
    const email_container = document.getElementById('email-container')
    email_container.classList.add("hide")
}

const statusSelect = document.getElementById("statusSelect");
const statusMessage = document.getElementById("statusMessage");
const ticketId = localStorage.getItem("current_ticket");

if (!statusSelect) {
    console.error("Status select element not found.");
}

// Ensure ticketId is available
if (!ticketId) {
    showMessage("No ticket ID found. Cannot update status.", "red");
}

// Event listener for status change
statusSelect.addEventListener("change", async () => {
    const newStatus = statusSelect.value;

    try {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        if (!csrfToken) {
            showMessage("CSRF token missing. Cannot update.", "red");
            return;
        }

        // Send PATCH request to update status
        const response = await fetch(`/repairs/ticket/${ticketId}/update/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ status: newStatus })
        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message || "Status updated successfully.", "green");
        } else {
            showMessage(result.message || "Failed to update status.", "red");
            console.error("API Errors:", result.errors);
        }
    } catch (error) {
        console.error("Error:", error);
        showMessage("An error occurred. Please try again.", "red");
    }
});


// Helper function to display messages
function showMessage(message, color) {
    const messageElem = document.getElementById("message");
    messageElem.style.color = color;
    messageElem.innerText = message;
}



const descriptiontForm = document.getElementById("descriptionForm");
const message = document.getElementById("description_message");

descriptiontForm.addEventListener("submit", async (e)=> {
    e.preventDefault();

    // const customer = localStorage.getItem('current_customer_id')
    const description = document.getElementById("descriptionInput").value;
    const ticket =  localStorage.getItem('current_ticket')

    if (!description.trim()) {
        message.textContent = "Description  is required.";
        return;
    }

    const payload = {
        ticket_id: ticket,
        description:description
    };

    try {
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        const response = await fetch("/repairs/description/add/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add description.");
        }

        message.textContent = "Description added successfully!";
        const description_list = document.getElementById("description_list")
        const li = document.createElement('li')
        li.textContent = description 
        description_list.append(li)
        // clear the form
        descriptiontForm.reset()
        // close the modal form
            closeModal()
    } catch (error) {
        message.textContent = error.message || "An error occurred.";
    }
});





const technicianSelect = document.getElementById('technician-select');

    technicianSelect.addEventListener('change', async function() {
        const technicianId = this.value;
        const ticketId =localStorage.getItem('current_ticket')

        if (!technicianId) {
            alert('Please select a technician.');
            return;
        }
        if (!ticketId) {
            alert('Please select a ticket.');
            return;
        }
        try {
            const response = await fetch(`/repairs/set-technician/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // Include CSRF token 
                },
                body: JSON.stringify({ 
                    ticket_id:ticketId,
                    technician_id: technicianId 
                })
            });

            if (!response.ok) {
                throw new Error('Failed to set technician.');
            }

            const data = await response.json();
            alert('Technician updated successfully!');
            console.log('Response:', data);
        } catch (error) {
            console.error('Error:', error);
            alert('Error updating technician.');
        }
    })

 // Helper function to get CSRF token from the page
 function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


async function getCustomerDetails() {
    const first_name = document.getElementById("first-name");
    const last_name = document.getElementById("last-name");
    const customerEmail = document.getElementById("customer-email");
    const customerPhone = document.getElementById("customer-phone");

    const customerId = localStorage.getItem('current_customer_id');
    try { 
        const response = await fetch(`/api/customers/details/${customerId}/`, {  
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            }
        });
            openModal('spinner')
        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            closeModal()
            openModal('customer-info')
            first_name.value = data.customer_info.first_name;
            last_name.value = data.customer_info.last_name;
            customerEmail.value = data.customer_info.email;
            customerPhone.value = data.customer_info.phone;
            
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error fetching customer:", error);
        closeModal()
        alert("Failed to get customer. Please try again.");
    }
    
}



document.getElementById("customer-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form from reloading the page

    // Collect form data
    const customerId = localStorage.getItem('current_customer_id');
    const first_name = document.getElementById("first-name").value;
    const last_name = document.getElementById("last-name").value;
    const customerEmail = document.getElementById("customer-email").value;
    const customerPhone = document.getElementById("customer-phone").value;

    // Create form data object
    const formData = {
        id: customerId,
        first_name:first_name,
        last_name: last_name,
        email: customerEmail,
        phone: customerPhone
    };
    
    try {
        const response = await fetch("/api/customers/update/", { 
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            alert("Customer updated successfully!");
            closeModal(); // Close the modal after successful update
            // reload the page 
            document.location.reload()
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error updating customer:", error);
        closeModal()
        alert("Failed to update customer. Please try again.");
    }
});






async function getPropertyDetails() {
    const imei_serial_no_field = document.getElementById("imei_serial_no_field");
    const brand_field = document.getElementById("brand_field");
    const model_field = document.getElementById("model_field");
    const more_details = document.getElementById("more_details_field");

    const property_id = document.getElementById('property_id').value.trim();
    try { 
        const response = await fetch(`/repairs/properties/${property_id}/`, {  
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            }
        });
            openModal('spinner')
        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            closeModal()
            openModal('property-info')
            imei_serial_no_field.value = data.imei_serial_no;
            brand_field.value = data.brand;
            model_field.value = data.model;
            more_details.value = data.more_detail;
            
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error fetching customer:", error);
        closeModal()
        alert("Failed to get customer. Please try again.");
        
    }
    
}


document.getElementById("property-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form from reloading the page

    // Collect form data
    const property_id = document.getElementById('property_id').value.trim();
    const imei_serial_no_field = document.getElementById("imei_serial_no_field").value.trim();
    const brand_field = document.getElementById("brand_field").value.trim();
    const model_field = document.getElementById("model_field").value.trim();
    const more_details = document.getElementById("more_details_field").value.trim();

    // Create form data object
    const formData = {
        id: property_id,
        imei_serial_no:imei_serial_no_field,
        brand: brand_field,
        model: model_field,
        more_detail: more_details
    };
    // #  fields = ['id', 'imei_serial_no', 'brand', 'model', 'more_detail'] 
    try {
        const response = await fetch(`/repairs/properties/${property_id}/update/`, { 
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            alert("Property updated successfully!");
            closeModal(); // Close the modal after successful update
            // reload the page 
            document.location.reload()
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error updating property:", error);
        closeModal()
        alert("Failed to update property. Please try again.");
    }
});



async function getTicketDetails() {
    const problemField = document.getElementById("problem_field");
    const dueDateField = document.getElementById("due_date_field");
    const binLocationField = document.getElementById("bin_location_field");

    const ticket_id =  localStorage.getItem('current_ticket')
    try { 
        const response = await fetch(`/repairs/ticket-detail/${ticket_id}/`, {  
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            }
        });
            openModal('spinner')
        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            closeModal()
            openModal('ticket-info')
            problemField.value = data.problem;
            dueDateField.value = data.due_date;
            binLocationField.value = data.bin_location; 
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error fetching ticket:", error);
        closeModal()
        alert("Failed to get Ticket. Please try again.");
        
    }
    
}





document.getElementById("ticket-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form from reloading the page

    // Collect form data
    const problemField = document.getElementById('problem_field').value.trim();
    const dueDateField = document.getElementById("due_date_field").value.trim();
    const binLocationField = document.getElementById("bin_location_field").value.trim();
    const ticketId =  localStorage.getItem('current_ticket')
    // Create form data object
    const formData = {
        ticket_id: ticketId,
        problem:problemField,
        due_date: dueDateField,
        bin_location: binLocationField
    };
    // #  fields = ['id', 'imei_serial_no', 'brand', 'model', 'more_detail'] 
    try {
        const response = await fetch(`/repairs/ticket/${ticketId}/update/detail/`, { 
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken() // CSRF token for Django security
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json(); // Parse JSON response

        if (response.ok) {
            alert("Ticket updated successfully!");
            closeModal(); // Close the modal after successful update
            // reload the page 
            document.location.reload()
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error("Error updating ticket:", error);
        closeModal()
        alert("Failed to update ticket. Please try again.");
    }
});
