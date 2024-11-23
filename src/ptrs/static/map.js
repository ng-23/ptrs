/*map.on("click", function (e) {
	[markerGPS.longitude, markerGPS.latitude] = [parseFloat(e.lngLat.lng), parseFloat(e.lngLat.lat)];
	mapMarker.setLngLat([markerGPS.longitude, markerGPS.latitude]).addTo(map);
	let url = `https://api.geoapify.com/v1/geocode/reverse?lat=${markerGPS.latitude}&lon=${markerGPS.longitude}&apiKey=cae0e983bd184089b8f89641f5538ee8`;

	fetch(url)
		.then((result) => result.json())
		.then((featureCollection) => {
			markerGPS.address = featureCollection.features[0].properties.formatted.replace(", United States of America", "");
			document.querySelector("#address").innerHTML = markerGPS.address;

			fetch("http://127.0.0.1:5000/data", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ address: markerGPS.address, latitude: markerGPS.latitude, longitude: markerGPS.longitude }),
			})
				.then((response) => response.text())
				.catch((error) => {
					console.error("Error:", error);
				});
		});
});*/


async function initMap() {
	const { Map } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
		"marker",
	);
	const myLatLng = {lng: -79.1525, lat: 40.6215};
	const map = new Map(document.getElementById("map"), {
		center: myLatLng,
		zoom: 12,
		mapId: "c894f5bb0ee453ef",
	})
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