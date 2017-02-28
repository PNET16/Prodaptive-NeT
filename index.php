<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Prodaptive-Net</title>
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
    <header id="header"><h1><img src="/images/Capture.PNG" width="50" height="50" title="PNet picture"/>Prodaptive-Net</h1></header> 
    <div id="container">
        <main id="center" class="column">
            <article>
            
                <h1>Welcome to the Prodaptive-Net gateway page</h1>
                <br/>
<?php
$clientIP = $_SERVER['REMOTE_ADDR'];
#echo "Your IP is: ";
#echo $clientIP;
$status = 0;
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
$stmt = "SELECT CHK_Status FROM nmap_queue WHERE IP_ADDR = '" . $clientIP . "'";
#execute statement
$result = $conn->query($stmt);
#$result = $stmt->execute();
#check if the results are printed
if ($result->num_rows > 0) {
    
    #header('Location: redirect.php');
    #fetch the value CHK_Status from the DB
    $row=mysqli_fetch_assoc($result);
    #echo $row['CHK_Status'];
    #if denied
    if (strpos($row['CHK_Status'], 'Denied') !== false) {
        #redirect to other page for rescan
        header('Location: redirect.php');
    }elseif (strpos($row['CHK_Status'], 'Pending') !== false) { #Pending status show computer is now being queued
        echo '<h3>Your device is now being queued for the scan by the system</h3>';
        echo '<h3>Please wait a moment</h3>';
        #echo 'Your computer is now being queued for a scan';
    }elseif (strpos($row['CHK_Status'], 'Scanning') !== false) { #Scanning status show computer is now being scanned
        echo '<h3>Your computer is now being scanned</h3>';
        echo '<h3>Please wait a moment</h3>';
    }elseif (strpos($row['CHK_Status'], 'New') !== false) { #New status redirect to pending page
        echo '<h3>Your device is now being queued for the scan by the system</h3>';
        echo '<h3>Please wait a moment</h3>';
        #echo 'Your status is new!';
    }elseif (strpos($row['CHK_Status'], 'Cleared') !== false) {
        echo '<h3>You are cleared!</h3>';
        echo '<h4>You can now access the network</h4>';
        echo '<h5>If you are facing problems connecting to the internet after you are cleared, you can do the following</h5>';
        echo '<ul><li>Type "ipconfig /flushdns" in your command prompt</li>';
        echo '<li>Clear your web browser\'s cache</li>';
        echo '<li>Use a different browser to access the internet</li></ul>';
        echo '<h4><a href="https://www.google.com.sg">https://www.google.com.sg</a></h4>';
    }
}else { #if user is not new or scanned, send him to agree to scan
    echo '<ul>';
    echo '<li><h3>To connect to the network, a scan must be conducted on your device to ensure that it is secure</h3></li>';
    echo '<li><h3>Users who are found to have deliberately compromise the network will be strictly dealt with by the authorities</h3></li>';
    echo '<li><h3>To begin the scan on your device, click on the "I agree" button at the bottom to allow the system to carry out a scan on your device</h3></li>';
    echo '</ul>';
    echo '<form action="welcome.php" method="POST">';
    echo '<input type="submit" name="formSubmit" value="I Agree"/>';
    echo '</form>';
}
$conn->close();
?>
            </article>                                
        </main>
        <nav id="left" class="column">
            <h3>About</h3>
            <ul>
                <li><a href="video.html" target = "_blank"><u>Video on Prodaptive-Net</u></a></li>
                <li><br/></li>
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