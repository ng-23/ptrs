maptilersdk.config.apiKey = "X6QXRw7moQwVgb7tbcCO";
const mapMarker = new maptilersdk.Marker({ color: "#ff0000" });
const markerGPS = { longitude: null, lattitude: null, address: null };
const map = new maptilersdk.Map({
	container: "map",
	style: maptilersdk.MapStyle.STREETS,
	center: [-79.1525, 40.6215],
	zoom: 12,
	minZoom: 12,
	maxZoom: 18,
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
			let marker = new maptilersdk.Marker({ color: "#0000ff" });
			marker.setLngLat([pothole.longitude, pothole.lattitude]).addTo(map);
		}
	})
	.catch((error) => {
		console.error("Error:", error);
	});

map.on("click", async function (e) {
	[markerGPS.longitude, markerGPS.lattitude] = [parseFloat(e.lngLat.lng), parseFloat(e.lngLat.lat)];
	mapMarker.setLngLat([markerGPS.longitude, markerGPS.lattitude]).addTo(map);
	let url = `https://api.geoapify.com/v1/geocode/reverse?lat=${markerGPS.lattitude}&lon=${markerGPS.longitude}&apiKey=cae0e983bd184089b8f89641f5538ee8`;

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
				body: JSON.stringify({ address: markerGPS.address, lattitude: markerGPS.lattitude, longitude: markerGPS.longitude }),
			})
				.then((response) => response.text())
				.catch((error) => {
					console.error("Error:", error);
				});
		});
});
