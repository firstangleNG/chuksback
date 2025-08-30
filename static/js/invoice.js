

document.getElementById('invoice-form').addEventListener('submit', function(event) {
    const invoiceNumber = document.getElementById('invoice_no').value;  // Get the invoice number
    // Save the invoice number to localStorage
    localStorage.setItem('last_invoice_number', invoiceNumber);
});



// Clear form 
const clear_form = document.getElementById("clear-form")
clear_form.addEventListener("click",()=>{
    const form = document.getElementById('invoice-form')
    form.reset()
    window.location.reload()
})



const addItemButton = document.getElementById('add-item');
const itemsTable = document.querySelector('#invoice-items tbody');
// const printButton = document.getElementById('print-invoice');
const invoice_no = document.getElementById('invoice_no').value.trim();


    // Print Invoice Functionality
  function printInvoice(){
    
        const customerName = document.querySelector('input[name="customer_name"]').value;
        const paymentMethod = document.querySelector('select[name="payment_method"]').value;
        const paymentStatus = document.querySelector('select[name="payment_status"]').value;
        const rows = document.querySelectorAll('#invoice-items tbody tr');
       

        let backgroundImageSrc = ''
        let paidSentence = ""
        if(paymentStatus == "Paid"){
            paidSentence = "PAID";
            backgroundImageSrc =  "/static/images/paid.png";           
        }


        // Get the customer email address if provided
        const email_address = document.getElementById('customer_email_field').value || "Not provided"

        // Get number of items texed
        const tax_elements = document.querySelectorAll('select[name="tax[]"]');
        let  number_of_taxed_items_counter = 0;
        tax_elements.forEach(element=>{
           if(parseInt(element.value) > 0){
            number_of_taxed_items_counter ++;
           }
        })

        // Form the tax statement 
        let tax_statement = ""
        number_of_taxed_items_counter > 0?  tax_statement = `( 20% tax inclusive on ${number_of_taxed_items_counter} item(s) )` : tax_statement = "( 0% tax inclusive)"

       
        let itemsHtml = '';
        rows.forEach((row,index) => {
            const serviceName = row.querySelector('input[name="service_name[]"]').value;
            const description = row.querySelector('input[name="description[]"]').value;
            const quantity = row.querySelector('input[name="quantity[]"]').value;
            const price = row.querySelector('input[name="price_per_unit[]"]').value;
            const tax = row.querySelector('select[name="tax[]"]').value;
            const total = row.querySelector('.total').textContent;

            itemsHtml += `
                <tr>
                   <td><strong>${index + 1}</td>
                   <td>${serviceName}</strong><br>${description}</td>
                    <td>${quantity}</td>
                    <td>${price}</td>
                     <td>${parseInt(tax) > 0 ? '20%' : '0%'}</td>
                    <td>${total}</td>
                </tr>`;
        });

        const subtotal = document.getElementById('subtotal').textContent;
        const totalTax = document.getElementById('total-tax').textContent;
        const finalAmount = document.getElementById('final-amount').textContent;

        // Create printable HTML content
        const printContent = `
           <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Invoice - ComputerHubUK</title>
            <style>
             body {
            font-family: Arial, sans-serif;
            line-height: 1.4;
            margin: 0;
            padding: 15px;
            color: #000000;
	    font-size: 12px;
        }
        .invoice-header {
            /* text-align: center; */
            width: 100%;
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            border-bottom: 1px solid #000000;
            padding-bottom: 5px;
        }
        .invoice-header-items{
          flex: 1;
          width: 50%;
        }
        img{
          width: 30%;
          height: 40px;
        }
        .invoice-header h1 {
            color: #000000;
            margin: 0;
            font-size: 16px;
        }
        .invoice-header p {
            margin: 2px 0;
            font-size: 10px;
        }
	.invoice-details {
           width: 100%;
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 10px;
            caption-side: 30px;
        }
        .invoice-detail-single{
          flex:1;
          width: 30%;
        }
        .invoice-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
       
        .invoice-table th, .invoice-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .invoice-table th {
            background-color: #f2f2f2;
        }
        .totals {
            text-align: right;
            margin-bottom: 15px;
            font-size: 10px;
            padding-right: 5px;
        }
        .footer {
            margin-top: 20px;
            font-size: 9px;
            border-top: 1px solid #ddd;
            padding-top: 5px;
        }
        .disclaimer {
            font-style: italic;
            color: #666;
            margin-top: 10px;
            font-size: 8px;
        }
        .small-text {
        font-size: 9px;
        font-weight: bold;
      }
            ul {
        margin: 0;
         }

    ul li {
        margin: 0;
        padding: 0;
        line-height: 1; /* controls vertical spacing between lines */
        font-size: 8px;   
   }
    </style>
</head>
<body>
    <div class="invoice-header">
        <div class="invoice-header-items">
          <img src="https://chukticketingsystem.com/static/images/computer_hub_new.jpeg" alt="Logo"><br>
        </div>
         <div class="invoice-header-items">
          <span id="company-name">Sales Invoice<br>
            <span class="small-text">info@computerhubuk.com</span>
        </div>
        </div>
            <div class="disclaimer">
                        <p><strong>Disclaimer:</strong> <br/> When replacing faulty motherboard of your computer or laptop, please be aware that if BitLocker encryption is enabled on your device,<br/> you may need to know your BitLocker recovery key. We are not responsible if you do not have or cannot provide your BitLocker recovery key.<br/>
                        Thank you for your understanding.</p>
                    </div>
                </div>

                <div class="invoice-details">
                <div class="invoice-detail-single">
                    <p><strong>Bill To:</strong> ${customerName} <br/>
                    <!-- <strong>Address:</strong> 123 Customer Lane, London, UK <br/> -->
                    <strong>Email:</strong> ${email_address}</p>
                </div>
            <div class="invoice-detail-single">
                <p><strong>Sales Technician:</strong> Mr. Williams<br/>
                <strong>Contact:</strong> info@computerhubuk.com | +441793354694/07501241137</p>
            </div>
            <div class="invoice-detail-single">
                <p><strong>Invoice No:</strong>${invoice_no}</p>
                <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>           
            </div>
            </div>

                <p>VAT Number : 353 9011 12</p>
                <h3>Invoice Items</h3>
                <table class="invoice-table">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Description</th>
                            <th>Qty</th>
                            <th>Unit Price</th>
                            <th>Tax</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemsHtml}
                    </tbody>
                </table>

        <div class="totals">
          <p><strong>Total: ${(subtotal).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>${tax_statement}:${(totalTax).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>Grand Total: ${(finalAmount).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          
          
        </div>
    <div class="footer">
        <p><strong>Bank Details:</strong> Bank: Metro Bank; SC: 23-05-80; AC: 45688144
    </div>

        <p><strong>Terms & Conditions:</strong></p>
        <ul class="small-text">
            <li><strong>Ownership of Goods:</strong> All items left for repair shall remain the property of Computer Hub UK Limited until full payment is received.
            <li><strong>Damages and Shortages:</strong> Any damages or shortages of items sold or repaired must be reported to CHUK either at the time of delivery or within 24 hours of receiving the service.
	         <li><strong>Refunds and exchanges:</strong> We do not offer refunds for sold items, but we do allow exchanges for items of equal value in our store or issue store credit notes that can be used for future purchases or repairs.
            <li><strong>Book-in Fee:</strong> The book-in fee is non-refundable if you choose not to proceed with the repair; otherwise, it will go towards the cost of repairs.
             <li><strong>Shipping Responsibility:</strong> We have no control over shipping and cannot be held responsible for delays caused by external factors such as strikes, natural disasters, or supplier shortages.
            <li><strong>Estimates:</strong> When we provide you with an estimate, it signifies the receipt of your item(s) for repair. Please note that repair timelines may depend on the response time from third-party parts suppliers.
            <li><strong>Additional Information:</strong> Kindly refer to the "Notes" section of the invoice for specific details regarding the type of repair performed.
            <li><strong>Pricing and Exchange Rates:</strong> Prices are valid for the day the invoice was issued, and we do not have control over exchange rates and fluctuations.
        </ul>  

               
                    <p style="text-align:center;margin-top:15px;color:red;font-size:20px">${paidSentence}</p>

            </body>
            </html>
        `;

     
        const printWindow = window.open('', '_blank');
        printWindow.document.write(printContent);
        printWindow.document.close();
  
        printWindow.onload = () => {
          const img = printWindow.document.querySelector('img');
          if (img && !img.complete) {
            img.onload = () => {
              printWindow.focus();
              printWindow.print();
              printWindow.close();
            };
          } else {
            printWindow.focus();
            printWindow.print();
            printWindow.close();
          }
        };
  
    
    };

    // Auto-calculate totals
    function calculateTotals() {
        let subtotal = 0;
        let totalTax = 0;

        document.querySelectorAll('#invoice-items tbody tr').forEach(row => {
            const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
            const price = parseFloat(row.querySelector('.price').value) || 0;
            const tax = parseFloat(row.querySelector('.tax').value) || 0;

            const itemTotal = (quantity * price) + (quantity * price * tax / 100);
            row.querySelector('.total').textContent = itemTotal.toLocaleString("en-GB",
                {
                    style: "currency",
                    currency: "GBP",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
        
            subtotal += quantity * price;
            totalTax += (quantity * price * tax / 100);
        });

        document.getElementById('subtotal').textContent = subtotal.toLocaleString("en-GB",{
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        document.getElementById('total-tax').textContent = totalTax.toLocaleString("en-GB",{
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        document.getElementById('final-amount').textContent = (subtotal + totalTax).toLocaleString("en-GB",{
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Add new item row
    addItemButton.addEventListener('click', () => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" name="service_name[]" required></td>
            <td><input type="text" name="description[]"></td>
            <td><input type="number" name="quantity[]" class="quantity" min="1" value="1" required></td>
            <td><input type="number" name="price_per_unit[]" class="price" step="0.01" required></td>
            <td> <select  name="tax[]" class="tax">
                <option value="0">Not Taxed</option>
                <option value="20">Taxed</option>
            </select></td>
            <td class="total">0.00</td>
            <td><button type="button" class="remove-item">Remove</button></td>`;

        itemsTable.appendChild(newRow);
        calculateTotals();
    });

 

    // Remove item row
    itemsTable.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-item')) {
            e.target.closest('tr').remove();
            calculateTotals();
        }
    });

    // Recalculate on input change
    itemsTable.addEventListener('input', calculateTotals);

    calculateTotals();
// });



const email_messages = document.getElementById('email-messages')
document.getElementById("email-form").addEventListener("submit",async (e)=>{
    e.preventDefault();
   
    const invoice = document.getElementById("re-email-invoice").value.trim();
    const email = document.getElementById("customer_email").value.trim();
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const response = await fetch(`/invoicing/email-invoice/${email}/${invoice}/`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    });
    const data = await response.json();

    
    if (response.ok) {
    
        email_messages.textContent = "Email sent successfully. The customer  will recieve the email in a while.";
        } else {
     
        email_messages.textContent = `Email not sent. Error occured.${data.error} `
    }
});







//  Function to save invoice and print Invoice after saving it 
let clickedButton = null;
const saveAndPrintBtn = document.getElementById('print-invoice');
const invoiceForm = document.getElementById('invoice-form');

saveAndPrintBtn.addEventListener('click', function() {
    clickedButton = 'saveAndPrint';
  });




invoiceForm.addEventListener('submit', async function(e) {
  
    const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    if (clickedButton === 'saveAndPrint') {
        e.preventDefault();  // stop normal form submission
        const formData = new FormData(invoiceForm);
        try {
            const response = await fetch("/invoicing/create-invoice-api/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData
            });
            const data = await response.json();
            
            if (response.ok) {
                alert(data.message);  // success message from backend

                //  call the print function 
                printInvoice()
                invoiceForm.reset()   
                window.location.reload()
                      
            } else {
                alert(data.error || 'An error occurred.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong.');
            }
        }
    });





