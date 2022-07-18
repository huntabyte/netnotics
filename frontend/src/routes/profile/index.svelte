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
				id: session.user_id,
				name: session.name,
				email: session.email
			}
		};
	}
</script>

<script>
	export let id;
	export let name;
	export let email;
</script>

<h1>Profile {id}</h1>
<p>Welcome {name}, you are logged in with the email {email}</p>
