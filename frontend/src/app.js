// Main JavaScript file

import { fetchItems } from './api.js';

async function renderItems() {
    const itemList = document.getElementById('item-list'); // Ensure this matches the ID in your HTML
    const items = await fetchItems();

    if (items.length === 0) {
        itemList.innerHTML = '<li>No items found</li>';
        return;
    }

    // Clear existing items
    itemList.innerHTML = '';

    // Render each item as a list element
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item; // Assuming each item is a string
        itemList.appendChild(li);
    });
}

// Call the function to render items on page load
document.addEventListener('DOMContentLoaded', renderItems);