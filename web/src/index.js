import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

//ReactDOM.render(<App />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
//serviceWorker.unregister();

window.React = React

const task = window.task
const innerHTML = htmlDecode(document.getElementById('root').innerHTML)


ReactDOM.render(<App
        innerHTML={innerHTML}/>, document.getElementById('root'));



function htmlDecode(input){
    try {
        let e = document.createElement('div');
        e.innerHTML = input;
        return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
    } catch (err) {
        return input
    }
}