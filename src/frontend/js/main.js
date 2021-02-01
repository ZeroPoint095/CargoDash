import { getAllNodes, getNode, getVariable, getLoggingBuffer } from './CargoDashService.js';

// Start: Helper methods

let stopUpdating = false;

const createElement = (type, ...attributes) => {
    // Create HTML Element
    const element = document.createElement(type);
    for(const attribute of attributes) {
        element.setAttribute(attribute[0], attribute[1]);
    }
    return element;
}

const createIdSafeString = (...strings) => {
    // Function that creates safe HTML ID's
    let ErrorThrown = false;
    const newStringList = [];
    for(let string of strings) {
        if(typeof string !== 'string') {
            ErrorThrown = true;
            throw new Error(string, 'is not a String!');
        } else {
            newStringList.push(string.replace(/ /g, '_'));
        }
    }
    if(ErrorThrown) {
        return 'incorrect-id';
    } else {
        return newStringList.join('-');
    }
}

const createElementWithText = (parent, text, ElementType = 'h3', ...attributes) => {
    // Creates HTML Element with a text inside
    const element = createElement(ElementType, ...attributes);
    const title = document.createTextNode(text);
    element.appendChild(title);
    if(parent != null) {
        parent.appendChild(element);
    }
    return element;
}

const createDivWithHeader = (parent, text, id, headerType = 'h3') => {
    // Creates HTML Div with a header
    const div = createElement('div', ['class', 'node-card'], ['id', id]);
    createElementWithText(div, text, headerType);
    parent.appendChild(div);
    return div;
}

// End: Helper methods

const createAccordion = (parent) => {
    // Creates Bootstrap accordion
    // The accordion is tab-based element.
    const accordion = createElement('div', ['class', 'accordion'], ['id', 'accordionExample']);
    parent.appendChild(accordion);
    return accordion;
}

