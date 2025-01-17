import { defineConfig } from 'vitepress';

import MarkdownItAbbr from 'markdown-it-abbr';
import MarkdownItDeflist from 'markdown-it-deflist';
import MarkdownItFootnote from 'markdown-it-footnote';
import MarkdownItSub from 'markdown-it-sub';
import MarkdownItSup from 'markdown-it-sup';

// https://vitepress.dev/reference/site-config

export default defineConfig({
  srcDir: './.build',
  outDir: './html',

  lang: 'en',
  title: 'HiPEAC Vision',
  description: 'Drawing on the expertise of HiPEAC\'s 2,000-strong European network of experts, the HiPEAC Vision acts as a strategic roadmap for the European computing community. It sets out the main technology trends and challenges in computing and explores what these will mean for research, business, and society in general.',

  appearance: false,

  head: [
    ['meta', { name: 'theme-color', content: '#005eb8' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com' }],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Roboto+Slab:wght@400;600&display=swap',
      }
    ],
    [
      'script',
      { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=G-KXQ0GTGPP8' }
    ],
    [
      'script',
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-KXQ0GTGPP8');`
    ]
  ],

  themeConfig: {
    logo: '/hipeac.svg',
    sidebar: require('../.build/sidebar.json'),
    nav: [
      { text: 'Vision', link: '/introduction--foreword' },
      { text: 'HiPEAC.net', link: 'https://www.hipeac.net/' }
    ],
    search: {
      provider: 'local'
    },
    socialLinks: [
      { icon: 'youtube', link: 'https://www.youtube.com/@HiPEAC' }
    ],
    footer: {
      message: 'The HiPEAC project has received funding from the European Union\'s Horizon Europe research and innovation funding programme under grant agreement number 101069836. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union. Neither the European Union nor the granting authority can be held responsible for them.',
      copyright: '© 2004-2025 High Performance, Edge And Cloud computing'
    },
  },

  markdown: {
    config: (md) => {
      md.use(MarkdownItAbbr);
      md.use(MarkdownItDeflist);
      md.use(MarkdownItFootnote);
      md.use(MarkdownItSub);
      md.use(MarkdownItSup);
    }
  },
})
