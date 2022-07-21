<script>
	import { faSpinner } from '@fortawesome/free-solid-svg-icons';
	import Fa from 'svelte-fa';
	export let data = faSpinner;
	export let Size;
</script>

<Fa icon={data} size={Size} />
