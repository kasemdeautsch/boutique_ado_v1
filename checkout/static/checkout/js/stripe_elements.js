/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/


var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');
console.log('Found....')

//document.getElementById('id_full_name').style.innerHtml='cccccccc';

//handle realtime validation errors on the card

card.addEventListener('change', function(event) {
    //console.log('clicked....');
    var errorDiv = document.getElementById('card-errors');
    //errorDiv.innerText='Hello'
    //errorDiv.innerText=This.innerText
    if (event.error) {
        var html =
            `<span class="icon" role = "alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
            `
        $(errorDiv).html(html)
    } else {
        errorDiv.textContent=''
    }

})

// handle form submit

var form = document.getElementById('payment-form')

form.addEventListener('submit', function(event){
    event.preventDefault();
    console.log('submit prevented!!');
    card.update({'disabled':true});
    $('#submit-button').attr('disabled',true);
    //$('#payment-form').fadeToggle(100);
    $('#payment-form').fadeToggle(100);
    //$('#loading-overlay').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
             var errorDiv = document.getElementById('card-errors');
             var html = `
                <span class="icon" role = "alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({'disabled':false});
            $('#submit-button').attr('disabled',false);
            console.log('Not done!!');
        } else {
            if (result.paymentIntent.status==='succeeded') {
                console.log('Succedded!!')
                form.submit()
            }
        }
    })
})

