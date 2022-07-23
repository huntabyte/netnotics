<script>
	import DeviceRow from './DeviceRow.svelte';
	import InterfaceRow from './InterfaceRow.svelte';
	export let filteredDevices;
</script>

<div class="overflow-x-auto pt-4">
	<table class="table w-full">
		<!-- head -->
		<thead>
			<tr>
				<th>
					<label>
						<input type="checkbox" class="checkbox" />
					</label>
				</th>
				<th>Name</th>
				<th>IP Address</th>
				<th>Host</th>
				<th>Manageable</th>
				<th>Site</th>
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
