<script>
	import DeviceRow from './DeviceRow.svelte';
	export let filteredDevices;
</script>

<div class="overflow-x-auto pt-4">
	<table class="table table-compact w-full">
		<!-- head -->
		<thead>
			<tr>
				<th>Name</th>
				<th>IP Address</th>
				<th>Site</th>
				<th>Model</th>
				<th>Vendor</th>
				<th>Operating System</th>
				<th>OS Version</th>
				<th />
			</tr>
		</thead>
		<tbody>
			{#each filteredDevices as device (device.id)}
				<DeviceRow {device} />
			{/each}
		</tbody>
	</table>
</div>
