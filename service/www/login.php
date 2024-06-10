<?php
session_start();
error_reporting(0);
require_once 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    $stmt = $conn->prepare("SELECT id, username, password FROM users WHERE username = ?");
    $stmt->bind_param('s', $username);
    $stmt->execute();
    $stmt->bind_result($user_id, $db_username, $db_password);

    if ($stmt->fetch()) {
        if (password_verify($password, $db_password)) {
            $_SESSION['user_id'] = $user_id;
            $_SESSION['username'] = $db_username;
            header("Location: profile.php?id=" . $user_id);
            exit();
        } else {
            echo "Incorrect password";
        }
    } else {
        echo "User not found";
    }
    $stmt->close();
    $conn->close();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <link href="styles/login.css" rel="stylesheet">
    <style>
        #heart {
            animation: 1.5s ease 0s infinite beat;
        }

        @keyframes beat {

            0%,
            50%,
            100% {
                transform: scale(1, 1);
            }

            30%,
            80% {
                transform: scale(0.92, 0.95);
            }
        }
    </style>
</head>

<body class="text-center">
    <form class="form-signin" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
        <a href="index.php">
            <img class="mb-4" src="/images/logo.png" id="heart" alt="" width="72" height="72">
        </a>
        <h1 class="h3 mb-3 font-weight-normal">Login</h1>
        <label for="username" class="sr-only">Username</label>
        <input type="text" id="username" name="username" class="form-control" placeholder="Username" required autofocus>
        <label for="password" class="sr-only">Password</label>
        <input type="password" id="password" name="password" class="form-control" placeholder="Password" required>
        <a href="register.php" class="registration-link">Don't have an account? Register here.</a><br>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
    </form>
</body>

</html>