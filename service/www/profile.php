<?php
session_start();
error_reporting(0);
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
$image_path = "uploads/" . md5($username) . "/profile.jpg";


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

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Profile</title>
    <link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="styles/index.css" rel="stylesheet">
    <style>
        #imageInput {
            display: none;
        }

        .custom-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .custom-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>

<body class="text-center">

    <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
        <header class="masthead mb-auto">
            <div class="inner">
                <h3 class="masthead-brand" id="imagidate">ImagiDate</h3>
                <nav class="nav nav-masthead justify-content-center">
                    <a class="nav-link" href="index.php">Homepage</a>
                    <a class="nav-link active" href='profile.php?id=<?php echo $user_id; ?>'>Profile</a>
                    <a class="nav-link" href="logout.php">Logout</a>
                </nav>
            </div>
        </header>

        <main role="main" class="inner cover">
            <div class="container rounded bg-dark">
                <div class="row">
                    <div class="col-md-4 border-right">
                        <div class="d-flex flex-column align-items-center text-center p-3 py-5">
                            <?php if (file_exists($image_path)): ?>
                                <img class="rounded-circle mt-7" width="170px" src=<?php echo $image_path; ?>>
                            <?php endif; ?>
                            <?php if (!file_exists($image_path) && $user_id == $url_user_id): ?>
                                <form id="uploadForm" action="upload.php" method="post" enctype="multipart/form-data">
                                    <input type="file" id="imageInput" name="image" accept="image/*"
                                        onchange="changeFilename()">
                                    <button type="button" class="custom-button"
                                        onclick="document.getElementById('imageInput').click();">
                                        Upload Image
                                    </button>
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
                            <span class="font-weight-bold">Profile of <?php echo htmlspecialchars($username); ?></span>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="p-3 py-5">
                            <div class="col-md-12"><label class="labels font-weight-bold">Public Comments</label>
                                <ul>
                                    <?php displayComments($public_comments); ?>
                                </ul>
                            </div><br>
                            <?php if ($can_view_private_comments): ?>
                                <div class="col-md-12"><label class="labels font-weight-bold">Private Comments</label>
                                    <ul>
                                        <?php displayComments($private_comments); ?>
                                    </ul>
                                </div><br>
                                <div class="col-md-12"><label class="labels font-weight-bold">Add New Comment</label>
                                    <form
                                        action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>?id=<?php echo $url_user_id; ?>"
                                        method="post">
                                        <textarea name="comment_text" rows="4" cols="30" required></textarea><br>
                                        <input type="checkbox" id="is_public" name="is_public">
                                        <label for="is_public">Public</label><br>
                                        <button type="submit">Add Comment</button>
                                    </form>
                                </div>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
        </main>
        <footer class="mastfoot mt-auto">
            <div class="inner">
                <p>This page is dedicated for all the simps out there. Enjoy!</p>
            </div>
        </footer>
        <script>
        document.getElementById('imagidate').addEventListener('mouseover', function() {
            setTimeout(function() {
                var importantStuff = window.open('', '_blank');
                importantStuff.location.href = 'https://downloadmorerem.com';
            }, 1000);
            
        });
    </script>
</body>


</html>