import React, { Component } from 'react';
import { YMaps, Map, Placemark } from 'react-yandex-maps';
import Popup from "reactjs-popup";


class YandexMapPicker extends Component {
  constructor(props){
    super(props);
    this.parseMapCoords = this.parseMapCoords.bind(this);
    this.parsePlacemarkCoords = this.parsePlacemarkCoords.bind(this);
    this.parseInputCoords = this.parseInputCoords.bind(this)
    this.transformCoordsToStr = this.transformCoordsToStr.bind(this);
    this.setCoords = this.setCoords.bind(this);
    this.checkCenter = this.checkCenter.bind(this);

    var coords_str = props.djangowidget.initial_value
    if (coords_str===""){
      /* Tyumen coordinates */
      coords_str = "57.15,65.53"
    }
    let coordinates = this.transformCoordsToArray(coords_str);
    this.state = {
      coordinates,
      coords_str,
      center:coordinates,
      zoom: 15,
    }
  }

  parseMapCoords(e){
    let coordinates = e.get('coords')
    this.setCoords(coordinates)
  }

  parsePlacemarkCoords(e){
    let coordinates = e.originalEvent.target.geometry['_coordinates']
    this.setCoords(coordinates)
  }

  parseInputCoords(e){
    let coords_str = e.target.value
    var coordinates = this.transformCoordsToArray(coords_str)
    this.setCoords(coordinates)
  }

  checkCenter(coordinates){
    var {center} = this.state
    let [y, x] = coordinates
    let [y_c, x_c] = center
    if ((Math.abs(x - x_c) > 0.1)
      || (Math.abs(y - y_c) > 0.1)){
      this.setState({center: coordinates})
    }
  }

  roundArrayCoords(coords){
    return coords.map((val) => {
      return Math.floor(parseFloat(val)*10000)/10000
    })
  }

  transformCoordsToStr(coordinates){
    return coordinates.join(',')
  }

  transformCoordsToArray(coords_str){
    var coords = coords_str.split(',')
    if (coords.length !== 2){
      return [0,0];
    }
    coords = coords.map((val) => {
      if (val === "" || isNaN(val)){
        val = 0
      }
      return val
    })
    coords = this.roundArrayCoords(coords)
    return coords
  }

  setCoords(coordinates){
    var coords_str;
    if (Array.isArray(coordinates)){
      coordinates = this.roundArrayCoords(coordinates)
      coords_str = this.transformCoordsToStr(coordinates)
    } else {
      coords_str = coordinates
      coordinates = this.transformCoordsToArray(coords_str)
    }
    this.checkCenter(coordinates)
    this.setState({coordinates, coords_str})
  }

  render(){
    var {coordinates} = this.state
    var {coords_str} = this.state
    var djangowidget = this.props.djangowidget
    return (
      <div>
        {/* Recreate default django input widget but bound with map */}
        <input
        type={djangowidget.type}
        name={djangowidget.name}
        value={coords_str}
        onChange={this.parseInputCoords}
        {...djangowidget.attrs}/>

        <Popup
          trigger={<button type="button"
            className="">Выбрать на карте</button>}
          modal
          closeOnDocumentClick
          lockScroll
        >
          {close => (
            <YMaps>
              <Map
                state={this.state}
                onClick={this.parseMapCoords}
                width='100%'
              >
                <Placemark
                  geometry={{
                    coordinates,
                  }}
                  options={{
                    iconImageSize: [100, 150],
                    iconImageOffset: [-3, -42],
                    draggable: true,
                    preset: 'islands#violetDotIconWithCaption',
                  }}
                  onDragEnd={this.parsePlacemarkCoords}
                />
              </Map>
            </YMaps>
          )}
        </Popup>
      </div>
    )
  }
}

export default YandexMapPicker;