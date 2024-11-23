async function initMap() {
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
	const myLatLng = { lng: -79.1525, lat: 40.6215 };
	const map = new Map(document.getElementById("map"), {
		center: myLatLng,
		zoom: 12,
		mapId: "c894f5bb0ee453ef",
	});
	const marker = new AdvancedMarkerElement({
		map,
		position: myLatLng,
		title: 'Uluru',
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
					borderColor: "#0000ff",
					glyphColor: "white",
				});
				new AdvancedMarkerElement({
					map,
					position: {lng: pothole.longitude, lat: pothole.latitude},
					content: pinBlue.element,
				});
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}

window.initMap = initMap;