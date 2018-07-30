import React, { Component } from 'react';


class StickyBoxBottomLine extends Component {
  render(){
    let {l} = this.props;
    var {r} = this.props;
    if (r===undefined || r===null || r==='') {
      // return null;
      r = '---'
    }
    return(
      <div className='row'>
        <p className='col-xs-7'><b>{l}:</b></p>
        <p className='col-xs-5 text-right'>{r}</p>
      </div>
    )
  }
}

export default StickyBoxBottomLine;