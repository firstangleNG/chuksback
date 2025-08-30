const disclaimerText = `When replacing a faulty motherboard of your computer or laptop, please
  be aware that if BitLocker encryption is enabled on your device, 
  you may need to know your BitLocker recovery key or provide us with the 
  necessary details to allow us to boot your computer to Windows. We want to emphasize that
  we are not responsible if you do not have or cannot provide your BitLocker recovery key.
Thank you for your understanding.
  `

// Ticket number
const ticket_no = document.getElementById("ticket-no").textContent;
const invoice_no = document.getElementById("invoice").value;
//   Get customer detail from the page
const customer_name = document.getElementById("customer_name").textContent;
const customer_email = document.getElementById("customer_email").textContent;
const customer_phone = document.getElementById("customer_phone").textContent;


// Property info
const imei_serial_no = document.getElementById("imei_serial_no").textContent; 
const brand = document.getElementById("brand").textContent;
const model = document.getElementById("model").textContent;
const more_details = document.getElementById("more_details").textContent;



// Ticket info
const problem = document.getElementById("problem").textContent; 
const due_date = document.getElementById("due_date").textContent;
const bin_location = document.getElementById("bin_location").textContent;
const technician = document.getElementById("technician").textContent;
const salesman = document.getElementById("salesman").textContent;


// Use a direct path 
const logoUrl = "/static/images/computer_hub_uk.png";

 // Print Invoice Functionality
