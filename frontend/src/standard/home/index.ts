import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'Home',
  canonicalPath: '/',
  menuLabel: '首页',
  component: () => import('./page.vue'),
}

export default page
