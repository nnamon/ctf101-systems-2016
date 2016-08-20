<html>
    <head>
        <title>Knock Knock Onions!</title>
        <style type="text/css">
            body { background:black; color:white; font-size:10pt; }
        </style>
    </head>
<body>
<?php
    $id_value = $_COOKIE[user];
    $pw_value = $_COOKIE[password];

    $id_value=str_replace("!","1",$id_value);
    $id_value=str_replace("@","2",$id_value);
    $id_value=str_replace("$","3",$id_value);
    $id_value=str_replace("^","4",$id_value);
    $id_value=str_replace("&","5",$id_value);
    $id_value=str_replace("*","6",$id_value);
    $id_value=str_replace("(","7",$id_value);
    $id_value=str_replace(")","8",$id_value);

    $pw_value=str_replace("!","1",$pw_value);
    $pw_value=str_replace("@","2",$pw_value);
    $pw_value=str_replace("$","3",$pw_value);
    $pw_value=str_replace("^","4",$pw_value);
    $pw_value=str_replace("&","5",$pw_value);
    $pw_value=str_replace("*","6",$pw_value);
    $pw_value=str_replace("(","7",$pw_value);
    $pw_value=str_replace(")","8",$pw_value);

    for($i=0;$i<20;$i++){
        $id_value=base64_decode($id_value);
        $pw_value=base64_decode($pw_value);
    }

    echo("<font style=background:silver;color:black>&nbsp;&nbsp;HINT : base64&nbsp;&nbsp;</font><hr><a href=index.phps style=color:yellow;>index.phps</a><br><br>");
    echo("ID : $id_value<br>PW : $pw_value<hr>");

    if($id_value=="admin" && $pw_value=="NUSGreyhats"){
        success();
    }

    function success(){
        echo("<script>alert('XCTF{Haha_this_has_nothing_2_do_with_tor}');</script>");
    }
?>
    </body>
</html>
