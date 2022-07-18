<script>
	import title from '$lib/stores/title';
	import * as api from '$lib/api';
	import DeviceStore from '$lib/stores/DeviceStore';
	import { onMount } from 'svelte';
	import DeviceTable from '../../components/DeviceTable.svelte';

	$title = 'Devices';
	let searchTerm = '';
	let filteredDevices = $DeviceStore;

	onMount(async () => {
		const data = await api.get(fetch, '/devices');
		DeviceStore.update((currentDevices) => {
			return data;
		});
	});

	$: {
		if (searchTerm) {
			filteredDevices = $DeviceStore.filter((item) =>
				item.name.toLowerCase().includes(searchTerm.toLowerCase())
			);
		} else {
			filteredDevices = [...$DeviceStore];
		}
	}
</script>

<svelte:head>
	<title>Devices | Netnotics</title>
</svelte:head>

<div class="card-normal">
	<input
		class="input input-bordered input-md input-primary w-full max-w-xs"
		type="text"
		placeholder="Search"
		bind:value={searchTerm}
	/>
	<div class="sm:flex sm:items-center pt-2">
		<div class="sm:flex-auto">
			<h1 class="text-xl font-semibold text-gray-900">Inventory</h1>
			<p class="mt-2 text-sm text-gray-700">Device Data</p>
		</div>
		<div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
			<a
				href="/devices/add"
				class="btn btn-primary inline-flex items-center justify-center sm:w-auto">Add Device</a
			>
		</div>
	</div>
	<DeviceTable {filteredDevices} />
</div>
