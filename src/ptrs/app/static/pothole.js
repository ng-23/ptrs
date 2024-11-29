async function initMap() {
	// Import libraries
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
	const geocoder = new google.maps.Geocoder();

	// Create map
	const myLatLng = { lat: 40.66062326610511, lng: -79.06163481811751 };
	const map = new Map(document.getElementById("map"), {
		center: myLatLng,
		zoom: 10,
		minZoom: 10,
		maxZoom: 20,
		mapId: "c894f5bb0ee453ef",
		disableDefaultUI: true,
		zoomControl: true,
		clickableIcons: false,
	});

	// Feature layer adds outline on map of Indiana County
	const featureLayer = map.getFeatureLayer("ADMINISTRATIVE_AREA_LEVEL_2");
	const featureStyleOptions = {
		strokeColor: "#000000",
		strokeOpacity: 0.25,
		strokeWeight: 3.0,
	};
	featureLayer.style = (options) => {
		if (options.feature.placeId === "ChIJVQHtdMRBy4kRWBdHCi1ccYc") {
			return featureStyleOptions;
		}
	};

	// Create and style marker for new pothole
	let pinRed = new PinElement({
		background: "#ff0000",
		borderColor: "#990f02",
		glyphColor: "#ffffff",
	});
	let marker = new AdvancedMarkerElement({
		map,
		content: pinRed.element,
	});

	let newPotholeAddress = { latitude: 0, longitude: 0, address: "" };

	map.addListener("click", (e) => {
		// Variables
		let latitude = e.latLng.lat();
		let longitude = e.latLng.lng();
		marker.position = { lat: latitude, lng: longitude };
		[newPotholeAddress.latitude, newPotholeAddress.longitude] = [latitude, longitude];

		geocoder
			.geocode({ location: e.latLng })
			.then((response) => {
				// Check for valid "Administrative Area Level 2" (County)
				let addressComponents = response.results[0].address_components;
				for (let component of addressComponents) {
					if (component.types.includes("administrative_area_level_2")) {
						let county = component.long_name;

						if (county !== "Indiana County") {
							marker = new AdvancedMarkerElement({
								map,
								content: pinRed.element,
							});

							alert("Chosen pin is not within Indiana County!");
							throw new Error("Chosen pin is not within Indiana County!");
						}
					}
				}

				let address = response.results[0].formatted_address.replace(", USA", "");
				document.querySelector("#address").value = address;
				newPotholeAddress.address = address;
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	});

	fetch("/potholes", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((response) => response.text())
		.then((data) => {
			for (let pothole of JSON.parse(data).potholes) {
				// Create and style markers for previous reports
				let pinBlue = new PinElement({
					background: "#0000ff",
					borderColor: "#051094",
					glyphColor: "#ffffff",
				});
				let previousReportMarker = new AdvancedMarkerElement({
					map,
					position: { lat: pothole.latitude, lng: pothole.longitude },
					content: pinBlue.element,
				});

				// View selected pothole use case
				previousReportMarker.addListener("click", () => {
					map.setZoom(18);
					map.setCenter(previousReportMarker.position);

					let labels = document.querySelectorAll(".viewLabel");
					let descriptions = document.querySelectorAll(".viewDescription");
					let values = [
						pothole.street_addr,
						pothole.size,
						pothole.repair_status.replace(/(^\w{1})|(\s+\w{1})/g, (letter) => letter.toUpperCase()),
						pothole.report_date,
						pothole.expected_completion,
					];

					for (let i = 0; i < value.length; i++) {
						labels[i].style.display = "block";
						descriptions[i].style.display = "block";
						descriptions[i].innerHTML = values[i];
					}
				});
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});

	const form = document.querySelector("#newPotholeForm");
	form.addEventListener("submit", function () {
		// Variables
		let formData = new FormData(form);

		// Report pothole use case
		fetch("/pothole", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				street_addr: newPotholeAddress.address,
				latitude: newPotholeAddress.latitude,
				longitude: newPotholeAddress.longitude,
				size: formData.get("size") / 10,
				location: formData.get("location"),
				other: formData.get("other"),
			}),
		})
			.then((response) => response.text())
			.catch((error) => {
				console.error("Error:", error);
			});
	});
}

window.initMap = initMap;
