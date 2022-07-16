<script context="module">
	export async function load({ session }) {
		if (!session.authenticated) {
			return {
				status: 302,
				redirect: '/login'
			};
		}
		return {
			props: {
				id: session.user_id
			}
		};
	}
</script>

<script>
	export let id;
</script>

<h1>Profile {id}</h1>
