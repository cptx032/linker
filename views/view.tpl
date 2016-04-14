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
			.margin-top35 {
				margin-top: -35px;
			}
		</style>
	</head>
	<body class="">
		<nav>
			<div class="nav-wrapper">
				<a href="#" class="brand-logo"><span class="pad-10">linker</span></a>
				<ul id="nav-mobile" class="right">
					<li><a title="add a new folder" href="/add/{{folder_id}}/0"><i class="material-icons">add</i></a></li>
					% if folder_parent:
						<li><a title="back to parent folder" href="/view/{{folder_parent}}"><i class="material-icons">replay</i></a></li>
					% end
				</ul>
			</div>
		</nav>

		<div id="main-content">
			<ul class="collection with-header">
				<li class="collection-header"><h4>{{folder_name}}</h4></li>
				% for item in elems:
					% if item.type == 1:
						<a href="/view/{{item.id}}" class="collection-item avatar">
							<img src="/images/folder.png" alt="folder-icon" class="circle">
							<span class="title">{{item.name}}</span>
							<p>{{item.desc}}</p>
							<a href="/add/{{item.id}}/{{item.id}}" class="btn-floating btn-small waves-effect waves-light teal right margin-top35">
								<i class="material-icons">mode_edit</i>
							</a>
							<a href="/delete/{{item.id}}" class="btn-floating btn-small waves-effect waves-light red right margin-top35">
								<i class="material-icons">delete</i>
							</a>
						</a>
					% else:
						<a target="_blank" href="{{item.desc}}" class="collection-item avatar">
							<img src="/images/contacts.png" alt="folder-icon" class="circle">
							<span class="title">{{item.name}}</span>
							<p>{{item.desc}}</p>
							<a href="/add/{{folder_parent}}/{{item.id}}" class="btn-floating btn-small waves-effect waves-light teal right margin-top35">
								<i class="material-icons">mode_edit</i>
							</a>
							<a href="/delete/{{item.id}}" class="btn-floating btn-small waves-effect waves-light red right margin-top35">
								<i class="material-icons">delete</i>
							</a>
						</a>
					% end
				% end
			</ul>
		</div>
	</body>
</html>
