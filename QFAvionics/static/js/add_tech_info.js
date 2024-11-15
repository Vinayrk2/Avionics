
document.addEventListener("DOMContentLoaded", function () {
    const featureContainer1 = document.createElement("div");
    const jsonField1 = document.querySelector("#technical_info");
    jsonField1.style.display = "none";  // Hide the raw JSON textarea

    // Button to add a new field-value pair
    const addFeatureButton1 = document.createElement("button");
    addFeatureButton1.textContent = "Add Technical Information";
    addFeatureButton1.type = "button";
    addFeatureButton1.classList.add('defaultadmin');

    addFeatureButton1.onclick = addFeatureInput1;
    featureContainer1.appendChild(addFeatureButton1);

    jsonField1.parentElement.appendChild(featureContainer1);

    const notice1 = document.createElement("p")
    notice1.textContent = "* Any changes in the fields require you to confirm and save. After that it will reflect to the system.";
    notice1.style = "color:red;"
    jsonField1.parentElement.after(notice1)
    // Load existing JSON data if any
    let features1 = {};
    try {
        features1 = JSON.parse(jsonField1.value) || {};
    } catch (e) {
        console.error("Invalid JSON data in features1 field.");
    }
    Object.entries(features1).forEach(([key, value]) => {
        addFeatureInput1(key, value);
    });

    function addFeatureInput1(field = "", value = "") {
        const wrapper1 = document.createElement("div");
        wrapper1.className = "feature-input";
        
        // Create input for field name
        const fieldInput1 = document.createElement("input");
        fieldInput1.type = "text";
        fieldInput1.placeholder = "Field";
        fieldInput1.value = typeof(field) == "string"?  field : "";
        
        fieldInput1.onchange = () => {
            updateButton1.removeAttribute("disabled")
        }


        wrapper1.appendChild(fieldInput1);

        // Create input for field value
        const valueInput1 = document.createElement("textarea");
        valueInput1.type = "text";
        valueInput1.placeholder = "Value";
        valueInput1.value = value;
        valueInput1.className = "jsonfield"
        valueInput1.row = "2"
        valueInput1.cols = "110"
        wrapper1.appendChild(valueInput1);
        wrapper1.onchange = () => {
            updateButton1.removeAttribute("disabled")
        }
        // Create update button
        const updateButton1 = document.createElement("button");
        updateButton1.textContent = "Confirm";
        updateButton1.type = "button";
        updateButton1.classList.add('defaultadmin');
        updateButton1.onclick = () => {
            features1[fieldInput1.value] = valueInput1.value;
            updateJsonField1();
            updateButton1.setAttribute("disabled",true)
        };
        updateButton1.setAttribute("disabled",true)
        wrapper1.appendChild(updateButton1);

        // Create delete button
        const deleteButton1 = document.createElement("a");
        deleteButton1.textContent = "Delete";
        deleteButton1.type = "button";
        deleteButton1.classList.add("deletelink");
        deleteButton1.onclick = () => {
            delete features1[fieldInput1.value];
            wrapper1.remove();
            updateJsonField1();
            console.log(jsonField1.value)
        };
        wrapper1.appendChild(deleteButton1);
        featureContainer1.appendChild(wrapper1);

        
    }

    function updateJsonField1() {
        jsonField1.value = JSON.stringify(features1);
    }
    
    // Serialize all fields as JSON before form submission
    document.querySelector("form").onsubmit = function () {
        updateJsonField1();
        
    };
});
