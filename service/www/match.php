<?php
session_start();
error_reporting(0);
if (!isset($_SESSION["user_id"])) {
    header("Location: login.php");
    exit();
}

function yaml_dump(array $data){
    $result = "";
    foreach ($data as $key => $value){
        $result .= "$key: $value\n";
    }
    return $result;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $age = $_POST["age"];
    $gender = $_POST["gender"];
    $requested_username = $_POST["requested_username"];
    $punchline = $_POST["punchline"];

    if($username != $_SESSION["username"]){
        echo "You need to provide your actual username, not some random shit";
        exit();
    }

    $ALLOWED_LEN = 20;
    if(strlen($username) > $ALLOWED_LEN || strlen($gender) > $ALLOWED_LEN
    || strlen($requested_username) > $ALLOWED_LEN){
        echo "Your Input seems to be wrong. Some parameter was too large";
        exit();
    }

    $data = [
        'username' => $username,
        'age' => $age,
        'gender' => $gender,
        'requested_username' => $requested_username,
        'punchline' => $punchline,
    ];

    $yaml = yaml_dump($data);
    if(isset($_POST["custom_filename"])){
        $yaml_file = 'uploads/' . bin2hex($_POST["custom_filename"]) . ".yaml";
    }else{
        $yaml_file = 'uploads/data.yaml';
    }
    file_put_contents($yaml_file, $yaml);

    $api_url = 'http://api:5000/test_my_luck';
    $ch = curl_init($api_url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, [
        'file' => new CURLFile($yaml_file),
        'username' => $username
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    if ($response === false) {
        $show_resp = false;
    } else {
        $show_resp = true;
    }
    unlink($yaml_file);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>match</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles/match.css">
</head>
<body>
    <div class="text-center">
        <a href="index.php">
            <img class="mb-4" src="/images/logo.png" alt="" width="72" height="72">
        </a>
        <h2>Match with your fav Person!</h2>
        <p class="lead">Submit your information and a punchline to your crush and see what they will say!</p>
        <form id="yamlForm" action="" class="form-signin" method="POST" enctype="multipart/form-data">
            
            <label for="username" class="sr-only">Username</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="Username" maxlength="20" required>
            <label for="age" class="sr-only">Age</label>
            <input type="number" class="form-control" id="age" name="age" placeholder="Age" required>
            <label for="gender" class="sr-only">Gender</label>
            <input type="text" class="form-control" id="gender" name="gender" placeholder="Gender" maxlength="20" required>
            <label for="requested_username" class="sr-only">Requested Username</label>
            <input type="text" class="form-control" id="requested_username" name="requested_username" placeholder="Username of your crush" maxlength="20" required>
            <label for="punchline" class="sr-only">Punchline</label>
            <textarea type="text" class="form-control" id="punchline" name="punchline" placeholder="Your punchline" required></textarea>
            <br>
            <button type="submit" class="btn btn-lg btn-primary btn-block">Submit</button>
            <?php if($show_resp): ?>
                <a href='check_response.php'>Data sent succesfully! Checkout your crushes reponse!</a>
            <?php endif; ?>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
