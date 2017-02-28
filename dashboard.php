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
           
                <h1>Welcome to the Prodaptive-Net admin page</h1>
                <br/>
                <form method="post" action="">

<?php

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
#T_Q_ZONE_PC Table
$stmt = "SELECT * FROM T_Q_ZONE_PC";
#execute statement
$result = $conn->query($stmt);

#check if the results are printed 
if ($result->num_rows > 0) {
    echo '<h3>T_Q_ZONE_PC table</h3>';
    echo '<table border=\'1\'>';
    echo '<tr><th>Seq_ID</th><th>MAC Address</th><th>IP Address</th><th>Switch</th><th>Time Connected</th><th>Last Modified</th><th>Status</th><th>Action</th></tr>';
    while($row_records=mysqli_fetch_array($result)) {
        echo '<tr>';
        echo '<td>'.($row_records['Seq_ID']).'</td>';
        echo '<td>'.($row_records['MAC_ADDR']).'</td>';
        echo '<td>'.($row_records['IP_ADDR']).'</td>';
        echo '<td>'.($row_records['IN_PORT']).'</td>';
        echo '<td>'.($row_records['CREAT_TM']).'</td>';
        echo '<td>'.($row_records['LAST_MOD_TM']).'</td>';
        echo '<td>'.($row_records['CHK_STATUS']).'</td>';
        echo '<td><input type="checkbox" name="del[]" id="del" value="'.($row_records['Seq_ID']).'"/>';
        echo '</tr>';
    }
    echo '</table><input type="submit" name="delrecord" value="Delete records"/></td>';
}else {
    echo '<h4>Nothing to print from T_Q_ZONE_PC</h4>';
}

if(isset($_POST['delrecord'])) {
    $id = $_POST['del'];
    #echo $ip;
    $execlist='';
    foreach($id as $record) {
        $execlist .= $record.',';
    }
    $execlist1 = rtrim($execlist, ',');
    #echo $execlist1;
    $stmt="DELETE FROM T_Q_ZONE_PC WHERE Seq_ID IN (".($execlist1).")";
    #echo $stmt;
    if (mysqli_query($conn, $stmt)) {
        #echo 'Successful deletion';
        header('Refresh: 1;URL=dashboard.php');
    }else {
        echo 'Error';
    }

}

echo '<br/>______________________________________________________________________________________________________________________________';

#Nmap queue Table
$stmt = "SELECT * FROM nmap_queue";
#execute statement
$result = $conn->query($stmt);

#$result = $stmt->execute();

#check if the results are printed 
if ($result->num_rows > 0) {
    echo '<h3>nmap_queue table</h3>';
    echo '<table border=\'1\'>';
    echo '<tr><th>ID</th><th>IP Address</th><th>Status</th><th>Scan Results</th><th>Sec Status</th><th>Action</th></tr>';
    while($row_records=mysqli_fetch_array($result)) {
        echo '<tr>';
        echo '<td>'.($row_records['ID']).'</td>';
        echo '<td>'.($row_records['IP_ADDR']).'</td>';
        echo '<td>'.($row_records['CHK_Status']).'</td>';
        echo '<td>'.($row_records['Scan_Results']).'</td>';
        echo '<td>'.($row_records['Sec_Status']).'</td>';
        echo '<td><input type="checkbox" name="del1[]" id="del1" value="'.($row_records['ID']).'"/>';
        echo '</tr>';
    }
    echo '</table><input type="submit" name="delrecord1" value="Delete records"/></td>';
}else {
    echo '<h4>Nothing to print from nmap_queue</h4>';
}

if(isset($_POST['delrecord1'])) {
    $id = $_POST['del1'];
    #echo $ip;
    $execlist='';
    foreach($id as $record) {
        $execlist .= $record.',';
    }
    $execlist1 = rtrim($execlist, ',');
    #echo $execlist1;
    $stmt="DELETE FROM nmap_queue WHERE ID IN (".($execlist1).")";
    #echo $stmt;
    if (mysqli_query($conn, $stmt)) {
        #echo 'Successful deletion';
        header('Refresh: 1;URL=dashboard.php');
    }else {
        echo 'Error';
    }

}

#$conn.close();
?>
                </form>
            </article>                                
        </main>
        <nav id="left" class="column">
            <h3>About</h3>
            <ul>
                <li><a href="#"><u>Information</u></a></li>

<form action="logout.php"  method="POST">
    
                    <input type="submit" name="logout" value="Logout"/>
                </form>



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
<?php
$conn.close();
?>
  