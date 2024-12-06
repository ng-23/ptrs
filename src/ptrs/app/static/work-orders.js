async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    const gridContainer = document.querySelector(".gridContainer");

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
                let card = gridContainer.appendChild(document.createElement("div"));
                if (workOrder.pothole.repair_status === "repaired" || workOrder.pothole.repair_status === "removed") {
                    card.classList.add(...["card", `workOrder${i}`, "complete"]);
                    card.style.display = "none";
                }
                else {
                    card.classList.add(...["card", `workOrder${i}`, "active"])
                }

                let mapDiv = card.appendChild(document.createElement("div"));
                mapDiv.classList.add(...["map", `map${i}`]);

                let displayInfo = card.appendChild(document.createElement("div"));
                displayInfo.classList.add("displayInfo");

                let workOrderID = displayInfo.appendChild(document.createElement("h1"));
                workOrderID.innerHTML = "Work Order: " + workOrder.work_order_id;

                let potholeID = displayInfo.appendChild(document.createElement("p"));
                potholeID.innerHTML = "Pothole: " + workOrder.pothole_id;

                displayInfo.appendChild(document.createElement("br"));

                let address = displayInfo.appendChild(document.createElement("p"));
                address.innerHTML = "Address: " + workOrder.pothole.street_addr;

                let assignmentDate = displayInfo.appendChild(document.createElement("p"));
                assignmentDate.innerHTML = "Assignment Date: " + workOrder.assignment_date;

                let expectedCompletion = displayInfo.appendChild(document.createElement("p"));
                expectedCompletion.innerHTML = "Expected Completion Date: " + workOrder.pothole.expected_completion;

                let size = displayInfo.appendChild(document.createElement("p"));
                size.innerHTML = "Size: " + workOrder.pothole.size + "/10";

                let location = displayInfo.appendChild(document.createElement("p"));
                location.innerHTML = "Location: " + workOrder.pothole.location.replace("_", " ").replace(/(^\w{1})|(\s+\w{1})/g, (letter) => letter.toUpperCase());

                let repairPriority = displayInfo.appendChild(document.createElement("p"));
                repairPriority.innerHTML = "Repair Priority: " + workOrder.pothole.repair_priority.replace(/(^\w{1})/g, (letter) => letter.toUpperCase());

                let repairType = displayInfo.appendChild(document.createElement("p"));
                repairType.innerHTML = "Repair Type: " + workOrder.pothole.repair_type.replace(/(^\w{1})/g, (letter) => letter.toUpperCase());

                let estManHours = displayInfo.appendChild(document.createElement("p"));
                estManHours.innerHTML = "Estimated Man Hours: " + workOrder.estimated_man_hours;

                let repairStatus = displayInfo.appendChild(document.createElement("p"));
                repairStatus.innerHTML = "Repair Status: " + workOrder.pothole.repair_status.replace(/(^\w{1})|(\s+\w{1})/g, (letter) => letter.toUpperCase());

                let otherInfo = displayInfo.appendChild(document.createElement("p"));
                otherInfo.innerHTML = "Other Information: " + workOrder.pothole.other_info;

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
                let previousReportMarker = new AdvancedMarkerElement({
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

let activeButton = document.querySelector(".activeButton");
let completeButton = document.querySelector(".completeButton");

activeButton.addEventListener("click", function() {
    activeButton.style.backgroundColor = "#007aff";
    activeButton.style.color = "#ffffff";
    completeButton.style.backgroundColor = "#ffffff";
    completeButton.style.color = "#000000";

    let cards = document.querySelectorAll(".card");
    for (let card of cards) {
        if (card.classList.contains("active")) {
            card.style.display = "block";
        }
        else {
            card.style.display = "none";
        }
    }
});

completeButton.addEventListener("click", function() {
    activeButton.style.backgroundColor = "#ffffff";
    activeButton.style.color = "#000000";
    completeButton.style.backgroundColor = "#007aff";
    completeButton.style.color = "#ffffff";

    let cards = document.querySelectorAll(".card");
    for (let card of cards) {
        if (card.classList.contains("complete")) {
            card.style.display = "block";
        }
        else {
            card.style.display = "none";
        }
    }
});

window.initMap = initMap;