// Main JavaScript file

import { getProducts } from './api.js';

async function renderItems() {
    const itemList = document.getElementById('item-list'); // Ensure this matches the ID in your HTML
    const items = await getProducts();

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


// Example array of blog posts
const blogPosts = [
    { title: "Blog Post 1", content: "This is the content of blog post 1." },
    { title: "Blog Post 2", content: "This is the content of blog post 2." },
    { title: "Blog Post 3", content: "This is the content of blog post 3." }
];

// Function to render blog posts dynamically
function renderBlogPosts() {
    const itemList = document.getElementById("item-list");

    // Clear existing items
    itemList.innerHTML = "";

    // Add each blog post to the list
    blogPosts.forEach(post => {
        // Create the blog post container
        const li = document.createElement("li");
        li.className = "mb-4 p-3 border rounded bg-light";

        // Add the blog post title
        const title = document.createElement("h3");
        title.textContent = post.title;
        title.className = "mb-2";

        // Add the blog post content
        const content = document.createElement("p");
        content.textContent = post.content;
        content.className = "mb-3";

        // Add thumbs up and thumbs down buttons
        const thumbsUpButton = document.createElement("button");
        thumbsUpButton.textContent = "👍 Thumbs Up";
        thumbsUpButton.className = "btn btn-success me-2";
        thumbsUpButton.addEventListener("click", () => {
            alert(`You liked "${post.title}"`);
        });

        const thumbsDownButton = document.createElement("button");
        thumbsDownButton.textContent = "👎 Thumbs Down";
        thumbsDownButton.className = "btn btn-danger me-2";
        thumbsDownButton.addEventListener("click", () => {
            alert(`You disliked "${post.title}"`);
        });

        // Add a comments section
        const commentInput = document.createElement("textarea");
        commentInput.className = "form-control mt-3";
        commentInput.placeholder = "Write a comment...";
        commentInput.rows = 2;

        const commentButton = document.createElement("button");
        commentButton.textContent = "Submit Comment";
        commentButton.className = "btn btn-primary mt-2";
        commentButton.addEventListener("click", () => {
            alert(`Comment submitted for "${post.title}": ${commentInput.value}`);
            commentInput.value = ""; // Clear the input after submission
        });

        // Append all elements to the blog post container
        li.appendChild(title);
        li.appendChild(content);
        li.appendChild(thumbsUpButton);
        li.appendChild(thumbsDownButton);
        li.appendChild(commentInput);
        li.appendChild(commentButton);

        // Append the blog post container to the list
        itemList.appendChild(li);
    });
}

// Call the function to render blog posts on page load
document.addEventListener("DOMContentLoaded", renderBlogPosts);