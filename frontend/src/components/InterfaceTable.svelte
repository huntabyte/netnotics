<script>
	import InterfaceRow from '$components/InterfaceRow.svelte';
	export let interfaces;
	export let device;
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
			{#each interfaces as item (item.name)}
				<InterfaceRow {item} {device} />
			{/each}
		</tbody>
	</table>
</div>

<style>
	th {
		@apply bg-primary-content text-neutral;
	}
</style>
