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
#Get Client IP
$clientIP = $_SERVER['REMOTE_ADDR'];

$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "ovsDB";

#Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

#prepare and bind
$stmt = "SELECT CHK_Status, Scan_Results FROM nmap_queue WHERE IP_ADDR = '" . $clientIP . "'";
#execute statement
$result = $conn->query($stmt);

#check if the results are printed 
if ($result->num_rows > 0) {
	$row=mysqli_fetch_row($result);
	
	if (strpos($row[0], 'Denied') !== false) { #If user is denied, show results
		$scan_results=$row[1];
	}else { #Redirect user back to index.php as he has not been denied
		header('Location: index.php');
	}

}

#if the rescan button has been pressed, reset CHK_Status to 'New'
if (isset($_REQUEST['rescan'])) {
    rescan();
} 

function rescan() {
	global $clientIP;
	global $conn;
	# prepare and bind
	$stmt = "UPDATE nmap_queue SET CHK_Status = 'New' WHERE IP_ADDR = '" . $clientIP . "'";

	if ($conn->query($stmt) == TRUE) { #Redirect to index.html
	    #echo "Record updated successfully";
	    header('Location: index.php');
	} else {
	    #echo "Error updating record: " . $conn->error;
	}

	$conn->close();

	exit;
}

?>
<form action ="" method = "POST">
<h3>You have been DENIED access to our network.</h3>
<h4>Your scan result is as shown:</h4>
<h4><?php echo $scan_results; ?></h4>
<h3>PLEASE click on 'Rescan' to scan your device again.</h3>

    <input type="submit" name="rescan" value="Rescan"/>
</form>

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