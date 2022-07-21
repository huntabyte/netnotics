<script>
	import { page } from '$app/stores';
	import Icon from '$components/Icon.svelte';

	export let title;
	export let href;
	export let icon;
</script>

<a
	{href}
	class="{$page.url.pathname.includes(href)
		? 'bg-gray-100 text-gray-900'
		: 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'} + text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
>
	<div class="text-gray-500 mr-3 flex items-center h-6 w-6">
		<Icon data={icon} />
		<p class="ml-2">
			{title}
		</p>
	</div>
</a>
