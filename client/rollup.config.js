import svelte from 'rollup-plugin-svelte';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import html from '@rollup/plugin-html';
import css from 'rollup-plugin-css-only';

const production = !process.env.ROLLUP_WATCH;
const dir = production ? 'dist' : 'public';

const buildthese = [
  {
    path: '',
    title: 'Home',
  },
  {
    path: '/patient',
    title: 'Patient Info',
  },
  {
    path: '/login',
    title: 'Login',
  },
  {
    path: '/study',
    title: 'Study',
  },
];

function makeHTML({ publicPath, title }) {
  return `<!DOCTYPE html>
	<html>
		<head>
			<meta charset='utf-8'>
			<meta name='viewport' content='width=device-width'>
      <meta name="csrf-token" content="{{ csrf_token() }}" />
      <meta name="open-template-params" content="{{ template_params if template_params is not none else '' }}" />

			<title>${title}</title>
			<link rel='icon' type='image/png' href='/favicon.png'>
			<link rel='stylesheet' href='/global.css'>
			<link rel='stylesheet' href='.${publicPath}bundle.css'>
			<link rel='stylesheet' href='https://unpkg.com/tachyons@4.12.0/css/tachyons.min.css'/>
			<script defer src='.${publicPath}bundle.js'></script>
		</head>
		<body></body>
	</html>`;
}

const COMMON = function (mydir, page, index) {
  let path = page.path;
  let pageTitle = page.title;
  let ret = {
    input: 'src' + path + '/main.js',
    output: {
      sourcemap: !production,
      format: 'iife',
      name: 'app',
      file: mydir + path + '/bundle.js',
    },
    plugins: [
      /*html({
        html: `
<!doctype html>
<html>
<head>
	<meta charset='utf-8'>
	<meta name='viewport' content='width=device-width'>

	<title>${pageTitle}</title>

	<link rel='icon' type='image/png' href='/favicon.png'>
	<link rel='stylesheet' href='/global.css'>
	<link rel='stylesheet' href='${path}/bundle.css'>

	<script type="module" src=".${path}/main.js"></script>
</head>
<body></body>
</html>
`,
      }),*/
      svelte({
        dev: !production,
        /*css: (css) => {
          css.write(mydir + path + '/bundle.css', !production); // disable sourcemap in prod
        },*/
      }),
      css({ output: 'bundle.css' }),
      html({
        publicPath: path + '/',
        title: pageTitle,
        template: makeHTML,
      }),
      resolve({ browser: true }),
      commonjs(),
      !production &&
        livereload({
          watch: `public${path}`,
          port: 3000 + index,
        }),
      production && terser({ compress: true, mangle: true }),
    ],
    watch: {
      clearScreen: true,
    },
  };
  // if (!!page) {
  //   ret.plugins.splice(
  //     0,
  //     0,
  //     copy({
  //       targets: [
  //         { src: 'public/index.html', dest: mydir + page },
  //         { src: 'public/global.css', dest: mydir + page },
  //       ],
  //     })
  //   );
  // }
  return ret;
};

const exp = (function () {
  var ret = [];
  buildthese.forEach((target, i) => ret.push(COMMON(dir, target, i)));
  return ret;
})();

export default exp;
