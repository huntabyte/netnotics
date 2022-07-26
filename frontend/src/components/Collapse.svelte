<script>
	export let title;
	export let checked = false;
</script>

<div
	tabindex="0"
	class="collapse collapse-arrow border border-base-300 bg-base-100 rounded-box shadow-lg my-2"
>
	{#if checked}
		<input type="checkbox" checked />
	{:else}
		<input type="checkbox" />
	{/if}
	<div class="collapse-title text-xl font-medium">{title}</div>
	<div class="collapse-content">
		<slot />
	</div>
</div>
