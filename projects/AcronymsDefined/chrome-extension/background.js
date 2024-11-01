// background.js 

// Initialize an empty dictionary object 
let dictionary = {}; 

// Flag to check if dictionary is loaded
let isDictionaryLoaded = false;

// Load the dictionary from the JSON file at extension startup
fetch(chrome.runtime.getURL('dictionary.json'))
    .then(response => response.json())
    .then(data => { 
        dictionary = data; 
        isDictionaryLoaded = true;
    })
    .catch(error => console.error("Error loading dictionary:", error));

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.acronym) {
        if (!isDictionaryLoaded) {
            sendResponse({ definition: "Dictionary not loaded yet. Please try again." });
            return;
        }
        // Convert acronym to uppercase for case-insensitive lookup 
        const acronym = message.acronym.toUpperCase();

        // Look up the acronym in the loaded dictionary 
        const definition = dictionary[acronym] || "Definition not found"; 
        sendResponse({ definition: definition }); 
    }
});
