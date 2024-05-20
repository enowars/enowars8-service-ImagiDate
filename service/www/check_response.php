<?php
session_start();
error_reporting(0);
if (!isset($_SESSION["user_id"])) {
    header("Location: login.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];

    if($username != $_SESSION["username"]){
        echo "You need to provide your actual username, not some random shit";
        exit();
    }

    $api_url = 'http://api:5000/see_my_luck?username=' . $username;
    $ch = curl_init($api_url);
    curl_setopt($ch, CURLOPT_HTTPGET, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    if ($response === false) {
        $show_resp = false;
    } else {
        $show_resp = true;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>check response</title>
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
        <form id="check_form" action="" class="form-signin" method="POST">
            
            <label for="username" class="sr-only">Username</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="Username" maxlength="20" required>
            <button type="submit" class="btn btn-lg btn-primary btn-block">Submit</button>
            <?php if($show_resp): ?>
                <p><?php echo $response ?></p>
            <?php endif; ?>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>