document.addEventListener("DOMContentLoaded", function () {
    const featureContainer = document.createElement("div");
    const jsonField = document.querySelector("#features");
    jsonField.style.display = "none";  // Hide the raw JSON textarea

    // Button to add a new field-value pair
    const addFeatureButton = document.createElement("button");
    addFeatureButton.textContent = "Add Feature";
    addFeatureButton.type = "button";
    addFeatureButton.onclick = addFeatureInput;
    featureContainer.appendChild(addFeatureButton);

    jsonField.parentElement.appendChild(featureContainer);

    // Load existing JSON data if any
    let features = {};
    try {
        features = JSON.parse(jsonField.value) || {};
    } catch (e) {
        console.error("Invalid JSON data in features field.");
    }
    Object.entries(features).forEach(([key, value]) => {
        addFeatureInput(key, value);
    });

    function addFeatureInput(field = "", value = "") {
        const wrapper = document.createElement("div");
        wrapper.className = "feature-input";
        
        // Create input for field name
        const fieldInput = document.createElement("input");
        fieldInput.type = "text";
        fieldInput.placeholder = "Field";
        fieldInput.value = field;
        wrapper.appendChild(fieldInput);

        // Create input for field value
        const valueInput = document.createElement("input");
        valueInput.type = "text";
        valueInput.placeholder = "Value";
        valueInput.value = value;
        wrapper.appendChild(valueInput);

        // Create update button
        const updateButton = document.createElement("button");
        updateButton.textContent = "Confirm";
        updateButton.type = "button";
        updateButton.onclick = () => {
            features[fieldInput.value] = valueInput.value;
            updateJsonField();
        };
        wrapper.appendChild(updateButton);

        // Create delete button
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.type = "button";
        deleteButton.onclick = () => {
            delete features[fieldInput.value];
            wrapper.remove();
            updateJsonField();
            console.log(jsonField.value)
        };
        wrapper.appendChild(deleteButton);
        console.log(features)
        featureContainer.appendChild(wrapper);
    }

    function updateJsonField() {
        jsonField.value = JSON.stringify(features);
    }
    
    // Serialize all fields as JSON before form submission
    document.querySelector("form").onsubmit = function () {
        updateJsonField();
        
    };
});
