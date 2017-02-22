/* Path Confirmer (same as before) *
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
 *
var urlstart = url.lastIndexOf("eclipse/");
/* Change this whenever the extension changes for the web pages *
var urlend = url.lastIndexOf("html") + 4;
var urlpath = url.substring(urlstart, urlend);
if (url.substring(urlstart, urlstart + 8) == 'eclipse/') {
   var urldirs = urlpath.split('/');
   var urlnumdown = urldirs.length - 2;
   while (urlnumdown != 0) {
      path = path + '../';
      urlnumdown --;
   }
}
*/

/* Bottom Navigation Bar (not the same code) */
var one = new Array("Home","eclipse.html");
var two = new Array("Solar Eclipses","solar.html");
var three = new Array("Lunar Eclipses","lunar.html");
var four = new Array("Transits","transit/transit.html");
var five = new Array("Resources","resource.html");
/* var gtps = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"; // if you use the goto list icon */
var gtps = '';
var solar = gtps+one[0];
var lunar = gtps+two[0];
var resc = gtps+three[0];
var tran = gtps+four[0];
var ephm = gtps+five[0];
document.write('<div id="footmenu">');
document.write('<ul>');
document.write('<li class="one"><a href="'+path+one[1]+'"><span>'+solar+'</span></a></li>');
document.write('<li class="two"><a href="'+path+two[1]+'"><span>'+lunar+'</span></a></li>');
document.write('<li class="three"><a href="'+path+three[1]+'"><span>'+resc+'</span></a></li>');
document.write('<li class="four"><a href="'+path+four[1]+'"><span>'+tran+'</span></a></li>');
document.write('<li class="five"><a href="'+path+five[1]+'"><span>'+ephm+'</span></a></li>');
document.write('</ul>');
document.write('</div>');

/* Last Updated Script */
var mdate = new Date (document.lastModified);
var mo = "Month";
if (mdate.getMonth()==1-1) {
   mo = "January";
}
if (mdate.getMonth()==2-1) {
   mo = "February";
}
if (mdate.getMonth()==3-1) {
   mo = "March";
}
if (mdate.getMonth()==4-1) {
   mo = "April";
}
if (mdate.getMonth()==5-1) {
   mo = "May";
}
if (mdate.getMonth()==6-1) {
   mo = "June";
}
if (mdate.getMonth()==7-1) {
   mo = "July";
}
if (mdate.getMonth()==8-1) {
   mo = "August";
}
if (mdate.getMonth()==9-1) {
   mo = "September";
}
if (mdate.getMonth()==10-1) {
   mo = "October";
}
if (mdate.getMonth()==11-1) {
   mo = "November";
}
if (mdate.getMonth()==12-1) {
   mo = "December";
}
var utdate = mdate.getFullYear() + " " + mo + " " + mdate.getDate();

/* NASA Footer */
document.write('<div id="nasafoot">');
document.write('   <div id="nasafootplus">');
document.write('   <ul class="smallfoot">');
/* 
document.write('      <li>Website Manager: <a href="mailto:Robert.M.Candey@nasa.gov">Robert.M.Candey@nasa.gov</a></li>');
document.write('      <li>Responsible NASA Official: <a href="mailto:c.a.young@nasa.gov">Alex Young</a></li>');
*/
document.write('      <li>+ Heliophysics Science Division, Code 670</a><br />');
document.write('      NASA Goddard Space Flight Center<br />Greenbelt, MD 20771, USA</li>');
document.write('      <li>+ <a href="http://www.nasa.gov/about/highlights/HP_Privacy.html" target="Privacy">Privacy Policy and Important Notices</a></li>');
document.write('   </ul>');
document.write('   </div>');
document.write('   <a href="http://www.nasa.gov/" target="_blank"><img id="nasafootr" src="'+path+'image/nasa-foot-nasa.gif" width="51" height="48" alt="NASA Logo - nasa.gov" /></a>');
document.write('');
document.write('   <div id="nasafootlinks">');
document.write('   <ul class="smallfoot">');
document.write('      <li>Website Manager: <a href="mailto:Robert.M.Candey@nasa.gov">Robert.M.Candey@nasa.gov</a></li>');
document.write('      <li>Responsible NASA Official: <a href="mailto:c.a.young@nasa.gov">Alex Young</a></li>');
document.write('      <li>Last Updated: ');
