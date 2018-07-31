import React, { Component } from 'react';


export default class SimpleLine extends Component {
  constructor(props){
    super(props)
    this.show = true;
    let r = props.r;
    if (r===undefined || r===null || r===''){
      this.show = false;
      this.r = '---'
    }

  }
  render(){
    let {l} = this.props;
    let {r} = this.props;
    var WrappedComponent = r;
    if (this.show===false) {
      return null;
    } else if (this.WrappedComponent !== null && this.WrappedComponent !== undefined){
      WrappedComponent = this.WrappedComponent
    }
    return(
      <div className='row'>
        <p className='col-xs-7'><b>{l}:</b></p>
        <p className='col-xs-5 text-right'>{WrappedComponent}</p>
      </div>
    )
  }
}
