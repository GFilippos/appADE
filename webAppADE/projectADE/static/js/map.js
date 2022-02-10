const mymap = L.map('mymap').setView([0,0], 1);
      const attribution = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright"> \
        OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
      const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      const tiles = L.tileLayer(tileUrl, { attribution });
      tiles.addTo(mymap);
      L.control.scale().addTo(mymap)
      //map coordinate display
      mymap.on('mousemove',function(e){
        $('.coordinate').html(`Latitude: ${e.latlng.lat} Longitude: ${e.latlng.lng}`)
    })
      var marker
      //create a marker and get its location
      mymap.on('click',function(e) {
        var pos = e.latlng
        console.log(e.latlng)
        console.log('map click event')

        marker = L.marker(pos,{icon:myIcon, draggable:true })
        marker.on('drag', function(e) {
          console.log('marker drag event')
        })
      
        marker.on('click', L.DomEvent.stopPropagation)
        marker.addTo(mymap)
      })

      //remove marker