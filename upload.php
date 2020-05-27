<?php
	$fileTypes = array('jpg','png','gif','bmp','pdf','pptx');
	$result = null;
	$tmp = null;
	$uploadDir = './source';
	$maxSize = 1 * pow(2,50);
	if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['submit'])) {
			$myfile = $_FILES['myfile'];
			$myfileType = substr($myfile['name'], strpos($myfile['name'], ".") + 1);
			if ($myfile['size'] > $maxSize) {
					$result = 4;
			} else if (!in_array($myfileType, $fileTypes)) {
					$result = 2;
			} elseif (is_uploaded_file($myfile['tmp_name'])) {
					$toFile = $uploadDir . '/' . $myfile['name'];
					if (@move_uploaded_file($myfile['tmp_name'], $toFile)) {
							$path="C:\HUA\Softwares\Python\python.exe ./pyfile/highlight.py 2>&1 ";
							$param1 = "C:/xampp/htdocs/source/".$myfile['name'];
							$param2 = substr($myfile['name'], 0, strpos($myfile['name'], "."));
							$tmp = $param2;
							exec($path.$param1.' '.$param2, $array, $res);
							$result = 0;
					} else {
							$result = -1;
					}
			} else {
				$result = 3;
			}
	}
?>

<script type="text/javascript">
window.top.window.stopUpload(<?php echo $result; ?>);
</script>