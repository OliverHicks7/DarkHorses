// API calls to Azure Functions

// PLACE HOLDER TO BE REPLACED WITH YOUR AZURE FUNCTION URL
const baseApiUrl = 'http://localhost:7071/api'; // Replace with BASE URL

async function getProducts() {
    const url = `${baseApiUrl}/getProducts`;
    return fetchData(url);
}

async function fetchData(apiUrl) {
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

export { getProducts };
