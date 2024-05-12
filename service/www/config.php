<?php
define('DB_SERVER', 'db');
define('DB_USERNAME', 'date');
define('DB_PASSWORD', 'somepassword');
define('DB_DATABASE', 'date');


$conn = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
