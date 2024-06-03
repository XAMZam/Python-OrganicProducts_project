var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

// Add this function to retrieve the CSRF token
function getCSRFToken() {
    var csrfToken = null;
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            csrfToken = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return csrfToken;
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated');

    if (action == 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }
    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }
    console.log('cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';
    var csrftoken = getCSRFToken(); // Retrieve CSRF token here

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response:', data);
            // Update cart UI based on the response
            updateCartUI(data);
        })
        .catch(error => {
            console.error('Error updating cart:', error);
            // Optionally, you can display an error message to the user
        });
}

function updateCartUI(data) {
    // Update cart UI based on the response data
    // For example, you can update the cart total, item count, etc.
    // You can also show a success message or handle other UI updates
}