function printSection(){

    // Get all Descriptions 
const descriptions = document.querySelectorAll('.description');
let descriptionText = '';

descriptions.forEach((desc,index) => {
    descriptionText += `<diV>${index+1}. ${desc.innerHTML}</div>`; // Appends each description's HTML content
});



const subtotal = document.getElementById('subtotal')?.textContent || '0.00';
const totalTax = document.getElementById('total-tax')?.textContent || '0.00';
const finalAmount = document.getElementById('final-amount')?.textContent || '0.00';


const rows = document.querySelectorAll('.invoice-tr');


let itemsHtml = '';

rows.forEach(row => {
    const serviceName = row.querySelector('input[name="service_name"]')?.value || 'N/A';
    const description = row.querySelector('input[name="description"]')?.value || 'N/A';
    const quantity = row.querySelector('input[name="quantity"]')?.value || '0';
    const price = row.querySelector('input[name="price_per_unit"]')?.value || '0.00';
    const tax = row.querySelector('input[name="tax"]')?.value || '0.00';
    const total = row.querySelector('.total')?.textContent || '0.00';

    itemsHtml += `
        <tr>
            <td>${serviceName}</td>
            <td>${description}</td>
            <td>${quantity}</td>
            <td>${price}</td>
            <td>${tax}</td>
            <td>${total}</td>
        </tr>`;
});
            

      const printContent =  `
      <html>
              
                 <p style="text-align:center;margin-bottom:15px"><strong>Repairs ticket  #${ticket_no}</strong></p>

                 <!-- Brand Logo and Title -->
                 <div id="brand-container">
                    <img id="brand-logo" src="${logoUrl}" alt="Logo">
                    <div id="barnd_name_email_container">
                        <p id="brand_name">Computer Hub United Kingdom</p>
                        <small style="text-align:right;font-size:12px;">info@computerhubuk.com</small>
                    </div>
                </div>
                
                <p style='font-size:11px;'><strong>Disclaimer</strong></p>
                <p id="disclaimer_print">${disclaimerText}</p>

                <!-- customer info -->
                <div id="customer-info-repair-details"> 
                    <div id="customer-info">
                        <p><strong>Customer Details</strong></p>
                        <p><strong>Name :</strong>${customer_name}</p>
                        <p><strong>Email :</strong>${customer_email}</p>
                        <p><strong>Phone :</strong>${customer_phone}</p>
                              <!-- Property info -->
                        <p><strong>Property Details</strong></p>
                        <p><strong>IMEI/Serial No :</strong>${imei_serial_no}</p>
                        <p><strong>Brand :</strong>${brand}</p>
                        <p><strong>Model :</strong>${model}</p>
                        <p><strong>More Detail :</strong>${more_details}</p>
                        
                    </div>

                    <div id="ticket-info">
                             <!-- Ticket info -->
                        <p><strong>Ticket Details</strong></p>
                        <p><strong>Problem :</strong>${problem}</p>
                        <p><strong>Due Date :</strong>${due_date}</p>
                        <p><strong>Bin Location :</strong>${bin_location}</p>
                        <p><strong>Technician :</strong>${technician}</p>
                         <p><strong>Salesman :</strong>${salesman}</p>
                    </div>
                </div>
            
                <div id="descriptions">
                <p><strong>Description</strong></p>
                ${
                   descriptionText 
                }
                </div>

               
                <h3>Invoice Items  <span style="margin-left:20px;"><strong>Inoice#${invoice_no}</strong></h3>
                <table>
                    <thead>
                        <tr>
                            <th>Service Name</th>
                            <th>Description</th>
                            <th>Quantity</th>
                            <th>Price per Unit</th>
                            <th>Taxes (%)</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemsHtml}
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td><strong>Subtotal</strong></td>
                            <td>${subtotal}</td>
                        </tr>
                        
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td><strong>Total Tax</strong></td>
                            <td>${totalTax}</td>
                        </tr>

                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td><strong>Grand Total</strong></td>
                            <td><strong>${finalAmount}</strong></td>
                        </tr>
                         
                    </tbody>
                    </tbody>
                </table>
                <!-- Bank Detail -->
                <p id="bank-detail"><strong>Our Bank Details: Metro Bank , SC: 23-05-80, AC: 45688144</strong></p>

                <!-- Terms and conditions -->
                <p class="terms-header"><strong>Terms and Conditions:</strong></p>
                    <ol>
                        <li><strong>Ownership of Goods</strong>
                            <p>All items left for repair shall remain the property of Computer Hub UK Limited until full payment is received.</p>
                        </li>
                        <li><strong>Damages and Shortages</strong>
                            <p>Any damages or shortages of items sold or repaired must be reported to CHUK either at the time of delivery or within 24 hours of receiving the service.</p>
                        </li>
                        <li><strong>Refunds and Exchanges</strong>
                            <p>We do not offer refunds for sold items, but we do allow exchanges for items of equal value in our store or issue store credit notes that can be used for future purchases or repairs.</p>
                        </li>
                        <li><strong>Book-in Fee</strong>
                            <p>The book-in fee is non-refundable if you choose not to proceed with the repair; otherwise, it will go towards the cost of repairs.</p>
                        </li>
                        <li><strong>Shipping Responsibility</strong>
                            <p>We have no control over shipping and cannot be held responsible for delays caused by external factors such as strikes, natural disasters, or supplier shortages.</p>
                        </li>
                        <li><strong>Repair Estimates</strong>
                            <p>When we provide you with an estimate, it signifies the receipt of your item(s) for repair. Please note that repair timelines may depend on the response time from third-party parts suppliers.</p>
                        </li>
                        <li><strong>Additional Information</strong>
                            <p>Kindly refer to the "Notes" section of the invoice for specific details regarding the type of repair performed.</p>
                        </li>
                        <li><strong>Pricing and Exchange Rates</strong>
                            <p>Prices are valid for the day the invoice was issued, and we do not have control over exchange rates and fluctuations.</p>
                        </li>
                    </ol>

            </body>
        ` //End of interpolation string symbol
    

             
    // Open the print dialog for the current page
    const originalContents = document.body.innerHTML; // Save the original content
    document.body.innerHTML = printContent; // Replace the page content with the printable content
        
    // Dynamically set the logo image URL
    document.getElementById("brand-logo").src = logoUrl;

    window.print(); // Trigger the print dialog
    document.body.innerHTML = originalContents; // Restore the original content after printing
    document.location.reload()
}




// #brand-container{width:100%;height:60px;display:flex;justify-content:center;}
//                     #brand-logo{width:70%;height:90%}

// <p style="text-align:center;"><strong>Repairs ticket</strong><span style="margin-left:20px">Ticket#${ticket_no}</span></p>

// <!-- Brand Logo and Title -->
// <div id="brand-container">
//     <img id="brand-logo" src="${logoUrl}" alt="Logo">
// </div>

{/* <h2>Computer Hub UK United Kingdom</h2>
<small style="text-align:center">info@computerhubuk.com</small>
<p><strong>Disclaimer</strong></p>
<p>${disclaimerText}</p> */}

// // /////