import React from 'react';
import SimpleLine from './SimpleLine'
import { Area0digits } from '../../localization/formats'


export default class AreaLine extends SimpleLine {
	constructor(props){
		super(props)
		this.WrappedComponent = <Area0digits value={props.r} />
	}
}
