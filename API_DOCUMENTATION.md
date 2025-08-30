# Django Backend API Documentation for Next.js Frontend

Based on the Django backend codebase analysis, here are all the available API endpoints you can use to connect your Next.js frontend:

## Base URL
```
http://127.0.0.1:8000
```

## Authentication APIs

### User Management
| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/` | Login user | `{email, password}` |
| `POST` | `/logout/` | Logout user | - |
| `POST` | `/create-user/` | Create new user | `{full_name, email, phone_number, role, address, profile_picture}` |
| `GET` | `/accounts/verify-email/?token={token}` | Verify email with token | - |
| `POST` | `/new-password/{user_id}/` | Set new password | `{password, confirm_password}` |
| `POST` | `/verify-password-reset-otp/{user_id}/` | Verify OTP for password reset | `{otp}` |
| `POST` | `/forgot-password-email/` | Request password reset | `{email}` |
| `POST` | `/forgot-password/set-new/{user_id}/` | Set new forgot password | `{password, confirm_password}` |

## Customer APIs

### Customer Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/api/customers/create/` | Create new customer | `{first_name, last_name, email, phone, company, address}` | `{message, customer_id}` |
| `GET` | `/api/customers/search/?q={query}` | Search customers | - | `[{customer_data}]` |
| `GET` | `/api/customers/details/{customer_id}/` | Get customer details | - | `{customer_info}` |
| `PATCH` | `/api/customers/update/` | Update customer | `{id, first_name, last_name, email, phone}` | `{customer_info}` |

## Repair Ticket APIs

### Ticket Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/repairs/tickets/{user_id}/` | Get user tickets | - | HTML/Tickets list |
| `GET` | `/repairs/add/` | Add ticket form | - | HTML |
| `GET` | `/repairs/properties/` | Get all properties | - | `{properties}` |
| `POST` | `/repairs/tickets/create/` | Create repair ticket | `{ticket_data}` | `{ticket}` |
| `PATCH` | `/repairs/ticket/{ticket_id}/update/` | Update ticket status | `{status}` | `{success, message, data}` |
| `POST` | `/repairs/ticket/{ticket_id}/update/detail/` | Update ticket details | `{ticket_details}` | - |
| `GET` | `/repairs/ticket-detail/{ticket_id}/` | Get ticket details | - | `{ticket_data}` |
| `POST` | `/repairs/set-technician/` | Assign technician | `{ticket_id, technician_id}` | `{message, ticket}` |
| `GET` | `/repairs/note/{ticket_id}/` | Get ticket notes | - | `{notes}` |
| `POST` | `/repairs/note/create/{ticket_id}/` | Create ticket note | `{note_data}` | `{note}` |
| `GET` | `/repairs/customer-email/` | Get customer email | - | `{email}` |

### Property Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/repairs/properties/` | List all properties | - | `[{properties}]` |
| `POST` | `/repairs/properties/create/` | Create property | `{imei_serial_no, brand, model, more_detail, customer}` | `{property}` |
| `GET` | `/repairs/properties/{pk}/` | Get property details | - | `{property}` |
| `PUT` | `/repairs/properties/{pk}/update/` | Update property | `{property_data}` | `{property}` |
| `DELETE` | `/repairs/properties/{pk}/delete/` | Delete property | - | `{success}` |

### Payment Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET`/`POST` | `/repairs/payments/` | List/Create payments | `{ticket, payment_type, amount}` | `{payments}` |
| `GET` | `/repairs/payments/amount-due/{ticket_id}/` | Get amount due | - | `{amount_due}` |
| `DELETE` | `/repairs/payments/delete/{payment_id}/` | Delete payment | - | `{success}` |
| `POST` | `/repairs/description/add/` | Add description | `{ticket_id, description}` | `{description}` |

## Inventory APIs

### Inventory Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/inventory/listing/` | Get inventory list | - | HTML/Inventory items |
| `POST` | `/inventory/new-item/` | Add/Update inventory | `{part_name, sku, barcode, category, supplier_name, cost_price, selling_price, quantity_available, low_stock_threshold, reorder_level, location, expiration_date}` | `{message}` |
| `GET` | `/inventory/stock-alerts/` | Get low stock alerts | - | `{low_stock_items}` |
| `GET` | `/inventory/barcode-search/?barcode={barcode}` | Search by barcode | - | `{success, data}` |
| `GET` | `/inventory/manage-inventory/` | Manage inventory page | - | HTML |
| `POST` | `/inventory/add-item/` | Add item | `{part_name, sku, quantity_available, selling_price}` | - |
| `POST` | `/inventory/edit-item/{item_id}` | Edit item | `{item_data}` | - |
| `POST` | `/inventory/delete-item/{item_id}` | Delete item | - | - |
| `GET` | `/inventory/expiring-items/` | Get expiring items | - | `{expiring_items}` |

