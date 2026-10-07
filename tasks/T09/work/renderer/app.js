const api = (fn) => window.editorApi[fn]()
window.editorApi = window.editorApi || {}
window.saveHtml = async () => document.getElementById('ed').innerHTML
