<script>
	import { faCircle } from '@fortawesome/free-solid-svg-icons';
	import Icon from './Icon.svelte';
	export let device;
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
	<td>{device.fqdn || '-'}</td>
	<td>
		<span class={device.manageable ? 'text-success' : 'text-error'}>
			<Icon icon={faCircle} />
		</span>
	</td>
	<td>{device.site || '-'}</td>
	<th>
		<a
			sveltekit:prefetch
			href="/devices/{device.id}"
			class="btn btn-secondary hover:text-white btn-xs">details</a
		>
	</th>
</tr>
