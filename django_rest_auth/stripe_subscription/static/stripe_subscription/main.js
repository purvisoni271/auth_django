//document
//  .getElementById("checkout")
//  .addEventListener("click", function(evt) {
//    createCheckoutSession(PriceId).then(function(data) {
//      // Call Stripe.js method to redirect to the new Checkout page
//      stripe
//        .redirectToCheckout({
//          sessionId: data.sessionId
//        })
//        .then(handleResult);
//    });
// });
let stripe;
fetch("/payment/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  stripe = Stripe(data.publicKey);
  })

