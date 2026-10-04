const API_URL = "https://black-talons-floorball-1.onrender.com";

// Fetch all players
async function fetchPlayers() {
    try {
        const response = await fetch(`${API_URL}/players/`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching players:", error);
        return [];
    }
}

// Fetch all upcoming/past matches
async function fetchMatches() {
    try {
        const response = await fetch(`${API_URL}/matches/`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching matches:", error);
        return [];
    }
}

// Fetch news articles
async function fetchNews() {
    try {
        const response = await fetch(`${API_URL}/news/`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching news:", error);
        return [];
    }
}

// Submit contact / join form
async function submitContactForm(formData) {
    try {
        const response = await fetch(`${API_URL}/contact/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });
        return await response.json();
    } catch (error) {
        console.error("Error submitting contact form:", error);
        throw error;
    }
}

// Fetch all training schedules
async function fetchTraining() {
    try {
        const response = await fetch(`${API_URL}/training/`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching training schedules:", error);
        return [];
    }
}