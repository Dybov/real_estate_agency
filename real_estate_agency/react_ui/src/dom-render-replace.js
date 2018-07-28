import ReactDOM from 'react-dom';


/**
 * render Component not inside but instead of DOM element, keeping DOM element attrs
 *
 * While the default ReactDOM.render put your component
 * inside <div id="root" class="someclass"></div>
 * and it become: 
 * <body>
 *   <div id="root" class="someclass">
 *     <yourcomponentwrapper class="otherclass">content</yourcomponentwrapper>
 *   </div>
 * </body>
 * instead of it the renderReplace function make:
 * <body>
 *   <yourcomponentwrapper id="root" class="someclass">
 *     content
 *   </yourcomponentwrapper>
 * </body>
 * Note that the inital attrs of yourcomponentwrapper will be removed
 * 
 * @since      0.0.1
 *
 * @param {class}  Component     Component, which content need to put inside DOM element
 * @param {object} DOMElement    DOM elemenet which content must be replaced with Component's content.
 * 
 * @return {void}
 */
function renderReplace(component, dom_element) {
  let temp = document.createElement("div");
  ReactDOM.render(component, temp);

  let container = dom_element.parentNode;
  let target = temp.childNodes[0];

  for (let index = dom_element.attributes.length - 1; index > -1; -- index) {
    let attribute = dom_element.attributes[index];
    target.setAttribute(attribute.name, attribute.value);
  }

  container.replaceChild(target,
    dom_element);
}

export default renderReplace;