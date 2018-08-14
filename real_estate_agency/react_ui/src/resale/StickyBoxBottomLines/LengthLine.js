import React from 'react';
import SimpleLine from './SimpleLine'
import { Length0digits } from '../../localization/formats'


export default class LengthLine extends SimpleLine {
	constructor(props){
		super(props)
		this.WrappedComponent = <Length0digits value={props.r} />
	}
}
