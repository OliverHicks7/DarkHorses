// API calls to Azure Functions

// PLACE HOLDER TO BE REPLACED WITH YOUR AZURE FUNCTION URL
const baseApiUrl = 'https://<your-function-app>.azurewebsites.net/api'; // Replace with BASE URL

async function fetchItemsFromFunction1() {
    const url = `${baseApiUrl}/HttpTrigger1`;
    return fetchData(url);
}

async function fetchItems(apiUrl) {
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

export { fetchItemsFromFunction1 };
