<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YAML Upload Form</title>
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
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
