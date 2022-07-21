<script>
	import InterfaceRow from '$components/InterfaceRow.svelte';
	export let items;
</script>

<div class="overflow-x-auto">
	<table class="table w-full">
		<!-- head -->
		<thead>
			<tr>
				<th>Name</th>
				<th>IP Address</th>
				<th>Admin</th>
				<th>Oper</th>
				<th>MAC Address</th>
				<th>Speed</th>
				<th>Last Change</th>
				<th />
			</tr>
		</thead>
		<tbody>
			{#each items as item (item.name)}
				<InterfaceRow {item} />
			{/each}
		</tbody>
	</table>
</div>

<style>
	th {
		@apply bg-primary-content text-neutral;
	}
</style>
