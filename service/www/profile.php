<?php
session_start();
require_once "config.php";

if (!isset($_SESSION["user_id"])) {
    header("Location: login.php");
    exit();
}
$user_id = $_SESSION["user_id"];

if (!isset($_GET["id"])) {
    echo "User ID not provided.";
    exit();
}

$url_user_id = $_GET["id"];


$stmt = $conn->prepare("SELECT username FROM users WHERE id = ?");
$stmt->bind_param('i', $_GET["id"]);
$stmt->execute();
$stmt->bind_result($db_username);
if ($stmt->fetch()) {
    $username = $db_username;
} else {
    echo "User does not exist";
    exit();
}
$stmt->close();
$can_view_private_comments = ($user_id == $url_user_id);

$public_comments = array();
$private_comments = array();


$stmt = $conn->prepare("SELECT comment_text FROM comments WHERE user_id = ? AND is_public = 1");
$stmt->bind_param("i", $url_user_id);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $public_comments[] = $row["comment_text"];
}
$stmt->close();

$stmt = $conn->prepare("SELECT comment_text FROM comments WHERE user_id = ? AND is_public = 0");
$stmt->bind_param("i", $url_user_id);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $private_comments[] = $row["comment_text"];
}
$stmt->close();

function displayComments($comments)
{
    if (!empty($comments)) {
        foreach ($comments as $comment) {
            echo "<li>" . htmlspecialchars($comment) . "</li>";
        }
    } else {
        echo "<li>No comments yet.</li>";
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST["comment_text"])) {
        $comment_text = $_POST["comment_text"];
        $is_public = isset($_POST["is_public"]) ? 1 : 0;

        $stmt = $conn->prepare("INSERT INTO comments (user_id, comment_text, is_public) VALUES (?, ?, ?)");
        $stmt->bind_param("iss", $user_id, $comment_text, $is_public);
        if ($stmt->execute()) {
            echo "Comment added successfully.";
        } else {
            echo "Error adding comment: " . $conn->error;
        }
        $stmt->close();
        $conn->close();
        echo "<meta http-equiv='refresh' content='0'>";
        exit();
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile</title>
</head>

<body>
    <h2>Profile of <?php echo htmlspecialchars($username); ?>!</h2>

    <h3>Public Comments</h3>
    <ul>
        <?php displayComments($public_comments); ?>
    </ul>

    <?php if ($can_view_private_comments): ?>
        <h3>Private Comments</h3>
        <ul>
            <?php displayComments($private_comments); ?>
        </ul>

        <h3>Add New Comment</h3>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>?id=<?php echo $url_user_id; ?>" method="post">
            <textarea name="comment_text" rows="4" cols="50" required></textarea><br>
            <input type="checkbox" id="is_public" name="is_public">
            <label for="is_public">Public</label><br>
            <button type="submit">Add Comment</button>
        </form>
    <?php endif; ?>

    <!-- Display uploaded image -->
    <?php
    $image_path = "uploads/" . md5($username) . "/profile.jpg"; 
    if (file_exists($image_path)) {
        echo "<img src='$image_path' alt='Profile Image'>";
    } else {
        echo "<div>No profile image uploaded.</div>";
    }
    ?>

    <!-- Image upload form -->
    <?php if (!file_exists($image_path) && $user_id == $url_user_id): ?>
    <form id="uploadForm" action="upload.php" method="post" enctype="multipart/form-data">
        <input type="file" id="imageInput" name="image" accept="image/*" onchange="changeFilename()">
    </form>

    <script>
        function changeFilename() {
            var newFilename = 'profile.jpg';
            var formData = new FormData(document.getElementById('uploadForm'));
            formData.set('image', document.getElementById('imageInput').files[0], newFilename);
            fetch('upload.php', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Error uploading image: ' + response.statusText);
                }
            }).catch(error => {
                console.error('Error uploading image:', error);
            });
        }
    </script>
    <?php endif; ?>

    <a href="logout.php">Logout</a>
</body>

</html>