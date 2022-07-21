<script>
	import moment from 'moment';
	export let item;
	import { faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
	import Icon from './Icon.svelte';

	const lastChange = moment(item['last-change']).fromNow();
</script>

<tr>
	<td>
		<span class="link link-primary link-hover">
			{item.name}
		</span>
	</td>
	<td>X.X.X.X</td>
	<td>
		<span
			class="badge text-base-100 {item['admin-status'] === 'up' ? 'badge-success' : 'badge-error'}"
		>
			<!-- {item['admin-status'] === 'up' ? 'up' : 'down'} -->
			{#if item['admin-status'] === 'up'}
				<Icon data={faArrowUp} size="xs" />
			{:else}
				<Icon data={faArrowDown} size="xs" />
			{/if}
		</span>
	</td>
	<td>
		<span
			class="badge text-base-100 {item['oper-status'] === 'up' ? 'badge-success' : 'badge-error'}"
		>
			{#if item['oper-status'] === 'up'}
				<Icon data={faArrowUp} size="xs" />
			{:else}
				<Icon data={faArrowDown} size="xs" />
			{/if}
		</span>
	</td>
	<td>{item['phys-address']}</td>
	<td>{parseInt(item['speed']) / 1000000 + 'Mbps'}</td>
	<td>{lastChange}</td>
	<th>
		<a sveltekit:prefetch href="/devices" class="btn btn-secondary hover:text-white btn-xs"
			>details</a
		>
	</th>
</tr>
