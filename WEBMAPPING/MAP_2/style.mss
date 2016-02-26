Map {
  background-color: #147169;
}

#countries {
  ::outline {
    line-color: #2e756e;
    line-width: 2;
    line-comp-op: overlay;
    line-join: round;
  }
  [SOVEREIGNT = 'United States of America']
  		{polygon-fill: #b6fcfb}
}

#states {
  line-color:#b6fcfb;
  line-width:1.5;
  line-dasharray: 10, 4;
  polygon-opacity:1;
  polygon-fill:#000000;
}

#us_parks_area {
  line-color:#a0d417;
  line-width:4.0;
  polygon-opacity:1;
  polygon-fill:#1f4f07;
}

#us_parks_area {
  text-name: [Unit_Name];
  text-face-name: 'Helvetica Bold';
  text-fill: #3c4e61;
  text-size: 12;
  text-halo-fill: fadeout(white, 30%);
  text-halo-radius: 2.5
}

#urban_areas {
  line-color:#fff216;
  line-width: 3;
  polygon-comp-op: minus;
}
	
#populated_places [zoom >= 5]{
  marker-fill:#f45;
  marker-line-color:#813;
  marker-allow-overlap:true;
  marker-width:6;
  [zoom >= 5]{marker-width: 10}
  	[MEGACITY = 0]{marker-width: 5}
  	[MEGACITY = 1]{marker-width: 20}
}


#10mroads {
  	[zoom >= 6] 
    	{line-width:0.5}
  		line-color:#ddc0eb;
  	[zoom < 6]
    	{line-width:0}
  		line-color:#ddc0eb;
}
