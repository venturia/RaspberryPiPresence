<H1>Presenze in Sala</H1>
<?php
//ini_set('display_errors', 'On');
//error_reporting(E_ALL);
if(isset($_GET["setalarm"]) || isset($_POST["setalarm"])) {
  if(isset($_GET["setalarm"])) {
    $alarmsetting=$_GET["setalarm"];
  }
  else if(isset($_POST["setalarm"])) {
    $alarmsetting=$_POST["setalarm"];
  }

  if($alarmsetting=="Abilita") {
    exec("touch /var/apache/enabled_alarm");
    echo "abilita <br>";
  }

  if($alarmsetting=="Disabilita") {
    exec("rm -f /var/apache/enabled_alarm");
    echo "disabilita <br>";
  }
}

$file="/home/pi/presence_status";
$status=exec("cat $file",$output,$retval);
$expstatus=explode(" ",$status);
$flag=$expstatus[count($expstatus)-1];
$date=$expstatus[0];
$time=$expstatus[1];
$lastdatetime=$date . " " . $time;
echo "Stato Sensore: " .$status . "<br>";
$now = new DateTime("NOW");
$lastchange = new DateTime($lastdatetime);
$delta = $now->getTimestamp() - $lastchange->getTimestamp();
if($flag==1) $delta=0;
$scaleddelta=0;
if($delta<60) {
   $scaleddelta=$delta*200./60.;}
else if($delta<600) {
   $scaleddelta=200+($delta-60)*200./(600.-60.);}
else if($delta<3600) {
   $scaleddelta=400+($delta-600)*200./(3600.-600.);}
else if($delta<86400) {
   $scaleddelta=600+($delta-3600)*200./(86400.-3600.);}
else {
   $scaleddelta=800+($delta-86400)*200./(864000.-86400.);}

echo $delta . " " . $scaleddelta . "<br>";
//$delta = $now-$lastchange
//echo $flag . " " . $time . " " . $date . " " .$delta . "<br>";
echo "Return value: " .$retval . "<br>";
?>
<html>
  <head>
    <script type='text/javascript' src='https://www.google.com/jsapi'></script>
    <script type='text/javascript'>
      google.load('visualization', '1', {packages:['gauge']});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['No signal', <?php echo intval($scaleddelta); ?>]
        ]);

        var options = {
          width: 800, height: 240,
          max: 1000,
          redFrom: 0, redTo: 200,
          yellowFrom:200, yellowTo: 400,
          greenFrom:400, greenTo: 800,
          majorTicks: ["ora","1m","10m","1h","1g",">10gg"],
          minorTicks: 3
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id='chart_div'></div>

<?php
   exec("pgrep -u root presence",$dummyout,$daemonrunning);
   if($daemonrunning==0) {
     echo "Daemon in esecuzione: Tutto OK<BR>";
   }
   else {
     echo "DAEMON NON FUNZIONA: L'allarme non funzionera' $daemonrunning<BR>";
   }
?>
    <form action="presenze.php" method="post">
Allarme <?php if(file_exists("/var/apache/enabled_alarm")) {echo "abilitato";} else {echo "disabilitato";} ?><br>
      <input onClick="return true;" type="submit" name="setalarm" value="Abilita"> 
      <input onClick="return true;" type="submit" name="setalarm" value="Disabilita">
    </form>
<?php
 exec("pgrep -u motion motion",$dummyout,$motionrunning);
 if($motionrunning==0) {
    exec("wget -q -O /dev/null http://localhost:8182/0/action/snapshot");
 }
 else {
    echo "motion non e' in esecuzione:  $motionrunning<BR>";
 }
 sleep(1);
 if ( file_exists("/tmp/motion/lastsnap.jpg") ) {
   echo "<img src='plot_from_tmp.php?file=/tmp/motion/lastsnap.jpg'/>";
 }
 else {
   echo "Snapshot NON trovato<BR>";
 }
?>
  </body>
</html>
