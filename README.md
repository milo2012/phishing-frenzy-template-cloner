# phishing-frenzy-template-cloner   
   
The script genTemplate-nopwd.py is useful if you are interested in generating a phishing frenzy template that fingerprints the browser plugins and sent back these data back to phishing frenzy server.      
```
$ python genTemplate-nopwd.py -c http://edition.cnn.com -u phishingfrenzydomain -i fakedomain.com
- Cloning website: http://edition.cnn.com
- Generated data.html, index.php and index2.php
- Generated attachments.yml and template.yml
- Creating archive
- Generated zip file: template.zip
- You can now import the file in Phishing Frenzy under Templates > Restore
```
