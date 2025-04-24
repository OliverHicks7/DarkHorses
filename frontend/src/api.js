// API calls to Azure Functions

// PLACE HOLDER TO BE REPLACED WITH YOUR AZURE FUNCTION URL
const apiUrl = 'https://<your-function-app>.azurewebsites.net/api/<function-name>'; // Replace with your Azure Function URL

async function fetchItems() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const items = await response.json(); // Assuming the Azure Function returns a JSON array
        return items;
    } catch (error) {
        console.error('Error fetching items:', error);
        return [];
    }
}

export { fetchItems };
