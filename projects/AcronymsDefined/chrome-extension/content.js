// content.js 

// At the top of content.js
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = chrome.runtime.getURL('popup.css');
document.head.appendChild(link);


document.addEventListener('mouseup', () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 1 && /^[A-Z]{2,}$/.test(selectedText)) {
        fetchAcronymDefinition(selectedText);
    }
});

function fetchAcronymDefinition(acronym) {
    // For this example, we'll use a simple local dictionary. 
    // You can replace this with an API call to fetch acronym definitions.
    chrome.runtime.sendMessage({ acronym: acronym }, (response) => {
        if (response && response.definition) {
            showPopup(acronym, response.definition);
        }
    });
}

function showPopup(acronym, definition) {
    // Remove existing popup if any
    const existingPopup = document.getElementById('acronym-popup');
    if (existingPopup) {
        existingPopup.remove();
    }

    let popup = document.createElement('div');
    popup.id = 'acronym-popup';
    popup.innerHTML = `<strong>${acronym}:</strong> ${definition}`;
    popup.classList.add('acronym-popup');  // Add CSS class instead of inline styles

    document.body.appendChild(popup);

    // Position and display logic remains the same
    // ...
}


    let popup = document.createElement('div');
    popup.id = 'acronym-popup';
    popup.innerHTML = `<strong>${acronym}:</strong> ${definition}`;

    // Styling for a modern look 
    popup.style.position = 'absolute';
    popup.style.background = 'linear-gradient(135deg, #ffffff, #f0f0f0)';
    popup.style.color = '#333';
    popup.style.border = '1px solid #ddd';
    popup.style.borderRadius = '8px';
    popup.style.padding = '15px';
    popup.style.fontFamily = 'Arial, sans-serif';
    popup.style.fontSize = '14px';
    popup.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    popup.style.transition = 'opacity 0.2s ease';
    popup.style.opacity = '0';
    popup.style.zIndex = '10000';
    document.body.appendChild(popup);

    // Fade-in effect 
    setTimeout(() => { popup.style.opacity = '1'; }, 0);

    // Optional: Set up an event listener to hide the popup on click 
    popup.addEventListener('click', () => { 
        popup.style.opacity = '0';
        setTimeout(() => { document.body.removeChild(popup); }, 300); 
    });

    positionPopup(popup);

    // Click elsewhere to close the popup 
    document.addEventListener('click', closePopup);
    document.addEventListener('keydown', (e) => { 
        if (e.key === 'Escape') { closePopup(); } 
    });

    function positionPopup(popup) {
        const selection = window.getSelection();
        if (selection.rangeCount === 0) return;
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        popup.style.top = `${rect.bottom + window.scrollY + 5}px`;  // Added 5px for spacing
        popup.style.left = `${rect.left + window.scrollX}px`;
    }

    function closePopup() { 
        const popup = document.getElementById('acronym-popup'); 
        if (popup) { popup.remove(); } 
        document.removeEventListener('click', closePopup); 
    }
