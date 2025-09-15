document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

$(document).ready(function() {
    $('#filterButton').click(function() {
        var category_id = $('#category_id').val();
        var status = $('#status').val();
        var payment_name = $('#payment_name').val();
        var payment_amount = $('#payment_amount').val();
        var payment_date = $('#payment_date').val();

        $.ajax({
            url: filterPaymentsUrl,
            type: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            data: {
                'category_id': category_id,
                'status': status,
                'payment_name': payment_name,
                'payment_amount': payment_amount,
                'payment_date': payment_date
            },
            success: function(response) {
                var html = '';
                response.forEach(function(payment) {
                    html += `<div class="payment-item">
                        <h3>${payment.name}</h3>
                        <p>Amount: ${payment.amount}</p>
                        <p>Category: ${payment.category}</p>
                        <p>Status: ${payment.status}</p>
                        <p>Type: ${payment.payment_type}</p>
                        <p>Bank Account: ${payment.related_bank_account || 'None'}</p>
                        <a href="/payment/${payment.id}/">View Details</a>
                    </div>`;
                });
                $('#paymentList').html(html);
            },
            error: function(response) {
                console.log('Error:', response);
            }
        });
    });
});