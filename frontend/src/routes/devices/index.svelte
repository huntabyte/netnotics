<script context="module">
	export async function load({ fetch, session }) {
		if (!session.authenticated) {
			return {
				status: 302,
				redirect: '/login'
			};
		}
		const url = `http://localhost:8000/devices`;
		const res = await fetch(url, {
			credentials: 'include'
		});
		const data = await res.json();
		return {
			props: {
				loadedDevices: data
			}
		};
	}
</script>

<script>
	import title from '$lib/stores/title';
	import DeviceTable from '../../components/DeviceTable.svelte';
	import { devices } from '$lib/stores/devices';
	export let loadedDevices;
	devices.set(loadedDevices);

	$title = 'Devices';
	let searchTerm = '';

	// $: {
	// 	if (searchTerm) {
	// 		filteredDevices = devices.filter((item) =>
	// 			item.name.toLowerCase().includes(searchTerm.toLowerCase())
	// 		);
	// 	} else {
	// 		filteredDevices = [...devices];
	// 	}
	// }
</script>

<svelte:head>
	<title>Devices | Netnotics</title>
</svelte:head>

<div class="px-4 sm:px-6 lg:px-8">
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
			<button
				type="button"
				class="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
				>Add Device</button
			>
		</div>
	</div>
	<DeviceTable />
</div>
