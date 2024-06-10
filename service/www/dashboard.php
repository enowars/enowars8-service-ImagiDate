<?php
session_start();
error_reporting(0);
require_once 'config.php';

if (isset($_SESSION["user_id"])) {
    $user_id = $_SESSION["user_id"];
} else {
    header("Location: login.php");
    exit();
}

function getAllUserProfiles($conn)
{
    $query = "SELECT * FROM users";
    $result = $conn->query($query);
    return $result->fetch_all();
}

$profiles = getAllUserProfiles($conn);
$limit = 10;
$total_profiles = count($profiles);
$total_pages = ceil($total_profiles / $limit);

if (isset($_GET['page']) && is_numeric($_GET['page'])) {
    $current_page = (int) $_GET['page'];
} else {
    $current_page = 1;
}

$offset = ($current_page - 1) * $limit;
$current_profiles = array_slice($profiles, $offset, $limit);
?>

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Dashboard</title>
    <link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="styles/index.css" rel="stylesheet">
    <style>
        .table-container {
            margin: auto;
        }
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

    <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
        <header class="masthead mb-auto">
            <div class="inner">
                <h3 class="masthead-brand">ImagiDate</h3>
                <nav class="nav nav-masthead justify-content-center">
                    <a class="nav-link active" href="index.php">Homepage</a>
                    <a class="nav-link" href='profile.php?id=<?php echo $user_id; ?>'>Profile</a>
                    <a class="nav-link" href="logout.php">Logout</a>
                </nav>
            </div>
        </header>

        <main role="main" class="inner cover">
            <a href="index.php">
                <img class="mb-4" src="/images/logo.png" id="heart" alt="" width="72" height="72">
            </a>
            <h1 class="cover-heading">List of users</h1>
            <div class="table-responsive table-container">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Gender</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($current_profiles as $profile): ?>
                            <tr data-href="profile.php?id=<?php echo $profile[0]; ?>">
                                <td><?php echo $profile[0]; ?></td>
                                <td><?php echo $profile[1]; ?></td>
                                <td><?php echo $profile[3]; ?></td>
                                <td><?php echo $profile[4]; ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <br>
            <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <?php if ($current_page > 1): ?>
                        <li class="page-item">
                            <a class="page-link" href="?page=<?php echo $current_page - 1; ?>" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                                <span class="sr-only">Previous</span>
                            </a>
                        </li>
                    <?php endif; ?>
                    <?php for ($i = 1; $i <= $total_pages; $i++): ?>
                        <li class="page-item <?php if ($i == $current_page) echo 'active'; ?>">
                            <a class="page-link" href="?page=<?php echo $i; ?>"><?php echo $i; ?></a>
                        </li>
                    <?php endfor; ?>
                    <?php if ($current_page < $total_pages): ?>
                        <li class="page-item">
                            <a class="page-link" href="?page=<?php echo $current_page + 1; ?>" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                                <span class="sr-only">Next</span>
                            </a>
                        </li>
                    <?php endif; ?>
                </ul>
            </nav>
        </main>

        <footer class="mastfoot mt-auto">
            <div class="inner">
                <p>This page is dedicated for all the simps out there. Enjoy!</p>
            </div>
        </footer>
    </div>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="https://getbootstrap.com/docs/4.0/assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="https://getbootstrap.com/docs/4.0/assets/js/vendor/popper.min.js"></script>
    <script src="https://getbootstrap.com/docs/4.0/dist/js/bootstrap.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const rows = document.querySelectorAll("tbody tr");
            rows.forEach(row => {
                row.addEventListener("click", function() {
                    window.location.href = row.dataset.href;
                });
            });
        });
    </script>
</body>

</html>
