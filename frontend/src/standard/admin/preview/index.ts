import type { AppPageDefinition } from '@/router/pageRegistryTypes'

const page: AppPageDefinition = {
  routeName: 'AdminPreview',
  canonicalPath: '/admin/preview',
  menuLabel: '模型预览',
  component: () => import('./page.vue'),
}

export default page
