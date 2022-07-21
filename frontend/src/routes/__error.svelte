<script context="module">
	export function load({ error }) {
		return {
			props: { message: error.message }
		};
	}
</script>

<script>
	import title from '$lib/stores/title';
	export let message;
	$title = 'Error';
</script>

<h1>Oops</h1>
<p>{message}</p>
<a href="/">Return to Home</a>
