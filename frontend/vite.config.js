import { sveltekit } from '@sveltejs/kit/vite';
import path from 'path';

/** @type {import('vite').UserConfig} */
const config = {
	resolve: {
		alias: {
			'@': path.resolve('./src'),
			$lib: path.resolve('./src/lib'),
			$components: path.resolve('./src/components')
		}
	},
	plugins: [sveltekit()]
};

export default config;
