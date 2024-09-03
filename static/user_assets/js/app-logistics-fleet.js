mapboxgl.accessToken = "pk.eyJ1IjoibG9yZC1zaGl2YW0iLCJhIjoiY2xpeTlpNHFwMDVzbDNmczl2MXdob29udyJ9.JOLDU6VQG_ra1CoVG4jbUA";
const r = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/light-v9",
    center: [78.9629, 20.5937],
    zoom: 4
});

var markers = [];

function displayMap() {
    // mapboxgl.accessToken = "pk.eyJ1IjoibG9yZC1zaGl2YW0iLCJhIjoiY2xpeTlpNHFwMDVzbDNmczl2MXdob29udyJ9.JOLDU6VQG_ra1CoVG4jbUA";
    let features_collection = [];
    vehicleData.forEach(vehicle => {
        features_collection.push({
            type: "Feature",
            properties: {iconSize: [20, 42], message: vehicle.id.toString()},
            geometry: {type: "Point", coordinates: [vehicle.longitude, vehicle.latitude]}
        })
    });
    const t = {
        type: "FeatureCollection",
        features: features_collection
        
    };
    for (const i of t.features) {
        
        var e = document.createElement("div");
        o = i.properties.iconSize[0], s = i.properties.iconSize[1];
        e.className = "marker";
        e.insertAdjacentHTML("afterbegin", '<img src="' + assetsPath + 'img/illustrations/fleet-car.png" alt="Fleet Car" width="20" class="rounded-3" id="carFleet-' + i.properties.message + '">');
        e.style.width = o + "px";
        e.style.height = s + "px";
        e.style.cursor = "pointer"
        let marker = new mapboxgl.Marker(e).setLngLat(i.geometry.coordinates).addTo(r);
        markers.push(marker);
        const n = document.getElementById("fl-" + i.properties.message);
        c = document.getElementById("carFleet-" + i.properties.message);
        n.addEventListener("click", function () {
            var e = document.querySelector(".marker-focus");
            Helpers._hasClass("active", n) ? (r.flyTo(
                {
                    center: t.features[i.properties.message - 1].geometry.coordinates,
                    zoom: 16
                }), e && Helpers._removeClass("marker-focus", e), Helpers._addClass("marker-focus", c)) : Helpers._removeClass("marker-focus", c)
        });
    }
    var a = document.getElementById("carFleet-1");
    a = (Helpers._addClass("marker-focus", a), document.querySelector(".mapboxgl-control-container").classList.add("d-none"), $(".logistics-fleet-sidebar-body"));
    a.length && new PerfectScrollbar(a[0], {wheelPropagation: !1, suppressScrollX: !0})
}

displayMap(0);

// execute function displayMap() every 1 seconds

function updateCoords() {
    vehicleData.forEach(vehicle => {
        vehicle.latitude += 0.0001;
        vehicle.longitude -= 0.0001;
    })
}

async function processMap() {
    i = 0;
    while (1) {
        displayMap(i);
        // Wait for 1 second before the next iteration
        await new Promise((resolve) => setTimeout(resolve, 1000)); // 1000 milliseconds = 1 second
        markers.forEach(marker => {
            marker.remove()
        });
        markers = [];
        updateCoords();
        i++;
    }
}

processMap();
