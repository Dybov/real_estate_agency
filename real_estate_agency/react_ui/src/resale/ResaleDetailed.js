import React, { Component } from 'react';

import { gteSM } from '../devices';
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

    /* Change string to Date object */
    apartment.date_of_construction = 
      new Date(apartment.date_of_construction);

    const year = apartment.date_of_construction.getFullYear();
    const floor = apartment.floor ? (
        apartment.number_of_storeys ? (
            apartment.floor + ' / ' + apartment.number_of_storeys
          ) : (
            apartment.floor
          )
      ) : (
        null
      )
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
                <h4>
                  {apartment.old_price ? (
                      <s><ResaleDetailedCurrency value={apartment.old_price} /></s>
                    ) : (
                      <br/>
                    )
                  }
                </h4>
                <h3><b><ResaleDetailedCurrency value={apartment.full_price} /></b></h3>
                <p className="text-right"><small>Цена за м²: <ResaleDetailedCurrency value={apartment.price_per_square_meter} /></small></p>
              </div>
            </div>
            <div className="sticky-bottom col-xs-12">
              <SimpleLine l='Район'
                r={apartment.neighbourhood} />
              <SimpleLine l='Материал здания'
                r={apartment.get_building_type_display} />
              <SimpleLine l='Этаж'r={floor} />
              <SimpleLine l='Год постройки'
                r={ year } />
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
          </div>
        </Wrapper>
    )
  }
}
