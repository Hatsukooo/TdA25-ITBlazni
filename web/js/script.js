// Ahoj Function
function Ahoj() {
    console.log("Co to tady děláš????");
}
Ahoj();

document.addEventListener("DOMContentLoaded", function () {
    const apiUrls = {
        production: "https://26e7458d.app.deploy.tourde.app/api/v1/games/",
        development: "http://localhost:8000/api/v1/games/"
    };

    const environment = "production";
    const apiUrl = apiUrls[environment];

    const levelList = document.getElementById("level-list");

    async function fetchLevels() {
        try {
            const response = await fetch(apiUrl);
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
        if (levels.length === 0) {
            levelList.innerHTML = "<li>No levels available. <strong>DEV_TEST #1</strong></li>";
            return;
        }

        levelList.innerHTML = "";
        levels.forEach((level, index) => {
            const levelItem = document.createElement("li");
            levelItem.classList.add("level-item");
            levelItem.innerHTML = `
                <div class="level-card">
                    <h3>Level #${index + 1}: ${level.name}</h3>
                    <p><strong>Obtížnost:</strong> ${level.difficulty}</p>
                    <p><strong>Status:</strong> ${level.gameState}</p>
                    <p><strong>Vytvořeno:</strong> ${new Date(level.createdAt).toLocaleString()}</p>
                    <p><strong>Aktualizováno:</strong> ${new Date(level.updatedAt).toLocaleString()}</p>
                    <a href="{% url 'game' %}?level=${level.uuid}" class="btn">Hrát Level</a>
                </div>
            `;
            levelList.appendChild(levelItem);
        });
    }

    if (levelList) {
        fetchLevels();
    }

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
});
