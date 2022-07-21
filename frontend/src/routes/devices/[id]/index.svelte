<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const endpoint = `http://localhost:8000/devices/${id}`;
		const res = await fetch(endpoint, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await res.json();

		const resTwo = await fetch(
			`http://localhost:8000/devices/${id}/restconf?xpath=interfaces-state`,
			{
				method: 'GET',
				credentials: 'include'
			}
		);
		const data = await resTwo.json();
		const interfaces = data['ietf-interfaces:interfaces-state']['interface'];

		if (res.ok) {
			if (resTwo.ok) {
				return {
					props: {
						device,
						numInterfaces: interfaces.length
					}
				};
			} else {
				return {
					props: {
						device,
						numInterfaces: 'N/A'
					}
				};
			}
		}
		return {
			status: res.status,
			error: new Error('Could not fetch the device')
		};
	}
</script>

<script>
	export let device;
	export let numInterfaces;
	import title from '$lib/stores/title';
	import StatCard from '$components/StatCard.svelte';
	import { faEthernet } from '@fortawesome/free-solid-svg-icons';
	import Fa from 'svelte-fa/src/fa.svelte';
	$title = `Device Overview - ${device.name.toUpperCase()}`;
</script>

<div class="container">
	<div class="flex">
		<StatCard
			title="Interfaces"
			value={numInterfaces}
			desc={''}
			figure={faEthernet}
			Size="lg"
			link="/devices/{device.id}/interfaces"
		/>
	</div>
</div>
