import { defineConfig } from 'vitepress';

import MarkdownItAbbr from 'markdown-it-abbr';
import MarkdownItDeflist from 'markdown-it-deflist';
import MarkdownItFootnote from 'markdown-it-footnote';

// https://vitepress.dev/reference/site-config

export default defineConfig({
  srcDir: './.md',
  outDir: './html',
  lang: 'en',
  title: 'HiPEAC Vision',
  description: 'Drawing on the expertise of HiPEAC\'s 2,000-strong European network of experts, the HiPEAC Vision acts as a strategic roadmap for the European computing community. It sets out the main technology trends and challenges in computing and explores what these will mean for research, business, and society in general.',
  themeConfig: {
    nav: [
      { text: 'Vision document', link: '/' },
      { text: 'HiPEAC.net', link: 'https://www.hipeac.net/' }
    ],
    footer: {
      message: 'The HiPEAC project has received funding from the European Union\'s Horizon Europe research and innovation funding programme under grant agreement number 101069836. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union. Neither the European Union nor the granting authority can be held responsible for them.',
      copyright: '© 2004-2023 High Performance, Edge And Cloud computing'
    },
    search: {
      provider: 'local'
    },
    sidebar: require('../.md/sidebar.json'),
    socialLinks: [
      { icon: 'youtube', link: 'https://www.youtube.com/@HiPEAC' }
    ]
  },
  appearance: false,
  lastUpdated: true,
  markdown: {
    config: (md) => {
      md.use(MarkdownItAbbr);
      md.use(MarkdownItDeflist);
      md.use(MarkdownItFootnote);
    }
  }
})
