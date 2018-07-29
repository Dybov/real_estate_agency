import React from 'react';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
import ResaleDetailed from './resale/ResaleDetailed';
import renderReplace from './dom-render-replace';


renderReplace(
  <ResaleDetailed />,
  document.getElementById("sticky-resale")
)

registerServiceWorker();
