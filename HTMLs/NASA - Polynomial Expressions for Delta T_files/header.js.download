/* Assigns the right pathname 
var url = document.URL;
var path = '';
/* var urlstart = 0;
 * var urlonemorechar = 2;
 * if (url.indexOf('///') == -1) {
 *    urlstart = url.indexOf('//');
 * }
 * if (url.indexOf('///') != -1) {
 *    urlstart = url.indexOf('///');
 *    urlonemorechar = 3;
 * }
 * var urlend = url.lastIndexOf('/');
 
var urlstart = url.lastIndexOf("eclipse/");
/* Change this whenever the extension changes for the web pages */
// var urlend = url.lastIndexOf(".") + 3;
/*
if (url.lastIndexOf("html") != -1)
   urlend = url.lastIndexOf("html") + 4;
else if (url.lastIndexOf("php") != -1)
   urlend = url.lastIndexOf("php") + 3;

// var urlpath = url.substring(urlstart, urlend);
var urlpath = url.substring(urlstart);
// alert(urlstart + " " + urlend);
if (url.substring(urlstart, urlstart + 8) == 'eclipse/') {
   var urldirs = urlpath.split('/');
   var urlnumdown = urldirs.length - 2;
   while (urlnumdown != 0) {
      path = path + '../';
      urlnumdown --;
   }
}

/* Bryan: Modified the above code and condensed it */
   var path = '';
   var urldirs = document.URL.split('/');
   var urlnumdown = urldirs.length - 2;
   while (urlnumdown != 0) {
      path = path + '../';
      urlnumdown --;
   }

/* Outputs Style Sheets */
document.write('<link rel="stylesheet" type="text/css" href="'+path+'style/main.css" />');
document.write('<link rel="stylesheet" type="text/css" media="screen" href="'+path+'style/nasa-everyone.css" />');
document.write('<link rel="stylesheet" type="text/css" media="screen" href="'+path+'style/nasa-modified.css" />');
document.write('<link rel="stylesheet" type="text/css" media="print" href="'+path+'style/nasa-print.css" />');
document.write('<link rel="stylesheet" type="text/css" media="handheld" href="'+path+'style/nasa-handheld.css" />');
