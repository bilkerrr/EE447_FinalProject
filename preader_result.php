<?php
	echo '<link rel="stylesheet" type="text/css" href="result.css">';
	echo "<a href = 'http://localhost/preader_input.html'><button class='btn'>  < Back </button></a><br>";
	header("Content-Type:text/html;charset=utf-8");
	$filename = $_FILES['upload'];
	$fileInfoName = $filename["name"];//文件名
	$fileInfoPath = $filename["tmp_name"];//文件当前路径文件夹
	move_uploaded_file($fileInfoPath, "./source/".$fileInfoName);

	$path="C:\HUA\Softwares\Python\python.exe ./pyfile/information_extract.py ";
	$params = "C:/xampp/htdocs/source/".$fileInfoName;
	
	exec($path.$params, $array, $res);

	#var_dump($array);

	echo "<div class='abstract'>Abstract</div>";
	echo "<div class='abstract-content'>";
	echo $array[0];
	echo "</div>";

	echo "<div class='reference'>Reference</div>";


	$path2="C:\HUA\Softwares\Python\python.exe ./pyfile/keywords_process.py 2>&1 ";
	exec($path2.$params, $array2, $res2);
	
	#var_dump($dict);

	echo '<script type="text/javascript">
			function startUpload() {
				document.getElementById("processing").innerHTML = "loading...";
				return true;
			}
			
			function stopUpload(rel){
				var msg = "";
				switch (rel) {
						case 0:
								msg = "Success";
								break;
						case 1:
								msg = "Exceed maximum size";
								break;
						case 2:
								msg = "PDF file only";
								break;
						case 3:
								msg = "Failed";
								break;
						default:
								msg = "Upload failed";
				}
				document.getElementById("processing").innerHTML = msg;
			}
		</script>';

	for($i=1;$i<count($array);$i++){
		echo "<div class='reference-item'>";
		# reference item
		echo $array[$i];
		$idx = substr($array[$i], 1, strpos($array[$i],']')-1);
		echo "</div>";

		$i++;
		# fetch paper
		if(strcmp($array[$i],"null")!=0){
			echo $array[$i];
		}
	}

	echo "<div class='highlight'>Highlighter</div>";

	echo "<div class='note'>
		Instruction:<br>
		1. Rename your local PDF file as its index.<br>
		2. Submit it through the uploader.<br>
		3. Click 'Download Highlighted' button to get the highlighted version.
		</div>";

	echo '<div style="margin-left:30px">
			<div id="processing"></div>
			<form id="upload-form" action="upload.php" method="post" enctype="multipart/form-data" 
					target="form-target" οnsubmit="startUpload();">
				<input type="hidden" name="MAX_FILE_SIZE" value="5000000" />
				<label class="file">
				<input type="file" name="myfile" />
				<span class="file-custom"></span>
				</label>
				<br>
				<label class="submit">
				<input type="submit" name="submit" value="Upload" />
				<span class="submit-custom"></span>
				</label>
			</form>
			<br>
			<iframe style="width:0; height:0; border:0;" name="form-target"></iframe>
		</div>';

	echo '<a href=http://localhost/source/highlight.pdf download="highlight.pdf"><button class="download-btn">Download Highlighted</button></a>'

?>
