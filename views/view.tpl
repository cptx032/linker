<!DOCTYPE html>
<html>
	<head>
		<title>View - {{parent_tree[-1].name}}</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
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
		<div class="navbar-fixed">
			<nav>
				<div class="nav-wrapper blue-grey darken-3">
				
				<span class="col s12" style="margin-left: 15px;">
					% for elem in parent_tree:
						<a href="/view/{{elem.id}}" class="breadcrumb">{{elem.name}}</a>
					% end
				</span>
					<ul id="nav-mobile" class="right">
						<li>
							<a class="tooltipped" data-tooltip="search links/folders" href="/search/''">
								<i class="material-icons">search</i>
							</a>
						</li>
						% if can_add:
							<li>
								<a class="tooltipped" data-tooltip="add a new link/folder" href="/add/{{folder_id}}/0">
									<i class="material-icons">add</i>
								</a>
							</li>
						% end
						<li>
							<a class="tooltipped" data-tooltip="logout from {{username}}" href="/logout">
								<i class="material-icons">power_settings_new</i>
							</a>
						</li>
					</ul>
				</div>
			</nav>
		</div>
		<div id="confirm-delete-modal" class="modal bottom-sheet">
			<div class="modal-content">
				<span id="hidden-id" style="display: none;">id</span>
				<h4 id="confirm-delete-title">
					Delete X?
				</h4>
				<p>
					This operation can't be undone
				</p>
			</div>
				<div class="modal-footer">
				<a href="javascript:$('#confirm-delete-modal').closeModal();" class=" modal-action modal-close waves-effect waves-green btn-flat teal white-text">
					Cancel
				</a>
				<a id="button-delete-item" href="javascript:go_to_delete()" class=" modal-action modal-close waves-effect waves-green btn-flat teal-text">
					Delete
				</a>
			</div>
		</div>
  
		<script>
			function go_to_delete() {
				window.location = '/delete/' + $('#hidden-id').text();
			}
			function delete_item(id, name) {
				$('#confirm-delete-title').text('Delete ' + name + '?');
				$('#hidden-id').text(id);
				$('#confirm-delete-modal').openModal();
			}
		</script>

		<div id="main-content">
			% if can_see:
			<ul class="collection">
				% for item in elems:
					% if item.type == 1:
						<a href="/view/{{item.id}}" class="collection-item avatar">
							<img src="/images/folder.png" alt="folder-icon" class="circle">
							<span class="title">{{item.name}}</span>
							<p>{{item.desc}}</p>
							% if can_edit:
								<a href="/add/{{item.id}}/{{item.id}}" class="btn-floating btn-small waves-effect waves-light teal right margin-top35">
									<i class="material-icons">mode_edit</i>
								</a>
							% end
							% if can_delete:
								<a href="javascript:delete_item({{item.id}}, '{{item.name}}')" class="btn-floating btn-small waves-effect waves-light red right margin-top35">
									<i class="material-icons">delete</i>
								</a>
							% end
						</a>
					% else:
						<a target="_blank" href="{{item.desc}}" class="collection-item avatar">
							<img src="/images/contacts.png" alt="folder-icon" class="circle">
							<span class="title">{{item.name}}</span>
							<p>{{item.desc}}</p>
							% if can_edit:
								<a href="/add/{{folder_parent}}/{{item.id}}" class="btn-floating btn-small waves-effect waves-light teal right margin-top35">
									<i class="material-icons">mode_edit</i>
								</a>
							% end
							% if can_delete:
								<a href="javascript:delete_item({{item.id}}, '{{item.name}}')" class="btn-floating btn-small waves-effect waves-light red right margin-top35">
									<i class="material-icons">delete</i>
								</a>
							% end
						</a>
					% end
				% end
			</ul>
			% else:
				<div style="padding: 55px;">
					You haven't permission to see the content
				</div>
			% end
		</div>
	</body>
</html>
