<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const url = `http://localhost:8000/devices/${id}`;
		const resOne = await fetch(url, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await resOne.json();

		const resTwo = await fetch(
			`http://localhost:8000/devices/${id}/restconf?xpath=interfaces-state`,
			{
				method: 'GET',
				credentials: 'include'
			}
		);
		let data = await resTwo.json();

		const interfaces = data['ietf-interfaces:interfaces-state']['interface'];

		if (resOne.ok && resTwo.ok) {
			return {
				props: {
					device,
					interfaces
				}
			};
		}
		return {
			status: resTwo.status,
			error: new Error('Could not retrieve device interface information')
		};
	}
</script>

<script>
	export let device;
	export let interfaces;
	import title from '$lib/stores/title';
	import Error from '../../__error.svelte';
	import InterfaceTable from '$components/InterfaceTable.svelte';

	$title = `Interface Overview - ${device.name.toUpperCase()}`;
</script>

<div class="shadow-xl">
	<InterfaceTable items={interfaces} />
</div>
