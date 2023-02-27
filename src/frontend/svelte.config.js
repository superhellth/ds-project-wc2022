import adapter from '@sveltejs/adapter-auto';
import preprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: preprocess(),
	onwarn: (warning, handler) => {
		const { code, frame } = warning;
		if (code === "css-unused-selector" || code === "unused-export-let" || code === "a11y-invalid-attribute" || code === "a11y-missing-attribute" || code === "a11y-click-events-have-key-events")
			return;

		handler(warning);
	},
	kit: {
		adapter: adapter()
	}
};

export default config;
