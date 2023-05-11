* `index.html` and `script.js` is front-end which uses JQuery to make a REST POST
    * passes data
* POST goes to the instance containing `flack.py` and `makeGraph.py`
    * **NEED TO FILL IN URL OF INSTANCE IN `script.py`**
* `flack.py` calls `makeGraph.py` to make graph with data
* passes graph back to `script.js` to display
