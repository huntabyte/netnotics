<script>
	import DeviceStore from '$lib/stores/DeviceStore';
	export let device;
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faTrashCan, faPen } from '@fortawesome/free-solid-svg-icons/index.es';
	import { remove } from '$lib/api';

	async function handleDelete() {
		const data = await remove(fetch, `/devices/${device.id}`);
		DeviceStore.update((currentDevices) => {
			return currentDevices.filter((item) => item.id != device.id);
		});
	}
</script>

<tr>
	{#each Object.entries(device) as [key, value], i}
		{#if key !== 'id'}
			<td>{value || '-'}</td>
			<!-- <td>{device.ip_address || '-'}</td>
	<td>{device.site || '-'}</td>
	<td>{device.model || '-'}</td>
	<td>{device.vendor || '-'}</td>
	<td>{device.operating_system || '-'}</td>
	<td>{device.os_version || '-'}</td> -->
		{/if}
	{/each}
	<td class="flex justify-around">
		<a href="/devices/{device.id}/edit" class="text-indigo-600 hover:text-indigo-900"
			><Fa icon={faPen} /></a
		>
		<button on:click={handleDelete} class="text-red-600 hover:text-red-900 ml-3"
			><Fa icon={faTrashCan} /></button
		>
	</td>
</tr>