### Supplier Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/inventory/suppliers/` | List suppliers | - | `{suppliers}` |
| `POST` | `/inventory/suppliers/add/` | Add supplier | `{supplier_data}` | `{supplier}` |
| `POST` | `/inventory/suppliers/edit/{supplier_id}/` | Edit supplier | `{supplier_data}` | `{supplier}` |
| `POST` | `/inventory/suppliers/delete/{supplier_id}/` | Delete supplier | - | `{success}` |

### Sales Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/inventory/sales/` | Get sales transactions | - | `{sales}` |
| `POST` | `/inventory/sales/add/` | Add sale | `{sale_data}` | `{sale}` |

## Invoice APIs

### Invoice Management
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/invoicing/create-invoice/` | Create invoice form | - | HTML |
| `POST` | `/invoicing/create-invoice-api/` | Create invoice via API | `{invoice_data}` | `{invoice}` |
| `GET` | `/invoicing/invoice/list/` | List all invoices | - | HTML/Invoice list |
| `GET` | `/invoicing/invoice/{invoice_id}/` | Get invoice details | - | `{invoice_details}` |
| `GET` | `/invoicing/invoice-items/{invoice_id}/` | Get invoice items | - | `{invoice_items}` |
| `GET` | `/invoicing/invoice-item/{item_id}/` | Get invoice item details | - | `{item}` |
| `PUT` | `/invoicing/invoice-items/{item_id}/update/` | Update invoice item | `{item_data}` | `{item}` |
| `DELETE` | `/invoicing/invoice-items/{item_id}/delete/` | Delete invoice item | - | `{success}` |
| `POST` | `/invoicing/update-payment-method/` | Update payment method | `{invoice_id, payment_method}` | `{success, message}` |
| `POST` | `/invoicing/update-status/` | Update invoice status | `{invoice_id, status}` | `{success, message}` |
| `GET` | `/invoicing/email-invoice/{email}/{invoice}/` | Email invoice | - | `{success}` |
| `GET` | `/invoicing/get-customer-email/` | Get customer email | - | `{email}` |

### Repair Ticket Invoice APIs
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/invoicing/repair-ticket/invoice/` | Create invoice for ticket | `{ticket_id, invoice_data}` | `{invoice}` |
| `PUT` | `/invoicing/repair-ticket_invoice_update/{pk}/` | Update ticket invoice | `{invoice_data}` | `{invoice}` |
| `GET` | `/invoicing/ticket-invoices/{invoice}/` | Get ticket invoices | - | `{invoices}` |
| `DELETE` | `/invoicing/delete/ticket-item/{id}/` | Delete ticket item | - | `{success}` |
| `POST` | `/invoicing/update/ticket-invoice/{invoice}/` | Update ticket invoice | `{invoice_data}` | `{invoice}` |
| `GET` | `/invoicing/settings/` | Get invoice settings | - | `{settings}` |

## Dashboard APIs

### Analytics
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/dashboard/` | Get dashboard data | `{total_revenue, pending_payments, total_tickets, open_tickets, canceled, completed, closed_tickets, low_stock_items}` |

## Common Response Formats

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* response data */ }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "errors": { /* validation errors */ }
}
```

## Authentication Headers
Most endpoints require authentication. Include these headers:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

## Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

## Important Notes

1. **Authentication**: Most endpoints require user authentication. Use Django's session authentication or JWT tokens.

2. **CSRF Protection**: For POST/PUT/PATCH/DELETE requests, include CSRF tokens when using session authentication.

3. **File Uploads**: For endpoints accepting files (like profile pictures), use `multipart/form-data` content type.

4. **Database**: The backend uses PostgreSQL with UUID primary keys for most models.

5. **Pagination**: List endpoints may require pagination parameters.

6. **Search**: Customer search uses PostgreSQL full-text search.

7. **Permissions**: Different endpoints may require different user roles (admin, technician, etc.).

## Environment Variables Needed
```env
DJANGO_ENV=local
SECRET_KEY=your_secret_key
DB_NAME=chukticketingsystem_dev
DB_USER=postgres
DB_PASSWORD=godsp
DB_HOST=localhost
DB_PORT=5432
```

This comprehensive API documentation should help you integrate your Next.js frontend with the Django backend effectively.
