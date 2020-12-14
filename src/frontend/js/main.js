import { getAllNodes, getNode, getVariable, getLoggingBuffer } from './CargoDashService.js';

const createDivWithHeader = (parent, text, id, headerType = 'h3') => {
    const div = document.createElement('div');
    div.className = 'node-card';
    div.setAttribute('id', id);
    const header = document.createElement(headerType);
    header.className = 'node-title';
    const title = document.createTextNode(text);
    header.appendChild(title);
    div.appendChild(header);
    parent.appendChild(div);
    return div;
}

const createBootstrapContainerWithRow = (parent = null, ...textContent) => {
    const container = document.createElement('div');
    container.className = 'container';
    const row = document.createElement('row');
    row.className = 'row';
    for (const object of textContent) {
        const col = document.createElement('div');
        col.className = 'col';
        if(typeof object === 'object' && object !== null) {
            if(Array.isArray(object)) {
                for (const objectpart of object) {
                    if(objectpart.node_var_name !== undefined) {
                        addParagraphWithText(col, objectpart.node_var_name);
                    }
                }
            }
        } else {
            addParagraphWithText(col, object);
        }
        row.appendChild(col);
    }
    container.appendChild(row);
    if(parent != null) {
        parent.appendChild(container);
    }
    return container;
}

const addParagraphWithText = (parent, inputText) => {
    const paragraph = document.createElement('p');
    const text = document.createTextNode(inputText);
    paragraph.appendChild(text);
    parent.appendChild(paragraph); 
}

const addNavbarLink = (parent, inputText) => {
    const link = document.createElement('a');
    link.className = 'nav-link';
    link.setAttribute('href', '#'+inputText);
    const text = document.createTextNode(inputText);
    link.appendChild(text);
    parent.appendChild(link);
}

getAllNodes().then(response => {
    const section = document.getElementById('section');
    const nav = document.getElementById('nav');
    for(let node of response) {
        let div = createDivWithHeader(section, node.name + ' | ' + node.type, node.name);
        addNavbarLink(nav, node.name);
        for (const [key, value] of Object.entries(node)) {
            createBootstrapContainerWithRow(div, key, value);
        }
    }
});