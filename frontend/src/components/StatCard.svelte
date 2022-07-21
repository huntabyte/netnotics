<script>
	import Icon from '$components/Icon.svelte';

	export let title = 'Title';
	export let value = 'Value';
	export let desc = 'Description';
	export let figure;
	export let color = 'primary';
	export let Size = 'sm';
	export let link = '/';
</script>

<div class="stats shadow w-56">
	<div class="stat">
		<div class="stat-figure text-{color}">
			<Icon data={figure} {Size} />
		</div>
		<div class="stat-title">{title}</div>
		<a sveltekit:prefetch href={link} class="stat-value hover:text-primary cursor-pointer"
			>{value}</a
		>
		<div class="stat-desc">{desc}</div>
	</div>
</div>
