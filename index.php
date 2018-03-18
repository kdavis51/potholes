<?php
$data = file_get_contents('/home/myftpuser/gps.dat');
$api_key = 'XXXXXXXXXXXXXXX';  // insert your GOOGLE API KEY
$lines = explode("\n",$data);

foreach ($lines as $key => $value){
	if ($key>0&&strlen($value)>30){ // skip csv header row and blank rows
		$line = explode(",",$value);
		$markers[$key] = trim($line[0]).','.trim($line[1]).','.trim($line[2]).','.trim($line[3]); // title,content,lat,long
		
	}
}
?>
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      html, body, #map-canvas { height: 100%; margin: 0; padding: 0;}
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=<?=$api_key?>">
    </script>
    <script type="text/javascript">
		var map;
		var marker = {};
		function initialize() {
			var mapOptions = {
			  center: { lat: 40.918665, lng: -89.5822216667},
              zoom: 12
		};
		map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
		var markers = [];
		<?php 
			$counter = 0;
			foreach ($markers as $index => $list){
				   $marker_details = explode(',',$list);
				   echo 'markers["m'.($index-1).'"] = {};'."\n";
				   echo "markers['m".($index-1)."'].lat = '".$marker_details[1]."';\n";
				   echo "markers['m".($index-1)."'].lon = '".$marker_details[0]."';\n";
				   echo "markers['m".($index-1)."'].name = '".$marker_details[3]."';\n";
				   echo "markers['m".($index-1)."'].content = '".$marker_details[2]."';\n";
				   $counter++;
		   }
		?>
		var totalMarkers = <?=$counter?>;
		var i = 0;
		var infowindow;
		var contentString;
		for (var i = 0; i<totalMarkers; i++){
			
			contentString = '<div class="content">'+
				  '<h1 class="firstHeading">'+markers['m'+i].name+'</h1>'+
				  '<div class="bodyContent">'+
				  '<p>'+markers['m'+i].content+'</p>'+
				  '</div>'+
				  '</div>';
			
			
			infowindow = new google.maps.InfoWindow({
				  content: contentString
			});

			marker['c'+i] = new google.maps.Marker({
					position: new google.maps.LatLng(markers['m'+i].lat,markers['m'+i].lon),
					map: map,
					title: markers['m'+i].name,
					infowindow: infowindow
			  });
			//console.log(markers['m'+i].lat+','+markers['m'+i].lon);
			google.maps.event.addListener(marker['c'+i], 'click', function() {
					for (var key in marker){
						marker[key].infowindow.close();
					}
					this.infowindow.open(map, this);
					
			});
		}

      }
	  function panMap(la,lo){
			map.panTo(new google.maps.LatLng(la,lo));
			
	  }
	  function openMarker(mName){
		  //console.log(marker);
		  for (var key in marker){
			  marker[key].infowindow.close();
		  }
		  for (var key in marker){
			  
			if (marker[key].title.search(mName) != -1){
				marker[key].infowindow.open(map,marker[key]);
			}
		  }
	  }
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
<div id="map-canvas"></div>
  </body>
</html>