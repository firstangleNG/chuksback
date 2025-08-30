const currentCustomerIdField = document.getElementById("customer-id")
const messages = document.getElementById("new-user-messages")
const property = document.getElementById("property-id")

function toggleDropdowInputFields(dropdownElement,inputElement) {
    let dropdown = document.getElementById(dropdownElement);
    let input = document.getElementById(inputElement);

    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
        input.style.display = "none";
        input.value =""; //clear the input field
    } else {
        dropdown.style.display = "none";
        input.style.display = "block";
        input.focus(); // Auto-focus input when it appears
    }
}






// Adding new customer////////////////////////////////
document.getElementById("new-user-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent normal form submission

    // Get form values
  
        const first_name =  document.getElementById("firstName").value;
         const last_name = document.getElementById("lastName").value;
         const  email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;
        const secondary_phone = document.getElementById("alt-phone").value;
        const fax = document.getElementById("fax").value;
        const address = document.getElementById("address").value;
        const company =  document.getElementById("company").value;
    let formData = {
        first_name:first_name,
        last_name:last_name,
        email:email,
        phone:phone,
        secondary_phone:secondary_phone,
        fax:fax,
        address:address,
        company:company
    };
    // Get CSRF token
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
   
    try {
        let response = await fetch("/api/customers/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(formData)
        });

        let data = await response.json();

        if (response.ok) {
        const currentCustomerIdField = document.getElementById("customer-id")
        const customerSearchField = document.getElementById('customer-search')
        currentCustomerIdField.value = data.customer;
        localStorage.setItem('current_customer_id',data.customer)
        customerSearchField.value = `${first_name} ${last_name} - ${email} -${company}`
            messages.classList.add('success')
            messages.textContent = data.message; // Show success message
            document.getElementById("new-user-form").reset(); // Reset form
            // closeModal(); // Close modal after submission
        } else {
            messages.classList.add('error')
            messages.textContent= " Error: " + JSON.stringify(data); // Show error messages
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        messages.classList.add('error')
        messages.textContent="Failed to submit form. Please try again.";
    }
});

// End of adding new customer////////////////////////




// Customer Search Functionality////////////


let timer; // Timer for debouncing

