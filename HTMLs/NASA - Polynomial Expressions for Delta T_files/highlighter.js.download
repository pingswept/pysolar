var filename = document.URL;
var filenames = filename.split('/');
var tagaugment = '';
var taglength = filenames.length - 1;
if (filenames[taglength] == 'eclipse.html') {
   tagaugment = 'oneon';
}
if (filenames[taglength] == 'solar.html') {
   tagaugment = 'twoon';
}
if (filenames[taglength] == 'lunar.html') {
   tagaugment = 'threeon';
}
if (filenames[taglength] == 'transit.html') {
   tagaugment = 'fouron';
}
if (filenames[taglength] == 'TYPE.html') {
   tagaugment = 'fiveon';
}
if (filenames[taglength] == 'phase2001gmt.html') {
   tagaugment = 'sixon';
}

var txttable = document.getElementById('widetxt');

if (txttable != null) { // could use txttable.innerHTML
   document.write('<div id="paperw'+tagaugment+'">');
}
else {
   document.write('<div id="paper'+tagaugment+'">');
}