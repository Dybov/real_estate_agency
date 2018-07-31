import React, { Component } from 'react';

import {gteSM} from '../devices';
import StickyBox from "react-sticky-box";

import './ResaleDetailed.css'

import SimpleLine from './StickyBoxBottomLines/SimpleLine'
import AreaLine from './StickyBoxBottomLines/AreaLine'
import LengthLine from './StickyBoxBottomLines/LengthLine'

import { Area0digits, Currency0digits } from '../localization/formats'

const ResaleDetailedCurrency = Currency0digits



export default class ResaleDetailed extends Component {
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
                <h3 className="text-center">
                  {<Area0digits value={apartment.total_area} />}
                </h3>
              </div>
              <div className="sticky-top-right col-xs-8">
                <h4><s><ResaleDetailedCurrency value={apartment.full_price} /></s></h4>
                <h3><b><ResaleDetailedCurrency value={apartment.full_price} /></b></h3>
                <p className="text-right"><small>Цена за м²: <ResaleDetailedCurrency value={apartment.price_per_square_meter} /></small></p>
              </div>
            </div>
            <div className="sticky-bottom col-xs-12">
              <SimpleLine l='Район'
                r={apartment.neighbourhood} />
              <SimpleLine l='Материал здания'
                r={apartment.get_building_type_display} />
              <SimpleLine l='Этаж'r={apartment.floor} />
              <SimpleLine l='Год постройки'
                r={apartment.date_of_construction} />
              <LengthLine l='Высота потолка'
                r={apartment.celling_height} />
              <SimpleLine l='Тип ремонта'
                r={apartment.get_interior_decoration_display} />
              <AreaLine l='Площадь кухни'
                r={apartment.kitchen_area} />
              <AreaLine l='Площадь балкона'
                r={apartment.balcony_area} />
              <p className='text-right'>
                <small>Код объекта: {apartment.id}</small>
              </p>
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
