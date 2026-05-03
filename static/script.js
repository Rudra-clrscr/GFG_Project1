document.addEventListener('DOMContentLoaded', () => {
  // --- Cart Management ---
  let cart = JSON.parse(localStorage.getItem('aurelia_cart')) || [];
  
  const updateCartUI = () => {
    const cartCountStr = document.querySelector('.cart-count');
    if (cartCountStr) cartCountStr.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    const cartItemsContainer = document.querySelector('.cart-items');
    if (cartItemsContainer) {
      cartItemsContainer.innerHTML = '';
      let total = 0;
      cart.forEach(item => {
        total += item.price * item.quantity;
        cartItemsContainer.innerHTML += `
          <div class="cart-item">
            <img src="${item.image_url}" alt="${item.name}">
            <div class="cart-item-details">
              <div class="cart-item-title">${item.name} (x${item.quantity})</div>
              <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
            </div>
            <button class="remove-item" data-id="${item.id}" style="background:none;border:none;color:#fff;cursor:pointer;">&times;</button>
          </div>
        `;
      });
      
      const cartTotalStr = document.querySelector('.cart-total');
      if (cartTotalStr) cartTotalStr.innerHTML = `<span>Total</span> <span>$${total.toFixed(2)}</span>`;
      
      // Add remove event listeners
      document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = parseInt(e.target.getAttribute('data-id'));
          cart = cart.filter(item => item.id !== id);
          localStorage.setItem('aurelia_cart', JSON.stringify(cart));
          updateCartUI();
        });
      });
    }
  };
  
  updateCartUI();
  
  // Cart Drawer Toggle
  const cartIcon = document.querySelector('.cart-icon');
  const cartDrawer = document.querySelector('.cart-drawer');
  const closeCartBtn = document.querySelector('.close-cart');
  
  if (cartIcon) {
    cartIcon.addEventListener('click', () => {
      cartDrawer.classList.add('open');
    });
  }
  
  if (closeCartBtn) {
    closeCartBtn.addEventListener('click', () => {
      cartDrawer.classList.remove('open');
    });
  }

  // --- Scroll Animations (Intersection Observer) ---
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  // --- Header Scroll Effect Removed ---
  // (Header is now position: absolute, so it scrolls with the page)

  // --- AI Concierge Chat ---
  const chatFab = document.querySelector('.chat-fab');
  const chatWindow = document.querySelector('.chat-window');
  
  if (chatFab && chatWindow) {
    chatFab.addEventListener('click', () => {
      chatWindow.classList.toggle('open');
    });
  }

  const sendBtn = document.getElementById('chat-send-btn');
  const chatInput = document.getElementById('chat-input-field');
  const chatMessages = document.querySelector('.chat-messages');

  const appendMessage = (text, sender) => {
    if (!chatMessages) return;
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  if (sendBtn && chatInput) {
    sendBtn.addEventListener('click', async () => {
      const msg = chatInput.value.trim();
      if (!msg) return;
      
      appendMessage(msg, 'user');
      chatInput.value = '';
      
      try {
        // Assume API is on same origin, or use relative path since we mount static
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const data = await response.json();
        appendMessage(data.response, 'bot');
      } catch (err) {
        appendMessage("Connection error. Please try again.", 'bot');
      }
    });
    
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendBtn.click();
    });
  }

  // --- Bind Add to Cart buttons for hardcoded products ---
  const addToCartButtons = document.querySelectorAll('.add-to-cart');
  if (addToCartButtons.length > 0) {
    addToCartButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const item = {
          id: parseInt(e.target.dataset.id),
          name: e.target.dataset.name,
          price: parseFloat(e.target.dataset.price),
          image_url: e.target.dataset.image,
          quantity: 1
        };
        
        const existingItem = cart.find(i => i.id === item.id);
        if (existingItem) {
          existingItem.quantity += 1;
        } else {
          cart.push(item);
        }
        
        localStorage.setItem('aurelia_cart', JSON.stringify(cart));
        updateCartUI();
        cartDrawer.classList.add('open');
      });
    });
  }

  // --- Contact Form Submit ---
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const inquiry = document.getElementById('inquiry').value;
      
      try {
        const response = await fetch('/contact-submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, inquiry })
        });
        const data = await response.json();
        alert(data.message);
        contactForm.reset();
      } catch (err) {
        alert('Error submitting the form.');
      }
    });
  }

  // --- Checkout Page ---
  const checkoutItems = document.getElementById('checkout-items');
  const checkoutTotal = document.getElementById('checkout-total');
  const checkoutForm = document.getElementById('checkout-form');
  
  if (checkoutItems && checkoutTotal) {
    let total = 0;
    if (cart.length === 0) {
      checkoutItems.innerHTML = '<p>Your cart is empty.</p>';
    } else {
      cart.forEach(item => {
        total += item.price * item.quantity;
        checkoutItems.innerHTML += `
          <div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
            <span>${item.name} (x${item.quantity})</span>
            <span>$${(item.price * item.quantity).toFixed(2)}</span>
          </div>
        `;
      });
    }
    checkoutTotal.innerHTML = `<strong>Total: $${total.toFixed(2)}</strong>`;
  }
  
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (cart.length === 0) {
        alert("Your cart is empty.");
        return;
      }
      
      const submitBtn = checkoutForm.querySelector('button');
      submitBtn.textContent = "Processing...";
      submitBtn.disabled = true;
      
      let total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      
      try {
        const response = await fetch('/process-payment', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: cart, total: total })
        });
        const data = await response.json();
        alert(data.message);
        localStorage.removeItem('aurelia_cart');
        window.location.href = 'index.html';
      } catch (err) {
        alert("Payment error.");
        submitBtn.textContent = "Place Order";
        submitBtn.disabled = false;
      }
    });
  }
});
