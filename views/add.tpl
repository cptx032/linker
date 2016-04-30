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
			<div class="nav-wrapper blue-grey darken-3">
				<a href="#" class="brand-logo"><span class="pad-10">{{'edit' if edit_object else 'add'}} link</span></a>
			</div>
		</nav>

		<div id="main-content">
			<div class="row">
				<form class="col s12" action="/add" method="POST" id="main-form">
					<input type="hidden" value="{{parent_id}}" name="parent_id">
					<input type="hidden" value="{{edit_object.id if edit_object else 0}}" name="edit_id">
					<div class="row">
						<div class="input-field col s12">
							<input autofocus placeholder="name" name="name" id="name" type="text" class="validate" value="{{edit_object.name if edit_object else ''}}">
							<label for="name">Name</label>
						</div>
					</div>
					<div class="row">
						<div class="input-field col s12">
							<input placeholder="Folder description or url link" name="description" id="description" type="text" class="validate" value="{{edit_object.desc if edit_object else ''}}">
							<label for="description">Description</label>
						</div>
					</div>

					<a style="margin: 5px;" href="javascript:$( '#main-form' ).submit()" class="btn-floating btn-large waves-effect waves-light blue-grey darken-3 left tooltipped" data-tooltip="Save">
						<i class="material-icons">done</i>
					</a>

					<a style="margin: 5px;" href="javascript:history.back()" class="btn-floating btn-large waves-effect waves-light blue-grey darken-3 right tooltipped" data-tooltip="Cancel editing">
						<i class="material-icons">cancel</i>
					</a>

				</form>
			</div>
		</div>
		
	</body>
</html>
