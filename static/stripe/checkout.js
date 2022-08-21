// const stripe = Stripe('pk_test_51KplMlHDbaGlDWjrp82Da0ecOIeQ93TWSzSVf8ntQryeGR6NfST4tTRxD9990KLPnoBNs0gA9KekUk4pMc2SBlY100BddH3hZ3');
// The items the customer wants to buy
const items = [{id: "xl-tshirt"}];
let elements;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

initialize();
// checkStatus();

// document
//     .querySelector("#payment-form")
//     .addEventListener("submit", handleSubmit);

// Fetches a payment intent and captures the client secret

async function paymentIntentSecret() {
    let response = await fetch("/api/v1/stripe/create-payment-intent-secret/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            paymentMethodType: 'card',
            currency: 'usd',
        }),
    });
    // let {clientSecret} = await response.json();
    return await response.json();
}

async function createOrder(source, email, mobile_number) {
    let response = await fetch("/api/v1/orders/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            payment_source: source,
            email: email,
            mobile_number: mobile_number,
        }),
    });
    // let {clientSecret} = await response.json();
    return await response.json();
}

async function completeOrderPayment(source, email, mobile_number) {
    return await fetch("/api/v1/checkouts/complete-payment/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            payment_source: source,
            email: email,
            mobile_number: mobile_number,
        }),
    });
}

async function completeSubscription(subscription_id, payment_intent_id, payment_method_id) {
    return await fetch("/api/v1/stripe-payment/complete-subscription/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            subscription_id: subscription_id,
            payment_intent_id: payment_intent_id,
            payment_method_id: payment_method_id,
        }),
    });
}


async function initialize() {
    let appearance = {
        theme: 'flat',
    };

    // elements = stripe.elements({appearance, client_secret});
    elements = stripe.elements();
    // const elements = stripe.elements();

    let paymentRequest = stripe.paymentRequest({
        country: 'US',
        currency: 'usd',
        total: {
            label: 'Cart',
            amount: Math.round(cart_total_price),
        },
        requestPayerName: true,
        requestPayerEmail: true,
    });
    let prButton = elements.create('paymentRequestButton', {
        paymentRequest: paymentRequest,
    });
    // Check the availability of the Payment Request API first.
    paymentRequest.canMakePayment().then(function (result) {
        if (result) {
            prButton.mount('#payment-request-button');
        } else {
            console.log('google pay unavailable')
            document.getElementById('payment-request-button').style.display = 'none';
        }
    });
    paymentRequest.on('paymentmethod', async function (event) {
        console.log(event);
        let payer_email = 'test@test.com';
        let payer_name = 'test';
        let payer_phone = '';
        // let {client_secret} = await paymentIntentSecret();
        // console.log('client_secret', client_secret)
        console.log('payment method: ', event.paymentMethod)
        console.log('payment method id: ', event.paymentMethod.id)
        let payment_method_id = event.paymentMethod.id;
        let {
            subscription_id,
            payment_intent_id,
            payment_intent_client_secret
        } = await create_subscription(payment_method_id)
        stripe.confirmCardPayment(
            payment_intent_client_secret,
            {payment_method: event.paymentMethod.id},
            {handleActions: false}
        ).then(async function (confirmResult) {
            console.log(confirmResult);

            if (confirmResult.error) {
                console.log(confirmResult.error.message)
                event.complete('fail');
            }
            console.log(confirmResult.paymentIntent.status);

            if (confirmResult.paymentIntent.status === "requires_capture") {
                try {
                    let response = await completeSubscription(
                        subscription_id, confirmResult.paymentIntent.id, payment_method_id
                    );
                    console.log(await response.json())
                    if (response.status === 200 || response.status === 201) {
                        console.log('success');

                        event.complete('success');
                        window.location.reload();
                    } else {
                        console.log('failed');
                        event.complete('fail');
                    }

                } catch (err) {
                    console.log('err', err);
                    event.complete('fail');
                }
            } else if (confirmResult.paymentIntent.status === "succeeded") {
                console.log('success');

                event.complete('success');
            }

        })
    })


    // paymentRequest.on('source', async function (event) {
    //     // event.paymentMethod is available
    //     console.log(event);
    //     let source = event.source;
    //     // let order = createOrder(source.id, event.payerEmail, '');
    //     // if (order) {
    //     //     event.complete('success')
    //     // } else {
    //     //     event.fail('failed')
    //     // }
    //     // let intent = await paymentIntentSecret();
    //     // console.log(intent)
    // });

    // paymentRequest.on('token', async (e) => {
    //     console.log(e);
    //     let response = await fetch('/api/v1/stripe/charge-from-token/', {
    //         method: 'POST',
    //         headers: {"Content-Type": "application/json"},
    //         body: JSON.stringify({
    //             token: e.token.id
    //         })
    //     });
    //     let result = await response.json();
    //     console.log(result);
    //     if (result) {
    //         await e.complete('success')
    //     }
    //
    // });

    // paymentRequest.on('paymentMethod', async (e) => {
    //     console.log(e);
    //     let response = await fetch("/api/v1/stripe/create-payment-intent-test/", {
    //         method: "POST",
    //         headers: {"Content-Type": "application/json"},
    //         body: JSON.stringify({
    //             paymentMethodType: 'card',
    //             currency: 'usd',
    //         }),
    //     });
    //     let {clientSecret} = await response.json();
    //     let {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
    //         payment_method: e.paymentMethod.id,
    //     }, {handleActions: false});
    //     if (error) {
    //         e.complete('fail!')
    //     }
    //     e.complete('success...');
    //     console.log(paymentIntent)
    //     if (paymentIntent.status === 'requires_actions') {
    //         console.log('action required.')
    //     }
    // })

    // const paymentElement = elements.create("payment");
    // paymentElement.mount("#payment-element");
}