const createAccordionItem = (parent, id, title, table) => {
    // Creates a tab for the accordion
    const item = createElement('div', ['class', 'accordion-item']);
    const header = createElement('h2', ['class', 'accordion-header']);
    const button = createElement('button', ['class', 'accordion-button'], 
        ['type', 'button'], ['data-bs-toggle', 'collapse'], ['data-bs-target', '#collapse-' + id]
        ,['aria-expanded','true'], ['aria-controls', 'collapse-' + id], ['id', 'id-' + id]);
    
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

const createTable = (object, objectName = '', parent = null) => {
    // Creates Table that has information of node/variable
    const table = createElement('table', ['class', 'table']);
    
    const thead = document.createElement('thead');
    const theadTr = document.createElement('tr');
    theadTr.appendChild(createElementWithText(null, '#', 'th', ['scope', 'col']));
    theadTr.appendChild(createElementWithText(null, 'Attribute', 'th', ['scope', 'col']));
    theadTr.appendChild(createElementWithText(null, 'Value', 'th', ['scope', 'col']));
    thead.appendChild(theadTr);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    let index = 1;
    for(const [key, value] of Object.entries(object)) {
        if (key !== 'variables') {
            const tr = document.createElement('tr');
            tr.appendChild(createElementWithText(null, index.toString(), 'th', ['scope', 'row']));
            tr.appendChild(createElementWithText(null, key, 'td'));
            tr.appendChild(createElementWithText(null, value, 'td', ['id', createIdSafeString(objectName, key)]));
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

const addNavbarLink = (parent, inputText) => {
    // Adds link to the navbar
    const link = createElement('a', ['class', 'nav-link'], ['href', '#'+inputText]);
    const text = document.createTextNode(inputText);
    link.appendChild(text);
    parent.appendChild(link);
}

const updateGraph = () => {
    // Function that is able to cancel the updating of the graphs
    // This function is requested from the 'Stop Updating Graps' button
    const button = document.getElementById('updateGraphButton');
    if(!stopUpdating){
        button.classList.remove('btn-danger');
        button.classList.add('btn-success');
        button.innerHTML = 'Continue Updating Graphs';
    } else {
        button.classList.remove('btn-success');
        button.classList.add('btn-danger');
        button.innerHTML = 'Stop Updating Graphs';
    }
    stopUpdating = !stopUpdating;
};

let varValues = {};
let varGraphs = {};

const updateNodeVariableValues = () => {
    // Function for updating the values
    getAllNodes().then(response => {
        for(const node of response) {
            for(const variable of node.variables) {
                // Location where value can been seen in html-file
                let varValue = document.getElementById(createIdSafeString(variable.node_var_name, 'value'));
                // Current value
                varValue.innerHTML = variable.value;
                // Searches for unique value list
                const uniqueValueList = varValues[createIdSafeString(variable.node_name+variable.node_var_name)];
                
                if(uniqueValueList.length === 0) {
                    uniqueValueList.push([new Date(), variable.value]);
                } else {
                    // check if value is new
                    if(uniqueValueList[uniqueValueList.length-1][1] !== variable.value) {
                        // update valueList
                        uniqueValueList.push([new Date(), variable.value]);
                        // Check if graph initialized
                        if(varGraphs[createIdSafeString(variable.node_name+variable.node_var_name)] == undefined) {
                            // initializes graph
                            varGraphs[createIdSafeString(variable.node_name+variable.node_var_name)] = 
                            new Dygraph(document.getElementById('div_g-' + createIdSafeString(variable.node_name+variable.node_var_name)),
                            varValues[createIdSafeString(variable.node_name+variable.node_var_name)], {
                                drawPoints: true,
                                showRangeSelector: true,
                                valueRange: [null, null],
                                labels: ['Time', 'Value']
                            });
                        }
                        
                        if(varGraphs[createIdSafeString(variable.node_name+variable.node_var_name)] != undefined && !stopUpdating) {
                            // if not showing then stop updating
                            varGraphs[createIdSafeString(variable.node_name+variable.node_var_name)].updateOptions( 
                                { 'file': uniqueValueList} );
                        }
                    }
                }
            }
        }
    });
}

getAllNodes().then(response => {
    const section = document.getElementById('section');
    const nav = document.getElementById('nav');
    const row = createElement('div', ['class', 'row justify-content-center']);
    for(let node of response) {
        createElementWithText(section, 'Stop Updating Graphs', 'button', ['id', 'updateGraphButton'] , ['type','button'], 
            ['class','btn btn-danger mx-3 mt-3']);
        // Initialises Graphs
        for(const variable of node.variables) {
            let variableDiv = createElement('div', ['class', 'col-4 m-5',], ['style','background-color:white;']);
            createElementWithText(variableDiv, node.name + ' | ' + variable.node_var_name, 'h6',['class', 'm-2']);
            
            const graph = createElement('div', ['id','div_g-'+ createIdSafeString(variable.node_name+variable.node_var_name)],
                                        ['style','width:initial;']);
            variableDiv.appendChild(graph);

            row.appendChild(variableDiv);
        }
        section.appendChild(row);

        // Initialises Detailed Tables
        let div = createDivWithHeader(section, node.name + ' | ' + node.type, node.name);
        addNavbarLink(nav, node.name);
        // node table
        createTable(node, node.name, div);
        createElementWithText(div, 'Variables', 'h4', ['class', 'node-title']);
        const accordion = createAccordion(div);
        for(const variable of node.variables) {
            const table = createTable(variable, variable.node_var_name);
            createAccordionItem(accordion, createIdSafeString(variable.node_name+variable.node_var_name), variable.node_var_name, table);
            // Creates a unique list inside the varValues object
            // This list can be retrieved to make graphs.
            varValues[createIdSafeString(variable.node_name+variable.node_var_name)] = [];
        }
        document.getElementById('updateGraphButton').addEventListener('click', updateGraph, false);
    }
});

// Graphs updates every second
setInterval(() => updateNodeVariableValues(), 1000);
