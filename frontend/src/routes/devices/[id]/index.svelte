<script context="module">
	export async function load({ fetch, params }) {
		const id = params.id;
		const url = `http://localhost:8000/devices/${id}`;
		let res = await fetch(url, {
			method: 'GET',
			credentials: 'include'
		});
		const device = await res.json();

		res = await fetch(`http://localhost:8000/devices/${id}/restconf?xpath=interfaces-state`);
		let data = await res.json();
		const interfaces = data['ietf-interfaces:interfaces-state']['interface'];
		console.log(interfaces);

		return {
			props: {
				device,
				interfaces
			}
		};
	}
</script>

<script>
	export let device;
	export let interfaces;
	import title from '$lib/stores/title';

	$title = device.name.toUpperCase();
</script>

<h1 class="text-2xl uppercase font-bold">Interface Status</h1>
<div class="divider" />

{#each interfaces as item}
	<h2 class="text-lg font-medium">{item.name}</h2>
	<p>Packets in: {item['statistics']['in-octets']}</p>

	<div class="stats shadow mb-4">
		<div class="stat">
			<div class="stat-figure text-primary">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="inline-block w-8 h-8 stroke-current"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
					/></svg
				>
			</div>
			<div class="stat-title">Admin Status</div>
			<div
				class="stat-value uppercase {item['admin-status'] === 'up' ? 'text-success' : 'text-error'}"
			>
				{item['admin-status']}
			</div>
		</div>

		<div class="stat">
			<div class="stat-figure text-secondary">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					class="inline-block w-8 h-8 stroke-current"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M13 10V3L4 14h7v7l9-11h-7z"
					/></svg
				>
			</div>
			<div class="stat-title">Oper Status</div>
			<div
				class="stat-value uppercase {item['oper-status'] === 'up' ? 'text-success' : 'text-error'}"
			>
				{item['oper-status']}
			</div>
		</div>
	</div>
{/each}
