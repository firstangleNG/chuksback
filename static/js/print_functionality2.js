// Ticket number
const ticket_no = document.getElementById("ticket-no").textContent;
const invoice_no = document.getElementById("invoice").value;
const repair_status = document.getElementById("statusSelect").value;
//   Get customer detail from the page
const customer_name = document.getElementById("customer_name").textContent;
const customer_email = document.getElementById("customer_email").textContent;
const customer_phone = document.getElementById("customer_phone").textContent;
const customer_address = document.getElementById("customer_address").value.trim()
const created_at = document.getElementById("created_at").textContent;

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


 // Print Invoice Functionality
function printSection(){

    // Get all Descriptions 
    const descriptions = document.querySelectorAll('#description_list li');
        let description_text = '<ul>';
    descriptions.forEach((desc) => {
      description_text += `<li>${desc.textContent}</li>`;
    });
    description_text += '</ul>';


    // Get number of items texed

    const tax_elements = document.querySelectorAll('select[name="tax"]');
    let number_of_taxed_items_counter = 0;
    tax_elements.forEach(element=>{
       if(parseInt(element.value) > 0 ){
        number_of_taxed_items_counter ++;
       }
    })

// Form the tax statement 
let tax_statement = ""
number_of_taxed_items_counter > 0?  tax_statement = `( 20% tax inclusive on ${number_of_taxed_items_counter} item(s) )` : tax_statement = "( 0% tax inclusive )"


  
// Payment data 
let final_amount =  parseFloat(document.getElementById("final-amount").textContent.replace(/[^\d.]/g, "")) || 0.00; 
let  taxable_total = parseFloat(document.getElementById("subtotal").textContent.replace(/[^\d.]/g, "")) || 0.00; 
let total_tax = parseFloat(document.getElementById("total-tax").textContent.replace(/[^\d.]/g, "")) || 0.00;
 let amount_due = parseFloat(document.getElementById("amount_due").textContent.replace(/[^\d.]/g, "")) || 0.00;




const currentTime = new Date().toLocaleTimeString();

const rows = document.querySelectorAll('.invoice-tr');


let itemsHtml = '';

rows.forEach((row,index) => {
    const serviceName = row.querySelector('input[name="service_name"]')?.value || 'N/A';
    const description = row.querySelector('input[name="description"]')?.value || 'N/A';
    const quantity = row.querySelector('input[name="quantity"]')?.value || '0';
    const price = row.querySelector('input[name="price_per_unit"]')?.value || '0.00';
    const tax = row.querySelector('input[name="tax"]')?.value || '0.00';
    const total = row.querySelector('.total')?.textContent || '0.00';

    itemsHtml += `
        <tr>
            <td><strong>${index + 1}</td>
            <td>${serviceName}</strong><br>${description}</td>
            <td>${quantity}</td>
            <td>${price}</td>
            <td>${tax}</td>
            <td>${total}</td>
        </tr>`;
});

      const printContent =  `
      <!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <title>Repair Ticket</title>
    <style>
        body { font-family: Arial, sans-serif; font-size: 12px; line-height: 1.3; }

    .invoice-header {
      display: flex;
      border-bottom: 1px solid #000000; 
    }

    .invoice-header img {
  width: 100px;
  height: 30px;
}

        .disclaimer {
          width: 60%;
            font-style: italic;
            color: #666;
            margin-top: 10px;
            font-size: 8px;
        }
        .info-section { display: flex; justify-content: space-between; margin-bottom: 15px; }
        .customer-info, .ticket-info { width: 28%; }
        .section-title { background-color: #f2f2f2; padding: 4px; font-weight: bold; margin-bottom: 8px; font-size: 11px; }
        .device-info{margin-bottom: 10px;}

        table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 11px; }
        th, td { border: 1px solid #ddd; padding: 5px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total-row { font-weight: bold; }
        .footer { margin-top: 8px; padding-top: 8px; border-top: 1px solid #333; font-size: 8px; }
        .signature-line { margin-top: 30px; border-top: 1px solid #000; width: 200px; }
        .status-completed { 
            padding: 2px 6px; 
            border-radius: 3px; 
            font-weight: bold; 
            color: white;
            font-size: 10px;
            background-color: #27ae60;
        }
        .totals {
            text-align: right;
            margin-bottom: 15px;
            font-size: 10px;
            padding-right: 5px;
        }
        .notes { margin-bottom: 10px; }
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
      @media (max-width: 768px) {
        .disclaimer{
          width: 100%;
          
        }
        .info-section{
          width: 100%;
          display: flex;
          justify-content: space-between;
        }
      }

      @media (max-width: 480px) {
        .disclaimer{
          width: 100%;

        }
        .info-section{
          width: 100%;
          display: flex;
          justify-content: space-between;
        }
        .info-section-items{
          width: 50%;
          flex: 1;
        }
      }

    </style>
</head>
<body>
    <div class="invoice-header">
        <img src="https://chukticketingsystem.com/static/images/computer_hub_new.jpeg" alt="Logo">
            <p style="margin-left: 30px;">Repair Ticket <br>
            <span class="small-text">info@computerhubuk.com</span>
            </p>    
             <strong>Contact:</strong> info@computerhubuk.com | +441793354694/07501241137</p>      
    </div>

    <div class="disclaimer">
        <p><strong>*Disclaimer*</strong><br>
          <strong>When replacing faulty motherboard of your computer or laptop, please be aware that if BitLocker encryption is enabled on your device, you may need to know your BitLocker recovery key. We are not responsible if you do not have or cannot provide your BitLocker recovery key.<br>
          Thank you for your understanding.
          </p>
        </strong>
      </div>


      <div class="info-section">
        <div class="customer-info info-section-items">
            <div class="section-title">Customer Information</div>
            <p><strong>Name:</strong>${customer_name}</p>
            <p><strong>Email:</strong>${customer_email}</p>
            <p><strong>Phone:</strong> ${customer_phone}</p>
            <p><strong>Address:</strong>${customer_address}</p>
        </div>
        
        <div class="ticket-info info-section-items">
            <div class="section-title">Ticket Information</div>
            <p><strong>Ticket #:</strong>${ticket_no}</p>
            <p><strong>Date Received:</strong>${created_at}</p>
            <p><strong>Repair Status:</strong> <span class="status-completed">${repair_status}</span></p>
            <p><strong>Generated On:</strong> ${currentTime}</p>
            <p><strong>Due Date:</strong>${due_date}</p>
            
        </div>
      </div>
          <div class="device-info">
          <div class="section-title">Device Information</div> 
          <p><strong>Brand:</strong> ${brand} <strong>Model:</strong>v <strong>IMEI/Serial Number:</strong> ${imei_serial_no}<br/> <strong>Issue Description:</strong> ${problem}</p>
      </div>

    
       <div  id="description_parent">
        <div class="section-title">Descriptions</div>
            ${description_text}
    </div>
    <p>VAT Number : 353 9011 12</p>
    <div class="repair-items">
        <div class="section-title">Repair Ticket Invoice</div>
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
          <p><strong>Total: ${(taxable_total).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>${tax_statement}:${(total_tax).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>Grand Total: ${(final_amount).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>Amount Paid:${(final_amount - amount_due).toLocaleString('en-GB',{
            style:"currency",
            currency:"GBP",
            minimumFractionDigits:2,
            maximumFractionDigits:2
          })}</strong></p>
          <p><strong>Amount Due:${(amount_due).toLocaleString('en-GB',{
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
        </body>
        ` //End of interpolation string symbol
    

             
   
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
}




