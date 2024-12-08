/**
 * Function to create 'manage work order' card
 * @param workOrder     Dictionary object containing work order information from server
 * @param i             Index value used so google api can discern between the different maps
 */
function createCard(workOrder, i) {
    const gridContainer = document.querySelector(".gridContainer");
    // Create information elements for each work order
    let card = gridContainer.appendChild(document.createElement("div"));
    if (workOrder.pothole.repair_status === "not repaired") {
        card.classList.add(...["card", "active"])
    }
    else {
        card.classList.add(...["card", "complete"]);
        card.style.display = "none";
    }
    // Create map
    let mapDiv = card.appendChild(document.createElement("div"));
    mapDiv.classList.add(...["map", `map${i}`]);
    // Create div for information
    let displayInfo = card.appendChild(document.createElement("div"));
    displayInfo.classList.add("displayInfo");
    // Create work order id element
    let workOrderID = displayInfo.appendChild(document.createElement("h1"));
    workOrderID.innerHTML = "Work Order: " + workOrder.work_order_id;
    // Create pothole id element
    let potholeID = displayInfo.appendChild(document.createElement("p"));
    potholeID.innerHTML = "Pothole: " + workOrder.pothole_id;
    // Break a line
    displayInfo.appendChild(document.createElement("br"));
    // Create address element
    let address = displayInfo.appendChild(document.createElement("p"));
    address.innerHTML = "Address: " + workOrder.pothole.street_addr;
    // Create assignment date element
    let assignmentDate = displayInfo.appendChild(document.createElement("p"));
    assignmentDate.innerHTML = "Assignment Date: " + workOrder.assignment_date;
    // Create expected completion date element
    let expectedCompletion = displayInfo.appendChild(document.createElement("p"));
    expectedCompletion.innerHTML = "Expected Completion Date: " + workOrder.pothole.expected_completion;
    // Create size element
    let size = displayInfo.appendChild(document.createElement("p"));
    size.innerHTML = "Size: " + workOrder.pothole.size + "/10";
    // Create location element
    let location = displayInfo.appendChild(document.createElement("p"));
    location.innerHTML = "Location: " + workOrder.pothole.location.replace("_", " ")
        .replace(/(^\w)|(\s+\w)/g, (letter) => letter.toUpperCase());
    // Create repair priority element
    let repairPriority = displayInfo.appendChild(document.createElement("p"));
    repairPriority.innerHTML = "Repair Priority: " + workOrder.pothole.repair_priority
        .replace(/(^\w)/g, (letter) => letter.toUpperCase());
    // Create repair type element
    let repairType = displayInfo.appendChild(document.createElement("p"));
    repairType.innerHTML = "Repair Type: " + workOrder.pothole.repair_type
        .replace(/(^\w)/g, (letter) => letter.toUpperCase());
    // Create estimated man-hours element
    let estManHours = displayInfo.appendChild(document.createElement("p"));
    estManHours.innerHTML = "Estimated Man-Hours: " + workOrder.estimated_man_hours;
    // Create repair status element
    let repairStatus = displayInfo.appendChild(document.createElement("p"));
    repairStatus.innerHTML = "Repair Status: " + workOrder.pothole.repair_status
        .replace(/(^\w)|(\s+\w)/g, (letter) => letter.toUpperCase());
    // Create other information element
    let otherInfo = displayInfo.appendChild(document.createElement("p"));
    otherInfo.innerHTML = "Other Information: " + workOrder.pothole.other_info;
    otherInfo.style.overflow = "hidden";
    // Create update button element
    let updateButton = displayInfo.appendChild(document.createElement("button"));
    updateButton.innerHTML = "Update";
    updateButton.classList.add("updateButton");

    // Event listener for clicking update button on each Work Order card
    updateButton.addEventListener("click", () => {
        const workOrderCancelButton = document.querySelector(".workOrderPopup > .cancel");
        const workOrderSubmitButton = document.querySelector(".workOrderPopup > input[type=submit]");

        document.querySelectorAll("body :not(.workOrderPopup, .workOrderPopup > label, .workOrderPopup > select, " +
            ".workOrderPopup > input[type=number], .workOrderPopup > .cancel, .workOrderPopup > input[type=submit])")
            .forEach(element => element.style.filter = "blur(2px)");
        document.querySelector(".workOrderPopup").style.visibility = "visible";
        document.querySelector(".workOrderPopup").style.opacity = "1";

        // Cancel updating work order
        workOrderCancelButton.addEventListener("click", function() {
            document.querySelectorAll("*").forEach(element => element.style.filter = "none");
            document.querySelector(".workOrderPopup").style.visibility = "hidden";
            document.querySelector(".workOrderPopup").style.opacity = "0";
        })

        // Submit update of work order to server
        workOrderSubmitButton.addEventListener("click", function() {
            let repair_status = document.querySelector("#repairStatus").value;
            let actual_man_hours = document.querySelector("#actualManHours").value;

            // If 'Actual Man-Hours' is not provided show alert and throw error
            if (actual_man_hours === "" && workOrder.pothole.repair_status === "not repaired" && repair_status !== "removed") {
                alert("Please provide an input for 'Actual Man-Hours'");
                throw new Error("User provided no input for 'Actual Man-Hours'");
            }
            else {
                document.querySelectorAll("*").forEach(element => element.style.filter = "none");
                document.querySelector(".workOrderPopup").style.visibility = "hidden";
                document.querySelector(".workOrderPopup").style.opacity = "0";

                // Send update request of pothole to server
                fetch(`/api/pothole/?pothole_id=${workOrder.pothole_id}`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        "repair_status": repair_status
                    }),
                })
                    .then((response) => response.text())
                    .catch((error) => {
                        console.error("Error:", error);
                    });
                // Send update request of work order to server
                if (actual_man_hours !== "" && repair_status !== "removed") {
                    fetch(`/api/work-order/?work_order_id=${workOrder.work_order_id}`, {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            "actual_man_hours": actual_man_hours
                        }),
                    })
                        .then((response) => response.text())
                        .catch((error) => {
                            console.error("Error:", error);
                        });
                }

                window.location.reload();
            }
        })
    })
}


