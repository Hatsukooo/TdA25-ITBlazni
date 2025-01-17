// script.js

// Ahoj Function
function Ahoj() {
    console.log("Co to tady děláš????");
}
Ahoj();

document.addEventListener("DOMContentLoaded", function () {
    const apiUrls = {
        production: "https://26e7458d.app.deploy.tourde.app/api/v1/games",
        development: "http://localhost:8000/api/v1/games"
    };

    const environment = "production"; 
    const baseApiUrl = apiUrls[environment];

    const levelList = document.getElementById("level-list");

    // 1) Fetch & Display games without filters initially
    async function fetchLevels(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const levels = await response.json();
            displayLevels(levels);
        } catch (error) {
            console.error("Error fetching levels:", error);
            if (levelList) {
                levelList.innerHTML = "<li>Error loading levels. Please try again later.</li>";
            }
        }
    }

    function displayLevels(levels) {
        if (!levelList) {
            console.error("Level list container not found in the DOM.");
            return;
        }

        if (!levels || levels.length === 0) {
            levelList.innerHTML = "<li>No levels available.</li>";
            return;
        }

        levelList.innerHTML = "";
        levels.forEach((level, index) => {
            const levelItem = document.createElement("li");
            levelItem.classList.add("level-item");
            levelItem.innerHTML = `
                <div class="level-card">
                    <h3>LEVEL #${index + 1}</h3>
                    <p><strong style="color:#AB2E58;">Název:</strong> ${level.name}</p>
                    <p><strong style="color:#AB2E58;">Obtížnost:</strong> ${level.difficulty}</p>
                    <p><strong style="color:#AB2E58;">Status:</strong> ${level.gameState}</p>
                    <p><strong style="color:#AB2E58;">Vytvořeno:</strong> ${new Date(level.createdAt).toLocaleString()}</p>
                    <p><strong style="color:#AB2E58;">Upraveno:</strong> ${new Date(level.updatedAt).toLocaleString()}</p>
                    <a href="/game/${level.uuid}/" class="btn">Hrát Level</a>
                </div>
            `;
            levelList.appendChild(levelItem);
        });
    }

    // 2) Build query string and refetch from server
    function applyFilters() {
        const nameInput = document.getElementById("filterName");
        const difficultySelect = document.getElementById("filterDifficulty");
        const updatedSelect = document.getElementById("filterUpdated");

        const nameVal = nameInput.value.trim();
        const diffVal = difficultySelect.value.trim();
        const updVal = updatedSelect.value.trim();

        // Build query params
        const params = new URLSearchParams();

        if (nameVal) {
            params.append("name", nameVal);
        }
        if (diffVal) {
            params.append("difficulty", diffVal);
        }
        if (updVal) {
            params.append("updated", updVal);
        }

        // Construct the final URL
        const finalUrl = `${baseApiUrl}?${params.toString()}`; 
        console.log("Fetching with filters:", finalUrl);

        // Re-fetch the server with these filters
        fetchLevels(finalUrl);
    }

    // INITIAL LOAD: fetch all games (unfiltered)
    if (levelList) {
        fetchLevels(baseApiUrl);
    }

    // Hook up the "Použít filtry" button
    const applyFiltersBtn = document.getElementById("applyFilters");
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener("click", applyFilters);
    }

    // ---------------------------------------
    // The rest of your existing code remains
    // ---------------------------------------
    
    const textElement = document.getElementById("movingText");
    if (textElement) {
        let xPos = 0;
        let yPos = 0;
        let xSpeed = 1.0;
        let ySpeed = 1.0;

        function moveText() {
            xPos += xSpeed;
            yPos += ySpeed;
            const maxX = window.innerWidth - textElement.offsetWidth;
            const maxY = window.innerHeight - textElement.offsetHeight;
            if (xPos <= 0 || xPos >= maxX) {
                xSpeed = -xSpeed;
            }
            if (yPos <= 0 || yPos >= maxY) {
                ySpeed = -ySpeed;
            }
            textElement.style.left = xPos + "px";
            textElement.style.top = yPos + "px";
            requestAnimationFrame(moveText);
        }

        moveText();
    }

    const loader = document.getElementById('loader');
    window.addEventListener('load', () => {
        if (loader) loader.classList.add('hidden');
    });

    // Theme Toggle Functionality
    const toggleThemeBtn = document.getElementById('toggleTheme');
    const logoImg = document.querySelector('.center-logo');

    function updateLogo(theme) {
        if (logoImg) {
            if (theme === 'light') {
                logoImg.src = logoImg.dataset.lightSrc;
            } else {
                logoImg.src = logoImg.dataset.darkSrc;
            }
        }
    }

    if (localStorage.getItem('theme') === 'light') {
        document.documentElement.classList.add('light-theme');
        if (toggleThemeBtn) toggleThemeBtn.classList.add('active');
        updateLogo('light');
    } else {
        updateLogo('dark');
    }

    if (toggleThemeBtn) {
        toggleThemeBtn.addEventListener('click', () => {
            document.documentElement.classList.toggle('light-theme');
            toggleThemeBtn.classList.toggle('active');

            // Determine current theme
            const isLight = document.documentElement.classList.contains('light-theme');
            updateLogo(isLight ? 'light' : 'dark');

            // Save theme preference
            if (isLight) {
                localStorage.setItem('theme', 'light');
            } else {
                localStorage.setItem('theme', 'dark');
            }
        });
    }
});
