// https://vitepress.dev/guide/extending-default-theme#customizing-css

import DefaultTheme from 'vitepress/theme-without-fonts'
import './style.css'

import mediumZoom from 'medium-zoom';

export default {
  ...DefaultTheme,
  enhanceApp({ app, router, siteData }) {
    router.onAfterRouteChanged = () => {
      try {
        mediumZoom('.vp-doc img', { background: 'var(--vp-c-bg)', margin: 64 });
      } catch {
        // Ignore errors that we can have on build phase
      }
    };
  }
};
