import React, {Component} from 'react';


class BaseModal extends Component {
  render(){
  	const backdropStyle = {
      position: 'fixed',
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
      backgroundColor: 'rgba(0,0,0,0.3)',
      padding: 50
    };
  	return <div className="backdrop" style={backdropStyle}>
  		<div className='loader-50-50'></div>
	</div>;
  }
}

export default BaseModal
