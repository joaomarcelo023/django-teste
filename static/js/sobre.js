document.addEventListener("DOMContentLoaded", () => {
        var mapProp1 = {
            center:new google.maps.LatLng(-22.389428,-42.952799),
            zoom:16,
        };
        var marker1 = new google.maps.Marker({position: { lat: -22.389428, lng: -42.952799 }});

        var map1 = new google.maps.Map(document.getElementById("googleMap1"),mapProp1);
        marker1.setMap(map1);
        
        var mapProp2 = {
            center:new google.maps.LatLng(-22.668502807617188,-43.01982116699219),
            zoom:16,
        };
        var marker2 = new google.maps.Marker({position: { lat: -22.668502807617188, lng: -43.01982116699219 }});

        var map2 = new google.maps.Map(document.getElementById("googleMap2"),mapProp2);
        marker2.setMap(map2);

        var mapProp3 = {
            center:new google.maps.LatLng(-22.4077205657959,-42.95934295654297),
            zoom:16,
        };
        var marker3 = new google.maps.Marker({position: { lat: -22.4077205657959, lng: -42.95934295654297 }});

        var map3 = new google.maps.Map(document.getElementById("googleMap3"),mapProp3);
        marker3.setMap(map3);
});