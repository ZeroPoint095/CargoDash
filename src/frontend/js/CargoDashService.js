const httpServerUrl = 'http://localhost:8080';

export const getAllNodes = async () => {
    const response = await fetch(httpServerUrl + '/allnodes');
    return response.json();
}

export const getNode = async (nodeId) => {
    const response = await fetch(httpServerUrl + '/node/' + nodeId,
    {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return response.json();
}

export const getVariable = async (nodeId, varName) => {
    const response = await fetch(
        httpServerUrl + '/node/' + nodeId + '/' + varName);
    return response.json();
}

export const updateVariable = async (nodeId, varName, value) => {
    const response = await fetch(
        httpServerUrl + '/node/' + nodeId + '/' + varName, {
            method: 'POST',
            body: JSON.stringify({value: value})
        }
    );
    return response.json();
}

export const getLoggingBuffer = async () => {
    const response = await fetch(
        httpServerUrl + '/getloggingbuffer');
    return response.json();
}
