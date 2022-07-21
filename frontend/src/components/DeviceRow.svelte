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
	<th>
		<label>
			<input type="checkbox" class="checkbox" />
		</label>
	</th>
	<td class="hover:text-primary"
		><a sveltekit:prefetch href="/devices/{device.id}">{device.name || '-'}</a></td
	>
	<td>{device.ip_address || '-'}</td>
	<td>{device.site || '-'}</td>
	<td>{device.model || '-'}</td>
	<td>{device.vendor || '-'}</td>
	<td>{device.operating_system || '-'}</td>
	<th>
		<a
			sveltekit:prefetch
			href="/devices/{device.id}"
			class="btn btn-secondary hover:text-white btn-xs">details</a
		>
	</th>
</tr>
