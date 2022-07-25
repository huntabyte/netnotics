<script>
	import Icon from '$components/Icon.svelte';

	export let navActive;
	export let href;
	export let iconData;
	export let title;
</script>

<li>
	<a sveltekit:prefetch {href} class="content-start justify-start items-middle" data-tip="test">
		<span class="px-1 w-5 h-5">
			<Icon icon={iconData} size={'1.25x'} />
		</span>
		<span class={navActive ? 'ml-2' : 'hidden'}>{title}</span>
	</a>
</li>
