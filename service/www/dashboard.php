<?php #TODO ?>
<?php
session_start();
require_once 'config.php';

if (isset($_SESSION["user_id"])) {
    $logged_in = true;
    $user_id = $_SESSION["user_id"];
} else {
    $logged_in = false;
}

function getAllUserProfiles($conn) {
    $query = "SELECT * FROM users";
    $result = $conn->query($query);
    return $result->fetch_all();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImagiDate</title>
</head>
<body>

<?php if ($logged_in): ?>
    <div>
        <button onclick="window.location.href='profile.php?id=<?php echo $user_id; ?>'">Profile</button>
        <a href="logout.php">Logout</a>
    </div>
<?php else: ?>
    <div>
        <button onclick="window.location.href='login.php'">Login</button>
        <button onclick="window.location.href='register.php'">Register</button>
    </div>
<?php endif; ?>

<?php if ($logged_in): ?>
    <h2>Dashboard</h2>
    <ul>
        <?php $profiles = getAllUserProfiles($conn);
        foreach ($profiles as $profile): ?>
            <li><a href="profile.php?id=<?php echo $profile[0]; ?>"><?php echo $profile[1]; ?></a></li>
        <?php endforeach; ?>
    </ul>
<?php endif; ?>

</body>
</html>