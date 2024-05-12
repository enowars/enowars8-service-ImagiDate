<?php
require_once 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!empty($_POST["username"]) && !empty($_POST["password"]) && 
    !empty($_POST["confirm_password"]) && !empty($_POST["age"]) && 
    !empty($_POST["gender"])) {

        if ($_POST["password"] !== $_POST["confirm_password"]) {
            echo "Password and confirm password do not match.";
            exit();
        }

        $check_stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
        $check_stmt->bind_param("s", $_POST["username"]);
        $check_stmt->execute();
        $check_result = $check_stmt->get_result();
        if ($check_result->num_rows > 0) {
            echo "Username already exists. Please choose a different username.";
        } else {
            $insert_stmt = $conn->prepare("INSERT INTO users (username, password, age, gender) VALUES (?, ?, ?, ?)");
            $insert_stmt->bind_param("ssis", $username, $password, $age, $gender);

            $username = $_POST["username"];
            $password = password_hash($_POST["password"], PASSWORD_DEFAULT);
            $age = intval($_POST["age"]);
            $gender = $_POST["gender"];
            if ($insert_stmt->execute()) {
                echo "Registration successful. <a href='login.php'>Go to login</a>";
            } else {
                echo "Error: " . $insert_stmt->error;
            }

            $insert_stmt->close();
        }
        $check_stmt->close();
        $conn->close();
    } else {
        echo "All fields are required.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <link rel="stylesheet" href="styles/register.css">
    <title>User Registration</title>
</head>
<body class="text-center">
    <form class="form-signup" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
        <a href="index.php">
            <img class="mb-4" src="/images/logo.png" alt="" width="72" height="72">
        </a>
        <h1 class="h3 mb-3 font-weight-normal">Register</h1>
        <label for="username" class="sr-only">Username</label>
        <input type="text" id="username" name="username" class="form-control" placeholder="Username" required autofocus>
        <label for="password" class="sr-only">Password</label>
        <input type="password" id="password" name="password" class="form-control" placeholder="Password" required>
        <label for="confirm_password" class="sr-only">Confirm Password</label>
        <input type="confirm_password" id="confirm_password" name="confirm_password" class="form-control" placeholder="Confirm Password" required>
        <label for="confirm_password" class="sr-only">Age</label>
        <input type="number" id="age" name="age" class="form-control" placeholder="Age" required>
        <select id="gender" name="gender" class="form-control">
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select>
        <a href="login.php" class="login-link">Got an account? Login here.</a>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
    </form>
</body>
</html>