<script>
	import { DeviceStore } from '$lib/stores/DeviceStore';
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
	<td class="whitespace-nowrap py-2 pl-4 pr-3 text-sm text-gray-500 sm:pl-6"
		>{device.name || '-'}</td
	>
	<td class="whitespace-nowrap px-2 py-2 text-sm font-medium text-gray-900"
		>{device.ip_address || '-'}</td
	>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-900">{device.site || '-'}</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">{device.model || '-'}</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">{device.vendor || '-'}</td>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">{device.operating_system || '-'}</td
	>
	<td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">{device.os_version || '-'}</td>
	<td
		class="flex justify-around whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-6"
	>
		<a href="/devices/{device.id}" class="text-indigo-600 hover:text-indigo-900"
			><Fa icon={faPen} /></a
		>
		<button on:click={handleDelete} class="text-red-600 hover:text-red-900"
			><Fa icon={faTrashCan} /></button
		>
	</td>
</tr>
