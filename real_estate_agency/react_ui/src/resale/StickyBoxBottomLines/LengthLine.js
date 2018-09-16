import React from 'react';
import SimpleLine from './SimpleLine'
import { Length } from '../../localization/formats'


export default class LengthLine extends SimpleLine {
	constructor(props){
		super(props)
		this.WrappedComponent = <Length value={props.r} decPlaces={1} />
	}
}
