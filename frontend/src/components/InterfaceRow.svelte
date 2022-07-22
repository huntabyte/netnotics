<script>
	import moment from 'moment';
	export let item;
	export let device;
	import { faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
	import Icon from './Icon.svelte';

	const lastChange = moment(item['last-change']).fromNow();
</script>

<tr>
	<td>
		<span class="link link-primary link-hover">
			<a sveltekit:prefetch href="/devices/{device.id}/interfaces/{item.name}">
				{item.name}
			</a>
		</span>
	</td>
	<td>
		{#if item.ipv4 !== '0.0.0.0'}
			{item.ipv4}
		{:else}
			-
		{/if}
	</td>
	<td>
		<span
			class="badge text-base-100 {item['admin-status'].includes('up') ||
			item['admin-status'].includes('ready')
				? 'badge-success'
				: 'badge-error'}"
		>
			<!-- {item['admin-status'] === 'up' ? 'up' : 'down'} -->
			{#if item['admin-status'].includes('up') || item['admin-status'].includes('ready')}
				<Icon icon={faArrowUp} size="xs" />
			{:else}
				<Icon icon={faArrowDown} size="xs" />
			{/if}
		</span>
	</td>
	<td>
		<span
			class="badge text-base-100 {item['oper-status'].includes('up') ||
			item['oper-status'].includes('ready')
				? 'badge-success'
				: 'badge-error'}"
		>
			{#if item['oper-status'].includes('up') || item['oper-status'].includes('ready')}
				<Icon icon={faArrowUp} size="xs" />
			{:else}
				<Icon icon={faArrowDown} size="xs" />
			{/if}
		</span>
	</td>
	<td>{item['phys-address']}</td>
	<td>{parseInt(item['speed']) / 1000000 + 'Mbps'}</td>
	<td>{lastChange}</td>
	<th>
		<a
			sveltekit:prefetch
			href="/devices/{device.id}/interfaces/{item.name}"
			class="btn btn-secondary hover:text-white btn-xs">details</a
		>
	</th>
</tr>
