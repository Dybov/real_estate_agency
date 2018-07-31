import React, { Component } from 'react';
import { FormattedNumber } from 'react-intl';



let areaSuffix = ' м²';
let lengthSuffix = ' м';
let currencySuffix = ' руб';



function setDigits(d){
  return {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  }
}


class SuffixedNumberComponent extends Component{ 
  render(){
    // Add this to avoid errors with empty values
    if (this.props.value === undefined || this.props.value === null){
      return null;
    }

    let {decPlaces} = this.props;
    var additional_props = {};

    if (decPlaces !== undefined && decPlaces !== null){
      additional_props = setDigits(decPlaces);
    }

    return (<span><FormattedNumber {...additional_props} {...this.props}/>{this.props.suffix}</span>)
  }
}


const Area = ({...props}) => (<SuffixedNumberComponent suffix={areaSuffix} {...props}/>)
const Area0digits = ({...props}) =>(<Area decPlaces={0} {...props}/>)
const Area2digits = ({...props}) =>(<Area decPlaces={2} {...props}/>)

const Currency = ({...props}) => (<SuffixedNumberComponent suffix={currencySuffix} {...props}/>)
const Currency0digits = ({...props}) =>(<Currency decPlaces={0} {...props}/>)
const Currency2digits = ({...props}) =>(<Currency decPlaces={2} {...props}/>)

const Length = ({...props}) => (<SuffixedNumberComponent suffix={lengthSuffix} {...props}/>)
const Length0digits = ({...props}) => (<Length decPlaces={0} {...props}/>)
const Length2digits = ({...props}) => (<Length decPlaces={2} {...props}/>)



export {
  Area, Area0digits, Area2digits,
  Currency, Currency0digits, Currency2digits,
  Length, Length0digits, Length2digits,
};
