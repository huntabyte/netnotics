<script>
	import Icon from '$components/Icon.svelte';

	export let title = 'Title';
	export let value = 'Value';
	export let desc = 'Description';
	export let figure;
	export let color = 'primary';
	export let size = 'sm';
	export let link = '/';
</script>

<div class="stats shadow-lg w-56">
	<div class="stat">
		<div class="stat-figure text-{color}">
			<Icon icon={figure} {size} />
		</div>
		<div class="stat-title">{title}</div>
		<a sveltekit:prefetch href={link} class="stat-value hover:text-primary cursor-pointer"
			>{value}</a
		>
		<div class="stat-desc">{desc}</div>
	</div>
</div>
