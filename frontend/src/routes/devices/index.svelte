<script>
	import title from '$lib/stores/title';
	import * as api from '$lib/api';
	import { DeviceStore } from '$lib/stores/DeviceStore';
	import { onMount } from 'svelte';
	import DeviceRow from '../../components/DeviceRow.svelte';

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

<div class="px-2 sm:px-4 lg:px-2">
	<input
		class="w-1/2 rounded-md text-lg pg-4 border-2 border-gray-200 mb-4"
		type="text"
		placeholder="Search"
		bind:value={searchTerm}
	/>
	<div class="sm:flex sm:items-center">
		<div class="sm:flex-auto">
			<h1 class="text-xl font-semibold text-gray-900">Inventory</h1>
			<p class="mt-2 text-sm text-gray-700">Device Data</p>
		</div>
		<div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
			<a
				href="/devices/add"
				class="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
				>Add Device</a
			>
		</div>
	</div>
	<div class="mt-8 flex flex-col">
		<div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
			<div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
				<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
					<table class="min-w-full divide-y divide-gray-300">
						<thead class="bg-gray-50">
							<tr>
								<th
									scope="col"
									class="whitespace-nowrap py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6"
									>Name</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>IP Address</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>Site</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>Model</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>Vendor</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>Operating System</th
								>
								<th
									scope="col"
									class="whitespace-nowrap px-2 py-3.5 text-left text-sm font-semibold text-gray-900"
									>OS Version</th
								>
								<th scope="col" class="relative whitespace-nowrap py-3.5 pl-3 pr-4 sm:pr-6">
									<span class="sr-only">Edit</span>
								</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each filteredDevices as device (device.id)}
								<DeviceRow {device} />
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</div>
