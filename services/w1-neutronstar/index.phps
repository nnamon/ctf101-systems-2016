<html>
<head>
    <title>NEUTRON STAR COLLIDER</title>
    <style>
        body {
            background-image: url("blackhole.jpg");
        }
        h1 {
            color: white;
        }
        form {
            color: white;
        }
        p {
            color: white;
        }
    </style>
</head>
<body>
<h1>Super Awesome Blackhole Collider</h1>
<form method="post">
Username:<br>
<input type="text" name="username"><br><br>
Password:<br>
<input type="text" name="password"><br><br>
<input type="submit" value="Submit">
</form>
<?php

include 'flag_header.php';

# StackOverflow says the probability of a collision is 340 undecillion 282
# decillion 366 nonillion 920 octillion 938 septillion 463 sextillion 463
# quintillion 374 quadrillion 607 trillion 431 billion 768 million 211 thousand
# 456 so we should be pretty safe, huh Rick!
# http://stackoverflow.com/questions/201705/how-many-random-elements-before-md5-produces-collisions
$admins = array("rick:db25b8ea97562fdecb013bc197aab2aa",
                "morty:0e046769954751531150123789251246",
                "summer:3233f8995bd41a14635b46531c9b0a6f");
# Shut up, Morty.

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $auth = false;
    $user = $_POST["username"];
    $pass = md5($_POST["password"]);

    foreach ($admins as &$v) {
        $f = explode(":", $v);
        if ($user == $f[0] && $pass == $f[1]) {
            $auth = true;
        }
    }

    if ($auth == true) {
        echo "<p>Awesome, you're one of us. Here's your flag: $flag!";
    } else {
        echo "<p>Look Morty, it's one of them *burp*. It's one of them bureaucrats!</p>";
    }
}
?>

<p><a href="./index.phps">Source</a></p>
</body>
</html>
