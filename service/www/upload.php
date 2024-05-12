<?php
session_start();

if (!isset($_SESSION["user_id"])) {
    header("Location: login.php");
    exit();
}

$username = $_SESSION["username"];


$upload_dir = "uploads/" . md5($username) . "/";

if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

if ($_FILES["image"]["error"] == UPLOAD_ERR_OK) {

    $destination = $upload_dir . $_FILES["image"]["name"];
    $mime_check = getimagesize($_FILES["image"]["tmp_name"])["mime"];
    if ($mime_check == "image/png" || $mime_check == "image/jpg"){
        if (move_uploaded_file($_FILES["image"]["tmp_name"], $destination)) {
            header("Location: profile.php?id=" . $_SESSION["user_id"]);
            exit();
        } else {
            echo "Error: Failed to move uploaded file.";
            exit();
        }
    } else {
        echo "Error uploading file: Not an Image";
    }
} else {
    echo "Error uploading file: " . $_FILES["image"]["error"];
    exit();
}
?>
