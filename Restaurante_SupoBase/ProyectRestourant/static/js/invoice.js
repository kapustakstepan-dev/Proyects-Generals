// ¡Hola! Aquí tienes la lógica para generar las facturas de RetroBite. Todo está limpio y listo para que los clientes reciban sus recibos.
class InvoiceGenerator {
    constructor() {
        this.createInvoiceDOM();
        this.bindEvents();
    }

    createInvoiceDOM() {
        const overlay = document.createElement('div');
        overlay.classList.add('invoice-overlay');
        overlay.id = 'invoice-modal';
        overlay.style.display = 'none';

        overlay.innerHTML = `
            <div class="invoice-modal">
                <div class="invoice-header">
                    <h2 data-i18n="invoice_title" style="font-family: var(--font-heading); color: var(--primary-color);">RetroBite Receipt</h2>
                    <p id="inv-date"></p>
                    <p>Order #<span id="inv-id"></span></p>
                </div>
                <div class="invoice-details" id="inv-items">

                </div>
                <div class="invoice-total">
                    <span data-i18n="total">Total</span>: $<span id="inv-total"></span>
                </div>
                <div class="invoice-actions">
                    <button class="retro-btn" id="btn-close-invoice" data-i18n="close">Close</button>
                    <button class="retro-btn" style="background-color: var(--secondary-color); border-color: var(--secondary-color);" id="btn-send-invoice" data-i18n="invoice_send">Send to Email</button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);
    }

    bindEvents() {
        document.getElementById('btn-close-invoice').addEventListener('click', () => {
            this.hide();
        });

        document.getElementById('btn-send-invoice').addEventListener('click', () => {
            const emailBody = `Thank you for your order at RetroBite!%0D%0AOrder ID: ${document.getElementById('inv-id').textContent}%0D%0ATotal: $${document.getElementById('inv-total').textContent}`;
            window.location.href = `mailto:user@email.com?subject=RetroBite Invoice&body=${emailBody}`;
        });
    }

    show(orderData) {
        document.getElementById('inv-date').textContent = new Date().toLocaleString();
        document.getElementById('inv-id').textContent = Math.floor(Math.random() * 1000000);

        const itemsContainer = document.getElementById('inv-items');
        itemsContainer.innerHTML = '';

        let total = 0;
        orderData.items.forEach(item => {
            total += item.price;
            itemsContainer.innerHTML += `
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>${item.name} (x${item.quantity})</span>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `;
        });

        document.getElementById('inv-total').textContent = total.toFixed(2);

        document.getElementById('invoice-modal').classList.add('active');
        if (window.translator) window.translator.updateDOM();
    }

    hide() {
        document.getElementById('invoice-modal').classList.remove('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.invoiceSystem = new InvoiceGenerator();
});
