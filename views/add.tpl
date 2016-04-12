<!DOCTYPE html>
<html>
	<head>
		<title>Add link</title>
		<meta charset="utf-8">
		<script type="text/javascript" charset="utf-8" src="https://code.jquery.com/jquery-2.2.2.min.js"></script>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/css/materialize.min.css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/js/materialize.min.js"></script>
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
		<style>
			.width-100 {
				width: 100%;
			}
			.pad-10 {
				padding: 10px;
			}
			#main-content {
				padding: 25px;
			}
		</style>
	</head>
	<body class="">
		<nav>
			<div class="nav-wrapper">
				<a href="#" class="brand-logo"><span class="pad-10">add link</span></a>
			</div>
		</nav>

		<div id="main-content">
			<div class="row">
				<form class="col s12">
					<div class="row">
						<div class="input-field col s12">
							<input placeholder="name" id="name" type="text" class="validate">
							<label for="first_name">Name</label>
						</div>
					</div>
					<div class="row">
						<div class="input-field col s12">
							<input placeholder="Folder description or url link" id="name" type="text" class="validate">
							<label for="first_name">Description</label>
						</div>
					</div>
					
					<a class="btn-floating btn-large waves-effect waves-light red right"><i class="material-icons">add</i></a>
					
				</form>
			</div>
		</div>
		
	</body>
</html>
