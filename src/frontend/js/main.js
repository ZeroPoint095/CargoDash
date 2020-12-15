import { getAllNodes, getNode, getVariable, getLoggingBuffer } from './CargoDashService.js';

const createElement = (type, ...attributes) => {
    const element = document.createElement(type);
    for(const attribute of attributes) {
        element.setAttribute(attribute[0], attribute[1]);
    }
    return element;
}


const createDivWithHeader = (parent, text, id, headerType = 'h3') => {
    const div = createElement('div', ['class', 'node-card'], ['id', id]);
    const header = createElement(headerType, ['class', 'node-title']);
    const title = document.createTextNode(text);
    header.appendChild(title);
    div.appendChild(header);
    parent.appendChild(div);
    return div;
}

const createAccordion = (parent) => {
    const accordion = createElement('div', ['class', 'accordion'], ['id', 'accordionExample']);
    parent.appendChild(accordion);
    return accordion;
}

const createAccordionItem = (parent, id, title, table) => {
    const item = createElement('div', ['class', 'accordion-item']);
    const header = createElement('h2', ['class', 'accordion-header']);
    const button = createElement('button', ['class', 'accordion-button'], 
        ['type', 'button'], ['data-bs-toggle', 'collapse'], ['data-bs-target', '#collapse-' + id]
        ,['aria-expanded','true'], ['aria-controls', 'collapse-' + id]);
    const text = document.createTextNode(title);
    button.appendChild(text);
    header.appendChild(button);

    const collapseContainer = createElement('div', ['id', 'collapse-' + id], ['class','accordion-collapse collapse']
        , ['data-bs-parent','#accordionExample']);
    const accordionBody = createElement('div', ['class', 'accordion-body']);
    accordionBody.appendChild(table);
    collapseContainer.appendChild(accordionBody);
    item.appendChild(header);
    item.appendChild(collapseContainer);
    parent.appendChild(item);
}

const createVariablesHeader = (parent, headerType = 'h3') => {
    const header = createElement(headerType, ['class', 'node-title']);
    const title = document.createTextNode('Variables');
    header.appendChild(title);
    parent.appendChild(header);
}

const createHeaderCell = (content, scope) => {
    const th = createElement('th', ['scope', scope]);
    const text = document.createTextNode(content);
    th.appendChild(text);
    return th;
}

const createContentCell = (content) => {
    const td = document.createElement('td');
    const text = document.createTextNode(content);
    td.appendChild(text);
    return td;
}

const createTable = (node, parent = null) => {
    const table = createElement('table', ['class', 'table']);
    
    const thead = document.createElement('thead');
    const theadTr = document.createElement('tr');
    theadTr.appendChild(createHeaderCell('#', 'col'));
    theadTr.appendChild(createHeaderCell('Attribute', 'col'));
    theadTr.appendChild(createHeaderCell('Value', 'col'));
    thead.appendChild(theadTr);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    let index = 1;
    for(const [key, value] of Object.entries(node)) {
        if (key !== 'variables') {
            const tr = document.createElement('tr');
            tr.appendChild(createHeaderCell(index.toString(), 'row'));
            tr.appendChild(createContentCell(key));
            tr.appendChild(createContentCell(value));
            tbody.appendChild(tr);
            index++;
        }
    }
    table.appendChild(tbody);
    if(parent !== null) {
        parent.appendChild(table);
    }
    return table;
}

const createBootstrapContainerWithRow = (parent = null, ...textContent) => {
    const container = createElement('div', ['class', 'container']);

    const row = createElement('row', ['class', 'row']);
    for (const object of textContent) {
        const col = createElement('div', ['class', 'col']);
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
    const link = createElement('a', ['class', 'nav-link'], ['href', '#'+inputText]);
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
        // node table
        createTable(node, div);
        createVariablesHeader(div, 'h4');
        const accordion = createAccordion(div);
        for(const variable of node.variables) {
            const table = createTable(variable);
            createAccordionItem(accordion, Math.random().toString().replace('.',''), variable.node_var_name, table);
        }
    }
});