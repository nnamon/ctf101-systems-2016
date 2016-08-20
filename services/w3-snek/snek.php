<?php

$snek = "snek0.php";
$snekie = $_COOKIE['snek'];
$new = false;

if (!empty($_GET['besnek'])) {
    $snek = $_GET['besnek'];
    $new = true;
}

include $snek;
include "secret_hashkey.php";

if ($new) {
    $snekie = trim(exec("python /sneks/straya.py generate $secret_key " . escapeshellarg($snekfile)));
    setcookie("snek", $snekie);
}

?>

<head>
    <title>Don't Dread on Me</title>
    <style>
    img {
        width: 50%;
        height: auto;
    }
    </style>
</head>
<body>
<div align="center">
    <h1>U ARE THIS SNEK :D:D:D:D</h1>

<?php

passthru("python /sneks/straya.py load $secret_key " . escapeshellarg($snekie));

?>
<br>
<a href="./snek.php?besnek=snek1.php">be snek1</a>
<a href="./snek.php?besnek=snek2.php">be snek2</a>
<a href="./snek.php?besnek=snek3.php">be snek3</a>
<a href="./snek.php?besnek=snek4.php">be snek4</a>
<a href="./snek.php?besnek=snek5.php">be snek5</a>
</div>
</body>
