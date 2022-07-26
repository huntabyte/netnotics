<script>
	import DeviceRow from './DeviceRow.svelte';
	import InterfaceRow from './InterfaceRow.svelte';
	export let filteredDevices;
</script>

<table class="table table-compact w-full max-h-full min-h-full flex flex-grow">
	<!-- head -->
	<thead>
		<tr>
			<th>
				<label>
					<input type="checkbox" class="checkbox checkbox-sm" />
				</label>
			</th>
			<th>Name</th>
			<th>IP Address</th>
			<th>Host</th>
			<th>Manageable</th>
			<th />
		</tr>
	</thead>
	<tbody class="flex-grow">
		{#each filteredDevices as device (device.id)}
			<DeviceRow {device} />
		{/each}
	</tbody>
</table>
