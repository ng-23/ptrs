async function initMap() {
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
	const geocoder = new google.maps.Geocoder();
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

	const featureLayer = map.getFeatureLayer('ADMINISTRATIVE_AREA_LEVEL_2');
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

	let pinRed = new PinElement({
		background: "#ff0000",
		borderColor: "#990f02",
		glyphColor: "#ffffff",
	});
	let marker = new AdvancedMarkerElement({
		map,
		content: pinRed.element,
	});

	map.addListener("click", (e) => {
		let latitude = e.latLng.lat();
		let longitude = e.latLng.lng();
		marker.position = { lat: latitude, lng: longitude };

		geocoder.geocode({ location: e.latLng })
			.then((response) => {
				let addressComponents = response.results[0].address_components;

				for (let component of addressComponents) {
					if (component.types.includes('administrative_area_level_2')) {
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
				document.querySelector("#address").innerHTML = address;

				fetch("http://127.0.0.1:5000/data", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ address: address, latitude: latitude, longitude: longitude }),
				})
					.then((response) => response.text())
					.catch((error) => {
						console.error("Error:", error);
					});
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	});

	fetch("http://127.0.0.1:5000/data", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((response) => response.text())
		.then((data) => {
			for (let pothole of JSON.parse(data)) {
				let pinBlue = new PinElement({
					background: "#0000ff",
					borderColor: "#051094",
					glyphColor: "#ffffff",
				});
				let previousReport = new AdvancedMarkerElement({
					map,
					position: { lat: pothole.latitude, lng: pothole.longitude },
					content: pinBlue.element,
				});

				previousReport.address = pothole.address;
				previousReport.size = pothole.size;
				previousReport.other = pothole.other;
				previousReport.repairStatus = pothole.repairStatus;
				previousReport.reportDate = pothole.reportDate;
				previousReport.expectedCompletion = pothole.expectedCompletion;

				previousReport.addListener("click", () => {
					map.setZoom(18);
					map.setCenter(previousReport.position);
					document.querySelector(".viewLabel.address").innerHTML = "Street Address:";
					document.querySelector(".viewDescription.address").innerHTML = previousReport.address;
					document.querySelector(".viewLabel.size").innerHTML = "Size:";
					document.querySelector(".viewDescription.size").innerHTML = previousReport.size + "/10";
					document.querySelector(".viewLabel.repairStatus").innerHTML = "Repair Status:";
					document.querySelector(".viewDescription.repairStatus").innerHTML = previousReport.repairStatus;
					document.querySelector(".viewLabel.reportDate").innerHTML = "Report Date:";
					document.querySelector(".viewDescription.reportDate").innerHTML = previousReport.reportDate;
					document.querySelector(".viewLabel.expectedCompletion").innerHTML = "Expected Completion Date:";
					document.querySelector(".viewDescription.expectedCompletion").innerHTML = previousReport.expectedCompletion;
				});
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}

window.initMap = initMap;