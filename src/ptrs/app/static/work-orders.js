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
                // Create information elements for each work order
                let card = gridContainer.appendChild(document.createElement("div"));
                if (["repaired", "removed", "temporarily repaired"].includes(workOrder.pothole.repair_status)) {
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
                location.innerHTML = "Location: " + workOrder.pothole.location.replace("_", " ")
                    .replace(/(^\w)|(\s+\w)/g, (letter) => letter.toUpperCase());

                let repairPriority = displayInfo.appendChild(document.createElement("p"));
                repairPriority.innerHTML = "Repair Priority: " + workOrder.pothole.repair_priority
                    .replace(/(^\w)/g, (letter) => letter.toUpperCase());

                let repairType = displayInfo.appendChild(document.createElement("p"));
                repairType.innerHTML = "Repair Type: " + workOrder.pothole.repair_type
                    .replace(/(^\w)/g, (letter) => letter.toUpperCase());

                let estManHours = displayInfo.appendChild(document.createElement("p"));
                estManHours.innerHTML = "Estimated Man Hours: " + workOrder.estimated_man_hours;

                let repairStatus = displayInfo.appendChild(document.createElement("p"));
                repairStatus.innerHTML = "Repair Status: " + workOrder.pothole.repair_status
                    .replace(/(^\w)|(\s+\w)/g, (letter) => letter.toUpperCase());

                let otherInfo = displayInfo.appendChild(document.createElement("p"));
                otherInfo.innerHTML = "Other Information: " + workOrder.pothole.other_info;
                otherInfo.style.overflow = "hidden";

                let updateButton = displayInfo.appendChild(document.createElement("button"));
                updateButton.innerHTML = "Update";
                updateButton.classList.add("updateButton");

                updateButton.addEventListener("click", () => {
                    fetch(`/api/pothole?pothole_id=${workOrder.pothole_id}`, {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            "repair_status": "repaired"
                        }),
                    })
                        .then((response) => response.text())
                        .catch((error) => {
                            console.error("Error:", error);
                        });

                    window.location.reload();
                })

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

let activeButton = document.querySelector(".activeButton");
let completeButton = document.querySelector(".completeButton");
let generateReportButton = document.querySelector(".generateReportButton");
let cancelGenerateReportButton = document.querySelector(".popup > .cancel");
let generateReportSubmitButton = document.querySelector(".popup > input[type=submit]");

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

generateReportButton.addEventListener("click", function() {
    document.querySelectorAll("body :not(.popup, .popup > label, .popup > select, .popup > .cancel, .popup > input[type=submit])")
        .forEach(element => element.style.filter = "blur(2px)");
    document.querySelector(".popup").style.visibility = "visible";
    document.querySelector(".popup").style.opacity = "1";
})

cancelGenerateReportButton.addEventListener("click", function() {
    document.querySelectorAll("*").forEach(element => element.style.filter = "none");
    document.querySelector(".popup").style.visibility = "hidden";
    document.querySelector(".popup").style.opacity = "0";
})

generateReportSubmitButton.addEventListener("click", function() {
    document.querySelectorAll("*").forEach(element => element.style.filter = "none");
    document.querySelector(".popup").style.visibility = "hidden";
    document.querySelector(".popup").style.opacity = "0";

    let sortBy = document.querySelector("#sortBy").value;
    let order = document.querySelector("#order").value;
    let filter = (order === "ascending") ? "?sort_by=%2b" + sortBy : "?sort_by=%2d" + sortBy;

    window.open(window.location.href.replace("/work-orders/", `/api/report/${filter}`), "_blank");
})

window.initMap = initMap;