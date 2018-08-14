import React from 'react';
import SimpleLine from './SimpleLine'
import { Currency0digits } from '../../localization/formats'


export default class CurrencyLine extends SimpleLine {
	constructor(props){
		super(props)
		this.WrappedComponent = <Currency0digits value={props.r} />
	}
}
