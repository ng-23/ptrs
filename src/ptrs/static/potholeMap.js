async function initMap() {
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
	const geocoder = new google.maps.Geocoder();
	const myLatLng = { lat: 40.6215, lng: -79.1525 };
	const map = new Map(document.getElementById("map"), {
		center: myLatLng,
		zoom: 15,
		minZoom: 12,
		maxZoom: 20,
		mapId: "c894f5bb0ee453ef",
		disableDefaultUI: true,
		zoomControl: true,
		clickableIcons: false,
	});
	const pinRed = new PinElement({
		background: "#ff0000",
		borderColor: "#990f02",
		glyphColor: "white",
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
				const addressComponents = response.results[0].address_components;
				for (const component of addressComponents) {
					if (component.types.includes('administrative_area_level_2')) {
						const county = component.long_name;
						if (county !== "Indiana County") {
							marker = new AdvancedMarkerElement({
								map,
								content: pinRed.element,
							});;
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
				const pinBlue = new PinElement({
					background: "#0000ff",
					borderColor: "#051094",
					glyphColor: "white",
				});
				const previousReport = new AdvancedMarkerElement({
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
					document.querySelector(".viewDescription.address").innerHTML = previousReport.address.replace(", PA 15701", "").replace(", PA 15705", "");
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