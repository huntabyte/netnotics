<script>
	import { faSpinner } from '@fortawesome/free-solid-svg-icons';
	import Fa from 'svelte-fa';
	export let icon = faSpinner;
	export let size = '1x';
</script>

<Fa {icon} {size} />