function searchCustomers() {
    clearTimeout(timer); // Clear previous timer

    const resultsParent = document.getElementById("results-parent");
    const customerSearchField = document.getElementById("customer-search");
    let query = customerSearchField.value.trim();
    let resultsContainer = document.getElementById("customers-names-list");

    if (query.length < 2) { // Only search after 2+ characters
        resultsContainer.innerHTML = "";
        resultsParent.classList.remove("show");
        return;
    }

    // Set the debounce delay and fetch the results
    timer = setTimeout(() => {
        fetch(`/api/customers/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = ""; // Clear old results

                if (data.length === 0) {
                    resultsContainer.innerHTML = "<p>No customers found.</p>";
                    resultsParent.classList.add("show");
                    return;
                }

                data.forEach(customer => {
                    const li = document.createElement("li");
                    li.innerHTML = `<strong>${customer.first_name} ${customer.last_name}</strong> - ${customer.email} - ${customer.company}`;
                    li.addEventListener("click", function() {
                        customerSearchField.value = li.textContent;
                        currentCustomerIdField.value = customer.id;
                        localStorage.setItem('current_customer_id', customer.id);
                        resultsParent.classList.remove("show");
                    });
                    resultsContainer.appendChild(li);
                });

                resultsParent.classList.add('show');
            })
            .catch(error => console.error("Error fetching search results:", error));
    }, 200); // 200ms debounce delay
}






// Save Device Property ////////////////////



async function createProperty() {
    // Get input values from the form fields
    const imeiSerialNo = document.getElementById("imei_serial_no").value.trim() || "";
    const brandInput = document.getElementById("brandInput").value.trim();
    const brandDropDown = document.getElementById('brandDropDown').value;
    const modelInput = document.getElementById("modelInput").value.trim();
    const moreDetail = document.getElementById("more_detail").value.trim();
    const devicePropertyModalErrors = document.getElementById("device-property-modal-errors");
    const modelDropDown = document.getElementById('modelDropDown').value;
   
    
    const currentCustomerIdField = document.getElementById("customer-id")

    if (!currentCustomerIdField || currentCustomerIdField.value.trim().length < 1) {
        devicePropertyModalErrors.classList.add('error')
        devicePropertyModalErrors.textContent = "You must create or search a customer before creating a property";
       
        currentCustomerIdField?.focus(); // Bring focus to the field if it exists
        return;
    }
    

    let model = null
    if (modelInput.length < 1){
        model = modelDropDown
    }else{
        model = modelInput
    }

    let brand = null
    if (brandInput.length < 1){
        brand = brandDropDown
    }else{
        brand = brandInput
    }

    // Validate required fields
    if (!brand || !model) {
        devicePropertyModalErrors.classList.add('error');
        devicePropertyModalErrors.textContent = "Please fill in all required fields.";
        return;
    }



    const propertyData = {
        imei_serial_no: imeiSerialNo,
        brand: brand,
        model: model,
        more_detail: moreDetail,
        customer: currentCustomerIdField.value.trim()
    };
      // Get CSRF token
      let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value

    try {
        const response = await fetch("/repairs/properties/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(propertyData)
        });

        if (!response.ok) throw new Error("Error occurred while making request");

        const responseData = await response.json(); // Await JSON response

        if (responseData.success) {
            devicePropertyModalErrors.classList.remove('error');
            devicePropertyModalErrors.classList.add('success');
            devicePropertyModalErrors.textContent = "Property created successfully!";

            addOptionToCustomerDeviceDropdown(responseData.property.id,`${responseData.property.model}  ${responseData.property.brand} ${responseData.property.imei_serial_no}`)
            
        } else {
            throw new Error(responseData.error || "Unknown error occurred");
        }
    } catch (error) {
        console.error("Error:", error);
        devicePropertyModalErrors.classList.add('error');
        devicePropertyModalErrors.textContent = `Error creating property: ${error.message}`;
    }
}

// End of save device property



// Create Ticket functionality///////////////////////////////

async function createRepairTicket() {
    const ticket_id = document.getElementById("ticket_id").textContent.trim()
    const problemsDropDown = document.getElementById("problemsDropDown").value;
    const problemInput = document.getElementById("problemsInput").value.trim();
    const dueDate = document.getElementById("due_date").value.trim();
    const binLocation = document.getElementById("bin_location").value.trim();
    const repairTicketErrors = document.getElementById("repair-ticket-errors");
    const customerIdField = document.getElementById("customer-id").value.trim();
    const property = document.getElementById("customerDeviceDropdown").value.trim();
    const salesman = localStorage.getItem('logged_in_user_id')
    let problem = null
    if (problemInput.length < 1){
        problem = problemsDropDown
    }else{
        problem = problemInput
    }
    if (!customerIdField) { 
        repairTicketErrors.classList.add('error');
        repairTicketErrors.textContent = "Please select a customer or create one.";
        return;
    }
    if (!problem) { 
        repairTicketErrors.classList.add('error');
        repairTicketErrors.textContent = "Please select a problem or create on .";
        return;
    }

    // problemsDropDown  problemsInput
    // Validate required fields
    if (!problem || !dueDate || !property) {
        repairTicketErrors.classList.add('error');
        repairTicketErrors.textContent = "Problem, Due Date, and Property are required.";
        return;
    }

    const ticketData = {
        ticket_id:ticket_id,
        problem: problem,
        due_date: dueDate,
        bin_location: binLocation || null,
        technician: null,
        salesman: salesman,
        amount_due: 0.00,
        total_price: 0.00,
        status: "New", 
        customer: customerIdField,
        property: property
    };
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const response = await fetch("/repairs/tickets/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(ticketData)
        });

       
        if (!response.ok) {
            throw new Error("Failed to create ticket");
        }
        const responseData =  await response.json()
        if(responseData.success){
            repairTicketErrors.classList.remove('error');
            repairTicketErrors.classList.add('success');
            repairTicketErrors.textContent = "Repair ticket created successfully!";
            window.location.replace(`/repairs/summary/${customerIdField}/${ticket_id}/`);
            localStorage.setItem('current_ticket',ticket_id)
        }
        
    } catch (error) {
        console.error("Error:", error);
        repairTicketErrors.classList.add('error');
        repairTicketErrors.textContent = `Error: ${error.message}`;
    }
}



// End of Create Ticket functionality///////////////////////


document.addEventListener("DOMContentLoaded",()=>{
    const currentTicketValue = document.getElementById('ticket_id').textContent
    const logged_in_user = localStorage.getItem('logged_in_user_id')
    const cabcelBtn = document.getElementById("cancel-btn").addEventListener('click',()=>{
        window.location.href = `/repairs/tickets/${logged_in_user}/`;
    })
  
}) 

function addOptionToCustomerDeviceDropdown(value, text) {
    let select = document.getElementById("customerDeviceDropdown");

    // Check if the option already exists
    if (![...select.options].some(opt => opt.value === value)) {
        let opt = document.createElement("option");
        opt.value = value;
        opt.textContent = text;
        // select.appendChild(opt);
        select.insertBefore(opt, select.options[0] || null); 
        select.value = value;
    } else {
        select.value = value;
    }
}
