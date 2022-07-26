<script>
	import { faCircle } from '@fortawesome/free-solid-svg-icons';
	import { faEllipsisVertical } from '@fortawesome/free-solid-svg-icons';
	import Icon from './Icon.svelte';
	export let device;
</script>

<tr>
	<th>
		<label>
			<input type="checkbox" class="checkbox checkbox-sm" />
		</label>
	</th>
	<td class="hover:text-primary"
		><a sveltekit:prefetch href="/devices/{device.id}">{device.name || '-'}</a></td
	>
	<td>{device.ip_address || '-'}</td>
	<td>{device.host || '-'}</td>
	<td>
		<span class={device.manageable ? 'text-success' : 'text-error'}>
			<Icon icon={faCircle} />
		</span>
	</td>
	<th>
		<div class="dropdown dropdown-left">
			<button class="ml-2 py-0.5 px-2">
				<Icon icon={faEllipsisVertical} />
			</button>
			<ul
				tabindex="0"
				class="dropdown-content menu menu-compact p-2 shadow bg-base-100 rounded-box w-28 font-normal"
			>
				<li><a sveltekit:prefetch href="/devices/{device.id}/edit">Edit</a></li>
				<li><a sveltekit:prefetch href="/devices/{device.id}">Details</a></li>
			</ul>
		</div>
	</th>
</tr>
