<!DOCTYPE html>
<html>
	<head>
		<title>{{folder_name}} - View</title>
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
		</style>
	</head>
	<body class="">
		<nav>
			<div class="nav-wrapper">
				<a href="#" class="brand-logo"><span class="pad-10">linker</span></a>
				<ul id="nav-mobile" class="right">
					<li><a href="/add/{{folder_id}}"><i class="material-icons">add</i></a></li>
					<li><a href="/delete/{{folder_id}}"><i class="material-icons">delete</i></a></li>
				</ul>
			</div>
		</nav>

		<div id="main-content">
			<ul class="collection with-header">
				<li class="collection-header"><h4>{{folder_name}}</h4></li>
				% for item in elems:
					<a href="{{item.desc}}" class="collection-item avatar">
						% if item.type == 1:
							<img src="/images/folder.png" alt="folder-icon" class="circle">
						% elif item.type == 2:
							<img src="/images/contacts.png" alt="link-icon" class="circle">
						% end
						<span class="title">{{item.name}}</span>
						<p>{{item.desc}}</p>
					</a>
				% end
			</ul>
		</div>
	</body>
</html>
