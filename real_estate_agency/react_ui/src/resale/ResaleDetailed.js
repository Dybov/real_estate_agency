import React, { Component } from 'react';

import {gteSM} from '../devices';
import StickyBox from "react-sticky-box";

import './ResaleDetailed.css'

import StickyBoxBottomLine from './StickyBoxBottomLine'


class ResaleDetailed extends Component {
  render() {
    var Wrapper = 'div'
    if (gteSM()) {
      Wrapper = StickyBox
    }
    const apartment = window.apartment;
    return (
        <Wrapper>
          <div className="shadow">
            <div className="sticky-top col-xs-12">
              <div className="sticky-top-left col-xs-4">
                <h3 className="text-center">{Math.floor(apartment.total_area)} м²</h3>
              </div>
              <div className="sticky-top-right col-xs-8">
                <h4><s>{apartment.full_price} руб</s></h4>
                <h3><b>{apartment.full_price} руб</b></h3>
                <p className="text-right"><small>Цена за м²: { Math.round(apartment.price_per_square_meter)} руб</small></p>
              </div>
            </div>
            <div className="sticky-bottom col-xs-12">
              <StickyBoxBottomLine l='Район'
                r={apartment.neighbourhood} />
              <StickyBoxBottomLine l='Материал здания'
                r={apartment.get_building_type_display} />
              <StickyBoxBottomLine l='Этаж'r={apartment.floor} />
              <StickyBoxBottomLine l='Год постройки'
                r={apartment.date_of_construction} />
              <StickyBoxBottomLine l='Высота потолка'
                r={apartment.celling_height} />
              <StickyBoxBottomLine l='Тип ремонта'
                r={apartment.get_interior_decoration_display} />
              <StickyBoxBottomLine l='Площадь кухни'
                r={apartment.kitchen_area} />
              <StickyBoxBottomLine l='Площадь балкона'
                r={apartment.balcony_area} />
              <p className='text-right'><small>Код объекта: {apartment.id}</small></p>
            </div>
            <a href="" className='callback-link callback'>
              <button className='btn btn-block btn-primary'>
                Записаться на просмотр
              </button>
            </a>
            {/*<a href="" className="realty_home_page_characteristics-bottom">Записаться на просмотр</a>*/}
          </div>
        </Wrapper>
    )
  }
}

export default ResaleDetailed;
