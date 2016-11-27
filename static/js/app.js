var styles = [{"featureType":"all","elementType":"all","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":-30}]},{"featureType":"all","elementType":"labels.text.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"color":"#353535"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#656565"}]},{"featureType":"poi","elementType":"geometry.fill","stylers":[{"color":"#505050"}]},{"featureType":"poi","elementType":"geometry.stroke","stylers":[{"color":"#808080"}]},{"featureType":"road","elementType":"geometry","stylers":[{"color":"#454545"}]}];
var map;
var infoWindow;
var markersArr = [];

//        marker = new google.maps.Marker({
//            position: {lat: {# Site.Latitude #}, lng: {# Site.Longitude #} },
//            map: map,
//            icon: {
//              path: google.maps.SymbolPath.CIRCLE,
//              scale: 10,
//              strokeWeight: 2,
//              strokeColor: 'cyan',
//              fillColor: 'cyan',
//              fillOpacity: 0.8
//            },
//            label: {
//               text: '2',
//               color: 'white',
//               fontSize: '12px'
//            }
//        });

function initMap() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 37.0902, lng: -95.7129},
      zoom: 5,
      styles: styles
    });
}

//-------- functions for slider ----------------
function zeroPad(num, places) {
    var zero = places - num.toString().length + 1;
    return Array(+(zero > 0 && zero)).join("0") + num;
}

function formatDT(__dt) {
    var year = __dt.getFullYear();
    var month = zeroPad(__dt.getMonth()+1, 2);
    var date = zeroPad(__dt.getDate(), 2);
    var hours = zeroPad(__dt.getHours(), 2);
    var minutes = zeroPad(__dt.getMinutes(), 2);
    var seconds = zeroPad(__dt.getSeconds(), 2);
    //return hours;
    return year + '-' + month + '-' + date + ' ' + hours + ':' + minutes+ ':' + seconds;
};

function getColor(pm25){
    color = chroma.scale(['LimeGreen', 'yellow'])(pm25 / 50).hex();
    if (pm25 > 50) {
        color = chroma.scale(['yellow','orange'])((pm25 - 50)/ 50).hex();
    }
    if (pm25 > 100) {
        color = chroma.scale(['orange','red'])((pm25 - 100)/ 50).hex();
    }
    if (pm25 > 150) {
        color = chroma.scale(['red','purple'])((pm25 - 150)/ 50).hex();
    }
    if (pm25 > 200) {
        color = chroma.scale(['purple','maroon'])((pm25 - 200)/ 100).hex();
    }
    return color;
/*
    var color = 'cyan';
    if(pm25 < 51){
        color = 'LimeGreen';
    } else if(pm25 >=51 && pm25 < 101){
        color = 'yellow';
    } else if(pm25 >=101 && pm25 < 151){
        color = 'orange';
    }else if(pm25 >=151 && pm25 < 201){
        color = 'red';
    }else if(pm25 >=201 && pm25 < 301){
        color = 'purple';
    }else if(pm25 >= 301){
        color = 'maroon';
    }else{
        color = 'black';
    }
    return color;*/
}


function changeMarker(date){
    $.post('/data', {'date': date.format('MM/DD/YYYY')}, function(rawData) {
        var data = JSON.parse(rawData);

        function addMarker(item, index) {
            var marker;
            var label = item.aqi != -1 ? item.aqi.toString() : "NO DATA";
            if (index >= markersArr.length) {
                marker = new google.maps.Marker({
                    position: {
                        lat: item.lat,
                        lng: item.lng
                    },
                    map: map,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10*(1 + item.aqi/50),
                        strokeWeight: 2,
                        strokeColor: getColor(item.aqi),
                        fillColor: getColor(item.aqi),
                        fillOpacity: 0.8
                    },
                    label: {
                       text: label,
                       color: 'white',
                       fontSize: '12px'
                    }
                });
                markersArr.push(marker);
            } else {
                markersArr[index].setIcon({
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 10*(1 + item.aqi/50),
                    strokeWeight: 2,
                    strokeColor: getColor(item.aqi),
                    fillColor: getColor(item.aqi),
                    fillOpacity: 0.8
                });
                markersArr[index].setLabel({
                    text: label,
                    color: 'white',
                    fontSize: '12px'
                });
                markersArr[index].setMap(map);
            }
        }

        data.forEach(addMarker);
    });

//   {# for Site in Sites #}
//      var site = JSON.parse({#Site.DictJSON|tojson|safe#});
//      pm = site[dateGMTstr];
//      if(pm == -1){
//        pm = "undefined";
//      }
//      console.log(pm);
//      if(typeof(pm) != "undefined"&& pm != "undefined") {
//        markersArr[i].setIcon({
//          path: google.maps.SymbolPath.CIRCLE,
//          scale: 10,
//          strokeWeight: 2,
//          strokeColor: getColor(pm),
//          fillColor: getColor(pm),
//          fillOpacity: 0.8
//        });
//        markersArr[i].setLabel({
//          text: pm.toString(),
//          color: 'white',
//          fontSize: '12px'
//        });
//      }else if(typeof(pm) == "undefined" || pm == "undefined"){
//         markersArr[i].setIcon({
//          path: google.maps.SymbolPath.CIRCLE,
//          scale: 10,
//          strokeWeight: 2,
//          strokeColor: 'black',
//          fillColor: 'black',
//          fillOpacity: 0.8
//        });
//        markersArr[i].setLabel({
//          text: 'NA',
//          color: 'white',
//          fontSize: '12px'
//        });
//      }
//      i = i+1;
//   {# endfor #}
}


function hideAllMarker() {
    function setMapNull(item, index) {
        item.setMap(null);
    }
    markersArr.forEach(setMapNull);
}


function initApp(startTime, endTime) {
    var timeFormat = 'MM/DD/YYYY';
    $("#date-slider").slider({
        //orientation:"vertical",
        min: startTime,
        max: endTime,
        step: 24*60*60*1000,
        slide: function( event, ui ) {
            var date = moment.utc(ui.value);
            $("#date-selection").val(date.format(timeFormat))
            hideAllMarker();
            changeMarker(date);
        }
    });
    var value = $("#date-slider").slider("value");
    $("#date-selection").val(moment.utc(value).format(timeFormat));
    changeMarker(startTime);
}