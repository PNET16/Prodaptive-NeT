<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Prodaptive-Net Admin</title>
    <style type="text/css">
        /* Layout */
        body {
            min-width: 630px;
        }
        #container {
            padding-left: 200px;
            padding-right: 190px;
        }
        
        #container .column {
            position: relative;
            float: left;
        }
        
        #center {
            padding: 10px 20px;
            width: 100%;
        }
        
        #left {
            width: 180px;
            padding: 0 10px;
            right: 240px;
            margin-left: -100%;
        }
        
        #right {
            width: 130px;
            padding: 0 10px;
            margin-right: -100%;
        }
        
        #footer {
            clear: both;
        }
        
        /* IE hack */
        * html #left {
            left: 150px;
        }
        /* Make the columns the same height as each other */
        #container {
            overflow: hidden;
        }
        #container .column {
            padding-bottom: 1001em;
            margin-bottom: -1000em;
        }
        /* Fix for the footer */
        * html body {
            overflow: hidden;
        }
        
        * html #footer-wrapper {
            float: left;
            position: relative;
            width: 100%;
            padding-bottom: 10010px;
            margin-bottom: -10000px;
            background: #fff;
        }
        /* Aesthetics */
        body {
            margin: 0;
            padding: 0;
            font-family:Sans-serif;
            line-height: 1.5em;
        }
        
        p {
            color: #555;
        }
        nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }
        
        nav ul a {
            color: darkgreen;
            text-decoration: none;
        }
        #header, #footer {
            font-size: large;
            padding: 0.3em;
            background: #BCCE98;
        }
        #left {
            background: #DAE9BC;
        }
        
        #right {
            background: #F7FDEB;
        }
        #center {
            background: #fff;
        }
        #container .column {
            padding-top: 1em;
        }
        
    </style>
    
</head>
<body>
    <header id="header"><h1><img src="/images/Pnet.PNG" width="50" height="50" title="PNet picture"/>Prodaptive-Net</h1></header>
    <div id="container">
        <main id="center" class="column">
            <article>
            
                <h1>Welcome to the Prodaptive-Net admin login page</h1>
                <br/>

<?php
if(isset($_POST['login'])) {
    $uname=$_POST['uname'];
    $pwd=$_POST['psw'];

    $servername = "localhost";
    $username = "root";
    $password = "root";
    $dbname = "ovsDB";
    #Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    #Check connection
    if ($conn->connect_error) {
       die("Connection failed: " . $conn->connect_error);
    }
    #prepare and bind
    $stmt = "SELECT * FROM admin_login WHERE username='".$uname."' AND password='".$pwd."'";
    #execute statement
    $result = $conn->query($stmt);
    
    #check if the results are printed
    if ($result->num_rows > 0) {
        header('Location: dashboard.php');
    }else {
       
        echo '<font color="red"><h4>Username or password is incorrect</h4></font>';
    }
}
?>
                <form action="" method="POST">
                    <label><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="uname" required>
                    <br/>
                    <label><b>Password</b></label>
                    <input type="password" placeholder="Enter Password" name="psw" required>
                    <br/>
                    <input type="submit" name="login" value="Login"/>
                </form>

            </article>  
                            
        </main>
        <nav id="left" class="column">
            <h3>About</h3>
            <ul>
                <li><a href="#"><u>Information</u></a></li>
            </ul>
        </nav>
    </div>
    <div id="footer-wrapper">
        <footer id="footer">
            <center>
            <p>Prodaptive-Net</p>
            <p>2016 - 2017</p>
            </center>
        </footer>
    </div>
</body>
</html>


