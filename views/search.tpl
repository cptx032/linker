<!DOCTYPE html>
<html>
	<head>
		<title>Search</title>
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
		<script type="text/javascript">
			function search()
			{
				var term = document.getElementById('search');
				if (term.value != '')
					window.location.href = `/search/${term.value}`;
			}
		</script>
	</head>
	<body class="">
		<nav>
			<div class="nav-wrapper blue-grey darken-3">
				<a href="#" class="brand-logo">
					<span class="pad-10">Search</span>
				</a>
			</div>
		</nav>

		<div id="main-content">
			<div class="row">
				<div class="row">
					<div class="input-field col s12">
						<input autofocus placeholder="text contained in link or folder" name="search" id="search" type="text" class="validate">
						<label for="name">Search</label>
					</div>
				</div>
				<a href="javascript:search()" class="btn-floating btn-large waves-effect waves-light blue-grey darken-3 right tooltipped" data-tooltip="search">
					<i class="material-icons">done</i>
				</a>
			</div>
		</div>
		
	</body>
</html>
