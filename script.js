const landscapes = {
    field: "world_display_imgs/le_feild.png",
    mountain: "world_display_imgs/le_mountain.png",
    forest: "world_display_imgs/le_forest.png"
};

const rowPattern = ["field", "mountain", "forest", "mountain", "forest", "field", "mountain", "forest", "mountain", "forest", "field", "mountain", "forest", "mountain", "forest"];
const rows = 15;
const cols = rowPattern.length;

const ownerColors = {
    0: "white",
    1: "red",
    2: "blue",
    3: "green",
    4: "orange",
    5: "purple",
    6: "pink",
    7: "cyan",
    8: "brown",
    9: "yellow"
};

const worldContainer = document.querySelector(".world_display");

// First, fetch the owner data from the JSON
fetch("data.json")
    .then(response => {
        if (!response.ok) throw new Error("Failed to load JSON file");
        return response.json();
    })
    .then(data => {
        worldContainer.innerHTML = ""; // clear previous grid

        for (let r = 0; r < rows; r++) {
            const rowDiv = document.createElement("div");
            rowDiv.classList.add("image_grid");

            for (let c = 0; c < cols; c++) {
                const cellDiv = document.createElement("div");
                cellDiv.classList.add("grid_item");
                cellDiv.id = `cell-${r}-${c}`;

                // Set the image based on rowPattern
                const img = document.createElement("img");
                img.src = landscapes[rowPattern[c]];
                cellDiv.appendChild(img);

                // Set the border color based on owner from JSON
                const ownerId = data.grid[r][c];
                cellDiv.style.border = `2px solid ${ownerColors[ownerId] || "black"}`;

                rowDiv.appendChild(cellDiv);
            }

            worldContainer.appendChild(rowDiv);
        }
    })
    .catch(err => console.error(err));
