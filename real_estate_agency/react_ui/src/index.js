import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
import ResaleDetailed from './resale/ResaleDetailed';
import renderReplace from './dom-render-replace';

import ru from 'react-intl/locale-data/ru';
import { IntlProvider, addLocaleData } from 'react-intl';

import YandexMapPicker from './map/yandex-map-picker';



if (window.apartment !== undefined){
	addLocaleData([...ru]);

	var App = () => (
		<IntlProvider locale="ru">
			<ResaleDetailed/>
		</IntlProvider>
	)


	renderReplace(
	  <App />,
	  document.getElementById("sticky-resale")
	)
} else if (window.coordinate_widgets){
	let widgets = window.coordinate_widgets
	Array.prototype.forEach.call(
	  document.getElementsByClassName('coordinate-widget'),
	  function(el, idx) {
	    ReactDOM.render(
	      <YandexMapPicker djangowidget={widgets[idx]}/>,
	      el
	    )
	  }
	)
}
registerServiceWorker();
