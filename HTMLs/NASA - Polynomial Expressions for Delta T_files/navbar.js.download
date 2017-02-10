/* Assigns the right pathname *
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

/* Clears the search bar once done */
function searchclear() {
   document.search.nasaInclude.value = '';
}

/* NASA headers */
document.write('<div id="nasahead">');
document.write('<a href="http://www.nasa.gov/" target="_blank"><img src="'+path+'image/nasa-header-logo.gif" alt="NASA Logo, National Aeronautics and Space Administration" width="300" height="65" /></a>');
document.write('<div class="hidden"><a href="#skipping" title="Skip Navigation" accesskey="2">Skip Navigation (press 2)</a></div>');
document.write('<div id="nasaheadlinks">');
document.write('<ul>');
document.write('<li><a href="http://www.nasa.gov/" target="_blank">+ NASA Portal</a></li>');
document.write('<li><a href="http://sunearthday.nasa.gov/" target="_blank">+ Sun-Earth Day</a></li>');
document.write('<li><a href="'+path+'SEpubs/bulletin.html">+ Eclipse Bulletins</a></li>');
var ohdate = new Date();
var ohyear = ohdate.getFullYear();
document.write('<li><a href="'+path+'OH/OH'+ohyear+'.html">+ Eclipses During '+ohyear+'</a></li>');
document.write('</ul>');
document.write('</div>');
/* deleted 2013Oct18 by Robert Candey
document.write('<div id="searchbox">');
var searchtitle = "Find It @ NASA:";
searchtitle = searchtitle.toUpperCase();
document.write('<h3 class="nasa">'+searchtitle+'</h3>');
document.write('<form name="search" id="search" method="get" action="http://search.nasa.gov/nasasearch/search/search.jsp">');
document.write('<input type="text" name="nasaInclude" size="15" title="searchfield" value="Keywords" style="font-size: 11px; position: absolute; top: 25px; left: 0px;" onclick="searchclear();" />');
document.write('<input type="image" src="'+path+'image/nasa-button-go.gif" alt="Query" style="position: absolute; left: 115px; top: 24px;" class="submitit" />');
document.write('</form>');
document.write('</div>');
 */
document.write('</div>');

/* Navigation Bar Links - only change these six variables below; and modify nasa-modified.css to update the size of each box; and also modify eclipse.html so the right  */
var one = new Array("Home","eclipse.html");
var two = new Array("Solar Eclipses","solar.html");
var three = new Array("Lunar Eclipses","lunar.html");
var four = new Array("Transits","transit/transit.html");
// var five = new Array("12-Yr Ephemeris","TYPE/TYPE.html");
// var five = new Array("Moon Phases","phase/phase2001gmt.html");
// var five = new Array("Sky Events","SKYCAL/SKYCAL.html");
var solar = one[0].toUpperCase();
var lunar = two[0].toUpperCase();
var resc = three[0].toUpperCase();
var tran = four[0].toUpperCase();
// var ephm = five[0].toUpperCase();
// var moon = six[0].toUpperCase();
document.write('<div id="menu">');
document.write('<ul>');
document.write('<li class="one"><a href="'+path+one[1]+'"><span>'+solar+'</span></a></li>');
document.write('<li class="two"><a href="'+path+two[1]+'"><span>'+lunar+'</span></a></li>');
document.write('<li class="three"><a href="'+path+three[1]+'"><span>'+resc+'</span></a></li>');
document.write('<li class="four"><a href="'+path+four[1]+'"><span>'+tran+'</span></a></li>');
// document.write('<li class="five"><a href="'+path+five[1]+'"><span>'+ephm+'</span></a></li>');
// document.write('<li class="six"><a href="'+path+six[1]+'"><span>'+moon+'</span></a></li>');
document.write('</ul>');
document.write('</div>');
document.write('<div id="headimage">');
document.write('<a href="'+path+'eclipse.html"><img id="eclipsebanner" src="'+path+'image/bannerEclipse2008.jpg" lowres="'+path+'image/bannerEclipseLowRes.gif" alt="NASA Eclipse Web Site" /></a>');
document.write('</div>');
document.write('<div class="clear"></div>');
document.write('<div id="contentwrapper">');
document.write('<div id="singlecolumn">');
/* var str=("Hello JavaScripters!")
 * document.write(str.toLowerCase())
 * document.write("<br>")
 * document.write(str.toUpperCase())
 */
