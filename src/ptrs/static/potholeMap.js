async function initMap() {
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
	const myLatLng = { lat: 40.6215, lng: -79.1525 };
	const map = new Map(document.getElementById("map"), {
		center: myLatLng,
		zoom: 12,
		minZoom: 12,
		maxZoom: 18,
		mapId: "c894f5bb0ee453ef",
		mapTypeControl: false,
		streetViewControl: false,
		fullscreenControl: false,
	});
	const pinRed = new PinElement({
		background: "#ff0000",
		borderColor: "#990f02",
		glyphColor: "white",
	});
	const marker = new AdvancedMarkerElement({
		map,
		position: myLatLng,
		content: pinRed.element,
	});

	map.addListener("click", (e) => {
		let latitude = e.latLng.lat();
		let longitude = e.latLng.lng();
		marker.position = { lat: latitude, lng: longitude };

		let url = `https://api.geoapify.com/v1/geocode/reverse?lat=${latitude}&lon=${longitude}&apiKey=cae0e983bd184089b8f89641f5538ee8`;

		fetch(url)
			.then((result) => result.json())
			.then((featureCollection) => {
				let address = featureCollection.features[0].properties.formatted.replace(", United States of America", "");
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
				previousReport.addListener("click", () => {
					map.setZoom(18);
					map.setCenter(previousReport.position);
				});
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}

window.initMap = initMap;