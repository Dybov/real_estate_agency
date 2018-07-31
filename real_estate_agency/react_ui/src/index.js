import React from 'react';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
import ResaleDetailed from './resale/ResaleDetailed';
import renderReplace from './dom-render-replace';

import ru from 'react-intl/locale-data/ru';
import { IntlProvider, addLocaleData } from 'react-intl';

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

registerServiceWorker();
