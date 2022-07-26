<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const endpoint = `http://localhost:8000/devices/${id}/interfaces`;
		const res = await fetch(endpoint, {
			method: 'GET',
			credentials: 'include'
		});
		const data = await res.json();
		const device = data['device'];
		const interfaces = data['data'];

		if (res.ok) {
			return {
				props: {
					device: device,
					interfaces: interfaces
				}
			};
		}
		return {
			status: res.status,
			error: new Error('Could not fetch the device')
		};
	}
</script>

<script>
	export let device;
	export let interfaces;
	import title from '$lib/stores/title';
	import StatCard from '$components/StatCard.svelte';
	import InterfaceTable from '$components/InterfaceTable.svelte';
	import { faEthernet } from '@fortawesome/free-solid-svg-icons';
	$title = `Device Overview - ${device.name.toUpperCase()}`;
</script>

<div class="flex flex-col">
	<div class="flex justify-between">
		<h1 class="text-2xl font-semibold pb-4">{device.name}</h1>
		<a href="/devices/{device.id}/detect" class="btn btn-primary"> Detect </a>
	</div>
	<div class="flex pb-4">
		<StatCard
			title="Interfaces"
			value={interfaces.length}
			desc={''}
			figure={faEthernet}
			Size="lg"
			link="/devices/{device.id}/interfaces"
		/>
	</div>
	<div
		tabindex="0"
		class="collapse collapse-arrow border border-base-300 bg-base-100 rounded-box shadow-lg"
	>
		<input type="checkbox" checked />
		<div class="collapse-title text-xl font-medium">Interfaces</div>
		<div class="collapse-content">
			<InterfaceTable {interfaces} {device} />
		</div>
	</div>
</div>
