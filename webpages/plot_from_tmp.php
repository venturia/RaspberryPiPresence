<?php
$file = $_GET['file'];

$pname = $file;
if ( file_exists($file) ) {
  $f=fopen($file,"r");
  $size = filesize($file);
  $data = fread($f,$size);
  header("Content-type: image/png");
  header("Content-length: $size");
  header("Content-Disposition: inline; filename=$pname");
  header("Content-Description: PHP Generated Data");
  echo $data;
}
?>

