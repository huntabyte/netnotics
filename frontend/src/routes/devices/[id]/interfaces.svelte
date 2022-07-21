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
	import Fa from 'svelte-fa';
	import { faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
	export let device;
	export let interfaces;
	import title from '$lib/stores/title';
	import Error from '../../__error.svelte';

	$title = device.name.toUpperCase();
</script>

<h1 class="text-2xl uppercase font-bold">Interface Status</h1>
<div class="divider" />

{#each interfaces as item}
	<h2 class="text-lg font-medium">{item.name}</h2>
	<p>Packets in: {item['statistics']['in-octets']}</p>

	<div class="stats shadow mb-4">
		<div class="stat">
			<div class="stat-figure {item['admin-status'] === 'up' ? 'text-success' : 'text-error'}">
				<Fa size="2x" icon={item['admin-status'] === 'up' ? faArrowUp : faArrowDown} />
			</div>
			<div class="stat-title">Admin Status</div>
			<div
				class="stat-value uppercase {item['admin-status'] === 'up' ? 'text-success' : 'text-error'}"
			>
				{item['admin-status']}
			</div>
		</div>

		<div class="stat">
			<div class="stat-figure {item['oper-status'] === 'up' ? 'text-success' : 'text-error'}">
				<Fa size="2x" icon={item['oper-status'] === 'up' ? faArrowUp : faArrowDown} />
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