/**
 * Function that will be called by map API
 */
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    // Get all work orders from server and display them as cards
    fetch("/api/work-orders", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.text())
        .then((data) => {
            // Parse the JSON string into an object
            let parsedData = JSON.parse(data);
            let i = 1;

            for (let workOrder of parsedData.data) {
                createCard(workOrder, i);

                // Create map element for each work order
                let map = new Map(document.querySelector(`.map${i}`), {
                    center: { lat: workOrder.pothole.latitude, lng: workOrder.pothole.longitude },
                    zoom: 16,
                    mapId: "c894f5bb0ee453ef",
                    disableDefaultUI: true,
                    zoomControl: false,
                    draggable: false,
                    clickableIcons: false,
                });

                let pinBlue = new PinElement({
                    background: "#0000ff",
                    borderColor: "#051094",
                    glyphColor: "#ffffff",
                });
                new AdvancedMarkerElement({
                    map,
                    position: { lat: workOrder.pothole.latitude, lng: workOrder.pothole.longitude },
                    content: pinBlue.element,
                });

                i++;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}


// Button elements
const activeButton = document.querySelector(".activeButton");
const completeButton = document.querySelector(".completeButton");
const generateReportButton = document.querySelector(".generateReportButton");
const generateReportCancelButton = document.querySelector(".reportPopup > .cancel");
const generateReportSubmitButton = document.querySelector(".reportPopup > input[type=submit]");


// Show active work orders and hide complete work orders
activeButton.addEventListener("click", function() {
    activeButton.style.backgroundColor = "#007aff";
    activeButton.style.color = "#ffffff";
    completeButton.style.backgroundColor = "#ffffff";
    completeButton.style.color = "#000000";

    let cards = document.querySelectorAll(".card");
    for (let card of cards) {
        card.style.display = (card.classList.contains("active")) ? "block" : "none";
    }
});


// Show complete work orders and hide active work orders
completeButton.addEventListener("click", function() {
    activeButton.style.backgroundColor = "#ffffff";
    activeButton.style.color = "#000000";
    completeButton.style.backgroundColor = "#007aff";
    completeButton.style.color = "#ffffff";

    let cards = document.querySelectorAll(".card");
    for (let card of cards) {
        card.style.display = (card.classList.contains("complete")) ? "block" : "none";
    }
});


// Display popup after clicking generate report
generateReportButton.addEventListener("click", function() {
    document.querySelectorAll("body :not(.reportPopup, .reportPopup > label, .reportPopup > select, .reportPopup > .cancel, .reportPopup > input[type=submit])")
        .forEach(element => element.style.filter = "blur(2px)");
    document.querySelector(".reportPopup").style.visibility = "visible";
    document.querySelector(".reportPopup").style.opacity = "1";
})


// Cancel generate report
generateReportCancelButton.addEventListener("click", function() {
    document.querySelectorAll("*").forEach(element => element.style.filter = "none");
    document.querySelector(".reportPopup").style.visibility = "hidden";
    document.querySelector(".reportPopup").style.opacity = "0";
})


// Submit generate report
generateReportSubmitButton.addEventListener("click", function() {
    document.querySelectorAll("*").forEach(element => element.style.filter = "none");
    document.querySelector(".reportPopup").style.visibility = "hidden";
    document.querySelector(".reportPopup").style.opacity = "0";

    let sortBy = document.querySelector("#sortBy").value;
    let order = document.querySelector("#order").value;
    let filter = (order === "ascending") ? "?sort_by=%2b" + sortBy : "?sort_by=%2d" + sortBy;

    // Open report in new tab with filter
    window.open(window.location.href.replace("/work-orders/", `/api/report/${filter}`), "_blank");
})


window.initMap = initMap;