// async function handleSubmit(e) {
//     e.preventDefault();
//     setLoading(true);
//
//     const {error} = await stripe.confirmPayment({
//         elements,
//         confirmParams: {
//             // Make sure to change this to your payment completion page
//             return_url: "http://localhost:4242/checkout.html",
//         },
//     });
//
//     // This point will only be reached if there is an immediate error when
//     // confirming the payment. Otherwise, your customer will be redirected to
//     // your `return_url`. For some payment methods like iDEAL, your customer will
//     // be redirected to an intermediate site first to authorize the payment, then
//     // redirected to the `return_url`.
//     if (error.type === "card_error" || error.type === "validation_error") {
//         showMessage(error.message);
//     } else {
//         showMessage("An unexpected error occurred.");
//     }
//
//     setLoading(false);
// }
//
// // Fetches the payment intent status after payment submission
// async function checkStatus() {
//     const clientSecret = new URLSearchParams(window.location.search).get(
//         "payment_intent_client_secret"
//     );
//
//     if (!clientSecret) {
//         return;
//     }
//
//     const {paymentIntent} = await stripe.retrievePaymentIntent(clientSecret);
//
//     switch (paymentIntent.status) {
//         case "succeeded":
//             showMessage("Payment succeeded!");
//             break;
//         case "processing":
//             showMessage("Your payment is processing.");
//             break;
//         case "requires_payment_method":
//             showMessage("Your payment was not successful, please try again.");
//             break;
//         default:
//             showMessage("Something went wrong.");
//             break;
//     }
// }
//
// // ------- UI helpers -------
//
// function showMessage(messageText) {
//     const messageContainer = document.querySelector("#payment-message");
//
//     messageContainer.classList.remove("hidden");
//     messageContainer.textContent = messageText;
//
//     setTimeout(function () {
//         messageContainer.classList.add("hidden");
//         messageText.textContent = "";
//     }, 4000);
// }
//
// // Show a spinner on payment submission
// function setLoading(isLoading) {
//     if (isLoading) {
//         // Disable the button and show a spinner
//         document.querySelector("#submit").disabled = true;
//         document.querySelector("#spinner").classList.remove("hidden");
//         document.querySelector("#button-text").classList.add("hidden");
//     } else {
//         document.querySelector("#submit").disabled = false;
//         document.querySelector("#spinner").classList.add("hidden");
//         document.querySelector("#button-text").classList.remove("hidden");
//     }
// }
//
// // Fetches the payment intent status after payment submission
//
// async function checkStatus() {
//     const clientSecret = new URLSearchParams(window.location.search).get(
//         "payment_intent_client_secret"
//     );
//
//     if (!clientSecret) {
//         return;
//     }
//
//     const {paymentIntent} = await stripe.retrievePaymentIntent(clientSecret);
//
//     switch (paymentIntent.status) {
//         case "succeeded":
//             showMessage("Payment succeeded!");
//             break;
//         case "processing":
//             showMessage("Your payment is processing.");
//             break;
//         case "requires_payment_method":
//             showMessage("Your payment was not successful, please try again.");
//             break;
//         default:
//             showMessage("Something went wrong.");
//             break;
//     }
// }

async function create_subscription(payment_method_id) {
    let response = await fetch("/api/v1/stripe-payment/create-subscription/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            payment_method_id: payment_method_id,
        }),
    });
    return await response.json();
}