<script>
	import { page } from '$app/stores';
	import Icon from '$components/Icon.svelte';
	import { sidebarOpen } from '$lib/stores/ui';

	export let title;
	export let href;
	export let icon;
</script>

<a
	sveltekit:prefetch
	{href}
	class="{$page.url.pathname.includes(href)
		? 'bg-gray-100 text-gray-900'
		: 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'} + text-gray-900 flex group items-center px-2 py-2 text-sm font-medium rounded-md"
	data-tip={title}
>
	<div
		class="text-gray-500 flex items-center justify-center h-8 w-full active:w-6 active:justify-start"
	>
		<span class="justify-self-center">
			<Icon {icon} size="1.25x" />
			<p class="ml-2 hidden active:visible">
				{title}
			</p>
		</span>
	</div>
</a>
