<?php
    # nimda:stahyerGSUN
    if(!$_COOKIE[user]){
        $tmp_id = "guest";
        $tmp_pass = "guest";

        for( $i=0;$i<20;$i++ ){
            $tmp_id = base64_encode($tmp_id);
            $tmp_pass = base64_encode($tmp_pass);
        }

        $tmp_id = str_replace("1","!",$tmp_id);
        $tmp_id = str_replace("2","@",$tmp_id);
        $tmp_id = str_replace("3","$",$tmp_id);
        $tmp_id = str_replace("4","^",$tmp_id);
        $tmp_id = str_replace("5","&",$tmp_id);
        $tmp_id = str_replace("6","*",$tmp_id);
        $tmp_id = str_replace("7","(",$tmp_id);
        $tmp_id = str_replace("8",")",$tmp_id);

        $tmp_pass = str_replace("1","!",$tmp_pass);
        $tmp_pass = str_replace("2","@",$tmp_pass);
        $tmp_pass = str_replace("3","$",$tmp_pass);
        $tmp_pass = str_replace("4","^",$tmp_pass);
        $tmp_pass = str_replace("5","&",$tmp_pass);
        $tmp_pass = str_replace("6","*",$tmp_pass);
        $tmp_pass = str_replace("7","(",$tmp_pass);
        $tmp_pass = str_replace("8",")",$tmp_pass);

        Setcookie("user",$tmp_id);
        Setcookie("password",$tmp_pass);

        echo("<meta http-equiv=refresh content=0>");
    }
?>
