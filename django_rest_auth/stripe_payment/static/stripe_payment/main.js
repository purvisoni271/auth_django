console.log("Sanity check!");
let stripe;
fetch("/payment/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  stripe = Stripe(data.publicKey);
  })

  // new
  // Event handler
  var create_checkout = function(id){
    // Get Checkout Session ID
    fetch("create-checkout-session/" + id + "/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  };

 var createCheckoutSession = function(priceId) {
  return fetch("create-subscription-session/"+priceId+"/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      priceId: priceId
    })
  }).then(function(result) {
    var data = result.json()
    Promise.resolve(data).then(function(data){
        console.log(data.sessionId)
        return stripe.redirectToCheckout({
          sessionId: data.sessionId
        })
        .then(handleResult);
    })
    console.log(data.result)
    return data;
  });
};